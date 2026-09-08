import uuid
from datetime import datetime, date

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    TypeDecorator,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class StringArray(TypeDecorator):
    """PostgreSQL에서는 네이티브 text[]로, 그 외(SQLite 등 로컬 개발/테스트)에서는
    JSON 배열로 저장하는 이식성 있는 배열 타입. 운영 배포는 PostgreSQL을 사용한다."""

    impl = JSON
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_ARRAY(String))
        return dialect.type_descriptor(JSON())

    def process_bind_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        return value


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False, default="engineer")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    searches: Mapped[list["Search"]] = relationship(back_populates="user")


class Search(Base):
    __tablename__ = "searches"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    query: Mapped[str] = mapped_column(Text, nullable=False)
    period: Mapped[str] = mapped_column(String, nullable=False, default="최근 5년")
    period_from: Mapped[date | None] = mapped_column(Date, nullable=True)
    period_to: Mapped[date | None] = mapped_column(Date, nullable=True)
    exclude_expired: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    countries: Mapped[list[str]] = mapped_column(
        StringArray, nullable=False, default=lambda: ["KR", "US", "EP", "JP", "CN"]
    )
    company: Mapped[str] = mapped_column(String, default="전체 기업")
    status: Mapped[str] = mapped_column(String, nullable=False, default="processing")
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    step: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="searches")
    results: Mapped[list["SearchResult"]] = relationship(back_populates="search")


class Patent(Base):
    __tablename__ = "patents"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    application_no: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    assignee: Mapped[str] = mapped_column(String, nullable=False)
    filing_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    countries: Mapped[list[str] | None] = mapped_column(StringArray, nullable=True)
    abstract: Mapped[str | None] = mapped_column(Text, nullable=True)
    independent_claim: Mapped[str | None] = mapped_column(Text, nullable=True)

    # 정량 5대 지표 산식(§3.2)의 원본 입력값 — 점수 자체는 서비스 계층에서 매번 계산한다
    family_size: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    citation_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    claim_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    has_dispute: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    legal_status: Mapped[str] = mapped_column(String, nullable=False, default="active")

    source: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, onupdate=datetime.utcnow, nullable=True)

    results: Mapped[list["SearchResult"]] = relationship(back_populates="patent")


class SearchResult(Base):
    __tablename__ = "search_results"
    __table_args__ = (UniqueConstraint("search_id", "patent_id", name="uq_search_patent"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    search_id: Mapped[str] = mapped_column(ForeignKey("searches.id"), nullable=False)
    patent_id: Mapped[str] = mapped_column(ForeignKey("patents.id"), nullable=False)

    tier: Mapped[str] = mapped_column(String, nullable=False)  # Core | Major | Reference | Noise
    overlap_level: Mapped[str | None] = mapped_column(String, nullable=True)  # 상|중|하 (LLM, 목업)
    design_difficulty_level: Mapped[str | None] = mapped_column(String, nullable=True)  # 상|중|하 (LLM, 목업)

    confirm_needed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    search: Mapped["Search"] = relationship(back_populates="results")
    patent: Mapped["Patent"] = relationship(back_populates="results")


class SyncLog(Base):
    __tablename__ = "sync_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    source: Mapped[str] = mapped_column(String, nullable=False)  # KIPRIS | Google Patents | USPTO
    synced_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String, nullable=False)  # 완료 | 진행 중 | 실패
    records: Mapped[int | None] = mapped_column(Integer, nullable=True)
