from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=schemas.LoginResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    """MVP 목업 인증(API 명세서 §auth). 계정이 없으면 즉시 가입 처리해 데모 진입 장벽을 없앤다.
    기존 계정이면 비밀번호를 검증한다."""
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
    elif not verify_password(payload.password, user.password_hash):
        # 401을 내는 대신 MVP 목업 정책상 재해시하지 않고 그대로 로그인 허용은 하지 않는다.
        from fastapi import HTTPException, status
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="비밀번호가 일치하지 않습니다.")

    token = create_access_token(subject=user.id, role=user.role)
    return schemas.LoginResponse(token=token, user=schemas.UserOut.model_validate(user))
