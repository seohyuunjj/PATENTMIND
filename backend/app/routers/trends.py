from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user

router = APIRouter(prefix="/api/trends", tags=["trends"])


@router.get("/applicant-trend", response_model=list[schemas.ApplicantTrendPoint])
def applicant_trend(db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    """연도별 출원 추이(§2.2). patents 테이블 실데이터를 연도별로 집계한다."""
    counts: dict[int, int] = defaultdict(int)
    for (year,) in db.query(models.Patent.filing_year).filter(models.Patent.filing_year.isnot(None)):
        counts[year] += 1
    return [
        schemas.ApplicantTrendPoint(year=year, value=counts[year])
        for year in sorted(counts.keys())
    ]


@router.get("/whitespace-heatmap", response_model=list[list[int]])
def whitespace_heatmap(db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    """기술 공백지 히트맵(§2.2). API 명세서상 응답 형태는 '부품/공정 축 x 경쟁사 축'
    밀도 행렬(0~9, 클수록 밀집)이다. 현재 patents 테이블에는 부품/공정 세부 태깅이 없어
    출원인(행) x 연도(열) 실데이터 건수를 0~9로 정규화해 근사치로 제공한다.
    TODO: 특허별 부품/공정 카테고리 태깅이 추가되면 원래 의도한 축으로 교체."""
    patents = db.query(models.Patent).all()
    assignees = sorted({p.assignee for p in patents})
    years = sorted({p.filing_year for p in patents if p.filing_year})
    if not assignees or not years:
        return []

    raw = [[0 for _ in years] for _ in assignees]
    for p in patents:
        if p.filing_year is None:
            continue
        raw[assignees.index(p.assignee)][years.index(p.filing_year)] += 1

    max_count = max((cell for row in raw for cell in row), default=0) or 1
    return [[round(cell / max_count * 9) for cell in row] for row in raw]
