"""정성 평가(§3.3) — 로드맵·스펙 중첩도(overlap_level), 회피설계 난이도(design_difficulty_level).

MVP/해커톤 데모 범위 결정(2026-09-08): 실제 LLM 청구항 대조 대신 목업으로 대체한다.
나중에 실제 LLM 연동 시 이 두 함수의 내부 구현만 교체하면 되고,
호출부(routers/searches.py)는 변경할 필요가 없도록 인터페이스를 고정해 둔다.
"""
import hashlib

from .. import models

LEVELS = ["상", "중", "하"]


def _stable_bucket(key: str, weights: list[float]) -> str:
    """patent.id 기반 결정적 해시로 상/중/하 중 하나를 고른다 (데모 재현성 확보)."""
    digest = hashlib.sha256(key.encode()).hexdigest()
    ratio = int(digest[:8], 16) / 0xFFFFFFFF
    cumulative = 0.0
    for level, weight in zip(LEVELS, weights):
        cumulative += weight
        if ratio <= cumulative:
            return level
    return LEVELS[-1]


def assess_overlap_level(query: str, patent: models.Patent) -> str:
    """로드맵·스펙 중첩도. TODO: 실제 LLM 연동 시 query(사내 스펙)와
    patent.independent_claim을 시맨틱 대조하여 상/중/하를 산출하도록 교체."""
    from .scoring import compute_quant_score

    quant_score = compute_quant_score(patent)
    # 정량 점수가 높을수록 중첩도 "상"에 가중치를 둔다 (데모용 근사치).
    if quant_score >= 70:
        weights = [0.7, 0.25, 0.05]
    elif quant_score >= 40:
        weights = [0.25, 0.55, 0.2]
    else:
        weights = [0.05, 0.35, 0.6]
    return _stable_bucket(f"overlap:{patent.id}:{query}", weights)


def assess_design_difficulty(patent: models.Patent) -> str:
    """회피설계 난이도. TODO: 실제 LLM 연동 시 필수 구성요소 치환 가능성 분석으로 교체."""
    weights = [0.4, 0.35, 0.25] if patent.family_size >= 3 else [0.15, 0.35, 0.5]
    return _stable_bucket(f"difficulty:{patent.id}", weights)
