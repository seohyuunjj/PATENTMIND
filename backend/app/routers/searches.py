import time
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user
from ..services import qualitative, scoring

router = APIRouter(prefix="/api/searches", tags=["searches"])

# 데모용 진행 애니메이션 총 소요 시간(초). 이 시간 동안 progress가 0→100으로 올라가도록
# GET /status에서 매 호출마다 경과 시간 기반으로 계산한다 (별도 백그라운드 워커 불필요).
PROCESSING_DURATION_SECONDS = 4

# 자연어 질의 → 동의어/IPC 코드 추천 목업 사전. TODO: 실제 LLM 연동 시 교체.
EXPANSION_LIBRARY = [
    (["전해질", "배터리", "이차전지", "battery", "electrolyte"], {
        "synonyms": ["고체 전해질", "solid-state electrolyte", "황화물계 전해질", "sulfide-based electrolyte"],
        "ipcCodes": ["H01M 10/052", "H01M 4/136", "C01B 17/22"],
    }),
    (["라이다", "센서", "lidar", "sensor"], {
        "synonyms": ["라이다 노이즈 제거", "point cloud denoising", "실시간 필터링"],
        "ipcCodes": ["G01S 7/48", "G01S 17/931"],
    }),
    (["엣지", "추론", "가속기", "edge", "inference", "accelerator"], {
        "synonyms": ["저전력 NPU", "온디바이스 AI", "edge inference accelerator"],
        "ipcCodes": ["G06N 3/063", "G06F 15/78"],
    }),
]
DEFAULT_EXPANSION = {"synonyms": ["관련 기술 용어 확장(예시)"], "ipcCodes": ["G06F 00/00"]}


def _new_id(prefix: str) -> str:
    return f"{prefix}-{int(time.time() * 1000) % 100000}-{uuid.uuid4().hex[:4]}"


def _run_screening(db: Session, search: models.Search) -> None:
    """Step1(Rule 필터) → Step2(정량) → Step3(정성) → Step4(등급배정)을 동기로 실행하고
    search_results를 채운다. 해커톤 데모 범위: KIPRIS 등 외부 API 대신 patents 테이블의
    실데이터(정량 원본 필드)를 사용하고, 정성 평가만 목업 함수로 대체한다."""
    query_filter = db.query(models.Patent)
    candidates = query_filter.all()

    for patent in candidates:
        # Step 1: Rule 필터 (국가/존속상태/출원인)
        if search.exclude_expired and patent.legal_status in ("expired", "abandoned", "rejected"):
            continue
        if search.countries and patent.countries and not set(patent.countries) & set(search.countries):
            continue
        if search.company and search.company != "전체 기업" and patent.assignee != search.company:
            continue

        # Step 2: 정량 평가
        quant_score = scoring.compute_quant_score(patent)
        # Step 3: 정성 평가 (목업)
        overlap_level = qualitative.assess_overlap_level(search.query, patent)
        design_difficulty_level = qualitative.assess_design_difficulty(patent)
        # Step 4: 등급 배정
        tier = scoring.determine_tier(quant_score, overlap_level, patent)

        db.add(models.SearchResult(
            id=_new_id("r"),
            search_id=search.id,
            patent_id=patent.id,
            tier=tier,
            overlap_level=overlap_level,
            design_difficulty_level=design_difficulty_level,
        ))

    search.status = "completed"
    search.progress = 100
    search.step = 4
    db.commit()


def _search_summary(db: Session, search: models.Search) -> schemas.SearchSummary:
    results = db.query(models.SearchResult).filter_by(search_id=search.id).all()
    return schemas.SearchSummary(
        id=search.id,
        query=search.query,
        status="완료" if search.status == "completed" else "진행중",
        createdAt=search.created_at.strftime("%Y.%m.%d"),
        count=len(results),
        core=sum(1 for r in results if r.tier == "Core"),
        major=sum(1 for r in results if r.tier == "Major"),
    )


@router.get("", response_model=list[schemas.SearchSummary])
def list_searches(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    searches = db.query(models.Search).filter_by(user_id=user.id).order_by(models.Search.created_at.desc()).all()
    return [_search_summary(db, s) for s in searches]


@router.post("", response_model=schemas.SearchSummary, status_code=status.HTTP_201_CREATED)
def create_search(
    payload: schemas.SearchCreateRequest,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    search = models.Search(
        id=_new_id("PM"),
        user_id=user.id,
        query=payload.query,
        period=payload.period,
        period_from=payload.periodFrom,
        period_to=payload.periodTo,
        exclude_expired=payload.excludeExpired,
        countries=list(payload.countries),
        company=payload.company,
        status="processing",
        progress=0,
        step=0,
    )
    db.add(search)
    db.commit()
    db.refresh(search)

    # 결과 계산 자체는 동기로 즉시 완료하되(해커톤 데모 규모에서는 수 ms 수준),
    # 프론트 처리중 화면은 /status의 경과시간 기반 progress로 애니메이션을 보여준다.
    _run_screening(db, search)

    return _search_summary(db, search)


@router.post("/expand", response_model=schemas.QueryExpansion)
def expand_query(payload: schemas.QueryExpansionRequest):
    text = payload.query.lower()
    for keywords, expansion in EXPANSION_LIBRARY:
        if any(keyword.lower() in text for keyword in keywords):
            return schemas.QueryExpansion(**expansion)
    return schemas.QueryExpansion(**DEFAULT_EXPANSION)


@router.get("/{search_id}/status", response_model=schemas.SearchStatus)
def get_status(search_id: str, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    search = db.get(models.Search, search_id)
    if search is None or search.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="검색을 찾을 수 없습니다.")

    if search.status != "processing":
        return schemas.SearchStatus(id=search.id, progress=search.progress, step=search.step, status=search.status)

    created_at = search.created_at.replace(tzinfo=timezone.utc)
    elapsed = (datetime.now(timezone.utc) - created_at).total_seconds()
    ratio = min(elapsed / PROCESSING_DURATION_SECONDS, 1.0)
    progress = int(ratio * 100)
    step = min(int(ratio * 5), 4)
    return schemas.SearchStatus(
        id=search.id, progress=progress, step=step,
        status="completed" if ratio >= 1.0 else "processing",
    )


@router.get("/{search_id}/results", response_model=list[schemas.ResultSummary])
def get_results(
    search_id: str,
    tier: str | None = Query(default=None),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    search = db.get(models.Search, search_id)
    if search is None or search.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="검색을 찾을 수 없습니다.")

    query = db.query(models.SearchResult).filter_by(search_id=search_id)
    if tier and tier != "All":
        query = query.filter_by(tier=tier)
    results = query.all()

    return [
        schemas.ResultSummary(
            id=r.id, title=r.patent.title, assignee=r.patent.assignee, year=r.patent.filing_year,
            tier=r.tier, score=scoring.compute_quant_score(r.patent), confidence=r.overlap_level,
            abstract=r.patent.abstract,
        )
        for r in results
    ]
