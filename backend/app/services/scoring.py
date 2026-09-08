"""정량 5대 지표 산식(기획서 §3.2) 및 4-Tier 판정 규칙(§3.4).

가중치/구간은 코드 레벨 고정값이며, 관리자가 임의로 조정할 수 없다
(v1.4 §3.5 결정: 표준화된 스코어링 원칙 유지).
"""
from .. import models

METRIC_LABELS = ["패밀리 크기", "피인용 횟수", "청구항 수·범위", "분쟁·심판 이력", "권리 유효성"]
METRIC_MAX = {"패밀리 크기": 25, "피인용 횟수": 25, "청구항 수·범위": 15, "분쟁·심판 이력": 20, "권리 유효성": 15}


def _family_size_score(family_size: int) -> int:
    if family_size >= 4:
        return 25
    if family_size >= 2:
        return 15
    return 5


def _citation_score(citation_count: int) -> int:
    if citation_count >= 10:
        return 25
    if citation_count >= 5:
        return 18
    if citation_count >= 1:
        return 10
    return 0


def _claim_score(claim_count: int) -> int:
    if claim_count >= 20:
        return 15
    if claim_count >= 10:
        return 10
    return 5


def _dispute_score(has_dispute: bool) -> int:
    return 20 if has_dispute else 0


def _legal_status_score(legal_status: str) -> int:
    return 15 if legal_status == "active" else 0


def compute_metrics(patent: models.Patent) -> list[dict]:
    scores = {
        "패밀리 크기": _family_size_score(patent.family_size),
        "피인용 횟수": _citation_score(patent.citation_count),
        "청구항 수·범위": _claim_score(patent.claim_count),
        "분쟁·심판 이력": _dispute_score(patent.has_dispute),
        "권리 유효성": _legal_status_score(patent.legal_status),
    }
    return [{"label": label, "score": scores[label], "max": METRIC_MAX[label]} for label in METRIC_LABELS]


def compute_quant_score(patent: models.Patent) -> int:
    return sum(item["score"] for item in compute_metrics(patent))


def determine_tier(quant_score: int, overlap_level: str | None, patent: models.Patent) -> str:
    """§3.4 4단계 최종 등급 매트릭스."""
    strong_signal = patent.family_size >= 3 or patent.citation_count >= 5

    if quant_score >= 70 and overlap_level == "상" and strong_signal:
        return "Core"
    if 40 <= quant_score <= 69 or overlap_level == "중":
        return "Major"
    if quant_score < 40:
        # Rule 필터를 통과했다는 전제하에 키워드 일치로 유입된 건은 Reference,
        # 그 외 최하위는 Noise로 분류한다 (Step1 탈락 건은 애초에 search_results에 적재하지 않음).
        return "Reference"
    return "Noise"
