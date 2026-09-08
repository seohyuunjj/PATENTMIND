"""데모용 초기 데이터 시드. `python -m app.services.seed` 로 실행.

프론트엔드 src/mocks/index.js의 시나리오(고체 전해질 배터리 도메인)를 실제 DB 레코드로
재현해, 백엔드 연동 후에도 데모 흐름이 자연스럽게 이어지도록 한다.
"""
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from .. import models
from ..database import Base, SessionLocal, engine
from ..security import hash_password

PATENTS = [
    dict(
        title="황화물계 고체 전해질의 계면 안정화 구조",
        assignee="QuantumCell Technologies",
        filing_year=2024,
        countries=["KR", "US", "JP", "EP"],
        abstract="양극 활물질과 고체 전해질 사이에 탄성 완충층을 배치해 충방전 중 계면 저항 상승을 억제하는 기술입니다.",
        independent_claim="고체 전해질층과 양극층 사이에 이온전도성 완충층을 포함하고, 완충층의 탄성률을 특정 범위로 제어하는 배터리 셀.",
        family_size=4, citation_count=12, claim_count=22, has_dispute=True, legal_status="active",
        source="KIPRIS",
    ),
    dict(
        title="전고체 셀 제조를 위한 저온 압착 공정",
        assignee="NeoVolt Labs",
        filing_year=2023,
        countries=["KR", "US"],
        abstract="저온에서 압력을 단계적으로 증가시켜 전해질 분말의 밀도와 계면 접촉을 개선하는 제조 방법입니다.",
        independent_claim="전해질 분말을 2단계 이상의 압력 프로파일로 압착하고, 압착 후 열처리하는 제조 방법.",
        family_size=2, citation_count=6, claim_count=14, has_dispute=False, legal_status="active",
        source="Google Patents",
    ),
    dict(
        title="고체 전해질 입자 표면 코팅용 유무기 복합재",
        assignee="Sungwon Materials",
        filing_year=2022,
        countries=["KR"],
        abstract="전해질 입자 표면에 유무기 복합 코팅을 형성해 수분 민감도를 낮추고 공정 안정성을 높입니다.",
        independent_claim="황화물 입자 표면에 산화물 나노입자와 고분자 바인더를 포함하는 복합 코팅층을 형성하는 방법.",
        family_size=1, citation_count=2, claim_count=8, has_dispute=False, legal_status="expired",
        source="KIPRIS",
    ),
    dict(
        title="배터리 팩 열관리용 냉각 플레이트",
        assignee="K-Motion",
        filing_year=2021,
        countries=["KR"],
        abstract="배터리 모듈 하부 냉각 플레이트의 유로 설계에 관한 기술입니다.",
        independent_claim="복수의 냉각 유로가 형성된 냉각 플레이트 및 이를 포함하는 배터리 팩.",
        family_size=1, citation_count=0, claim_count=6, has_dispute=False, legal_status="abandoned",
        source="USPTO",
    ),
    dict(
        title="리튬메탈 음극 보호를 위한 인공 SEI 층 형성 방법",
        assignee="QuantumCell Technologies",
        filing_year=2025,
        countries=["KR", "US", "CN", "JP", "EP"],
        abstract="리튬메탈 표면에 무기물 기반 인공 SEI 층을 형성해 덴드라이트 성장을 억제합니다.",
        independent_claim="리튬메탈 음극 표면에 불소계 무기 화합물을 포함하는 보호층을 형성하는 이차전지 제조 방법.",
        family_size=5, citation_count=9, claim_count=19, has_dispute=True, legal_status="active",
        source="KIPRIS",
    ),
    dict(
        title="전고체 배터리용 건식 전극 시트 제조 장치",
        assignee="NeoVolt Labs",
        filing_year=2024,
        countries=["KR", "US"],
        abstract="용매 없이 전극 활물질과 바인더를 압연하여 건식 전극 시트를 연속 제조하는 장치입니다.",
        independent_claim="활물질, 도전재, 바인더 분말을 혼합 후 압연 롤러로 시트화하는 건식 전극 제조 장치.",
        family_size=2, citation_count=3, claim_count=11, has_dispute=False, legal_status="active",
        source="Google Patents",
    ),
]

SYNC_LOGS = [
    dict(source="KIPRIS", status="완료", records=2481, hours_ago=1),
    dict(source="Google Patents", status="완료", records=1832, hours_ago=2),
    dict(source="USPTO", status="진행 중", records=None, hours_ago=0),
]


def seed(db: Session) -> None:
    if not db.query(models.User).filter_by(email="engineer@patentmind.ai").first():
        db.add(models.User(
            id="u-001", email="engineer@patentmind.ai", name="김도윤",
            password_hash=hash_password("patentmind1234"), role="engineer",
        ))
    if not db.query(models.User).filter_by(email="admin@patentmind.ai").first():
        db.add(models.User(
            id="u-002", email="admin@patentmind.ai", name="운영자",
            password_hash=hash_password("patentmind1234"), role="admin",
        ))
    db.flush()

    if db.query(models.Patent).count() == 0:
        for row in PATENTS:
            db.add(models.Patent(**row))

    if db.query(models.SyncLog).count() == 0:
        now = datetime.utcnow()
        for row in SYNC_LOGS:
            db.add(models.SyncLog(
                source=row["source"], status=row["status"], records=row["records"],
                synced_at=now - timedelta(hours=row["hours_ago"]),
            ))

    db.commit()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        seed(session)
        print("시드 완료")
    finally:
        session.close()
