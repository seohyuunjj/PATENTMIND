from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..security import create_access_token, hash_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=schemas.LoginResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    """MVP 목업 인증(API 명세서 §auth, 프론트 로그인 화면 문구 "Demo workspace: any password
    works in mock mode."와 동일한 정책을 실제 백엔드에서도 유지). 계정이 없으면 즉시 가입 처리하고,
    있으면 비밀번호 일치 여부와 무관하게 로그인을 허용한다 — 데모 편의성이 목적이며,
    실제 서비스 전환 시에는 verify_password 검증을 다시 활성화해야 한다."""
    user = db.query(models.User).filter_by(email=payload.email).first()
    if user is None:
        user = models.User(
            email=payload.email,
            name=payload.name or payload.email.split("@")[0],
            password_hash=hash_password(payload.password),
            role="engineer",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token(subject=user.id, role=user.role)
    return schemas.LoginResponse(token=token, user=schemas.UserOut.model_validate(user))
