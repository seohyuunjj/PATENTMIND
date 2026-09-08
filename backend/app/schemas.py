from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field

Role = Literal["engineer", "ip_team", "pm", "admin"]
Tier = Literal["Core", "Major", "Reference", "Noise"]
Level = Literal["상", "중", "하"]
Country = Literal["KR", "US", "EP", "JP", "CN"]
Period = Literal["최근 3년", "최근 5년", "최근 10년", "직접 설정"]


class UserOut(BaseModel):
    id: str
    name: str
    email: str
    role: Role

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    token: str
    user: UserOut


# ---- searches ----

class SearchCreateRequest(BaseModel):
    query: str
    period: Period = "최근 5년"
    periodFrom: Optional[date] = None
    periodTo: Optional[date] = None
    excludeExpired: bool = True
    countries: list[Country] = Field(default_factory=lambda: ["KR", "US", "EP", "JP", "CN"])
    company: Optional[str] = None


class SearchSummary(BaseModel):
    id: str
    query: str
    status: Literal["완료", "진행중"]
    createdAt: str
    count: int
    core: int
    major: int

    class Config:
        from_attributes = True


class SearchStatus(BaseModel):
    id: str
    progress: int = Field(ge=0, le=100)
    step: int = Field(ge=0, le=4)
    status: Literal["processing", "completed", "failed"]


class QueryExpansionRequest(BaseModel):
    query: str


class QueryExpansion(BaseModel):
    synonyms: list[str]
    ipcCodes: list[str]


# ---- search results ----

class ResultSummary(BaseModel):
    id: str
    title: str
    assignee: str
    year: Optional[int] = None
    tier: Tier
    score: int
    confidence: Optional[Level] = None
    abstract: Optional[str] = None


class MetricBreakdown(BaseModel):
    label: Literal["패밀리 크기", "피인용 횟수", "청구항 수·범위", "분쟁·심판 이력", "권리 유효성"]
    score: int
    max: int


class ResultDetail(ResultSummary):
    claim: Optional[str] = None
    metrics: list[MetricBreakdown]
    designDifficulty: Optional[Level] = None
    confirmNeeded: bool = False
    note: Optional[str] = None


class ConfirmTagRequest(BaseModel):
    confirmNeeded: bool
    note: Optional[str] = None


class OkResponse(BaseModel):
    ok: bool = True


# ---- trends ----

class ApplicantTrendPoint(BaseModel):
    year: int
    value: int


# ---- admin ----

class SyncLogOut(BaseModel):
    source: Literal["KIPRIS", "Google Patents", "USPTO"]
    time: str
    status: Literal["완료", "진행 중", "실패"]
    records: str

    class Config:
        from_attributes = True
