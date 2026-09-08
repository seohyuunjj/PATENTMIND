from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user
from ..services import scoring

router = APIRouter(prefix="/api/search-results", tags=["search-results"])


def _get_owned_result(db: Session, result_id: str, user: models.User) -> models.SearchResult:
    result = db.get(models.SearchResult, result_id)
    if result is None or result.search.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="대상을 찾을 수 없습니다.")
    return result


@router.get("/{result_id}", response_model=schemas.ResultDetail)
def get_detail(result_id: str, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    result = _get_owned_result(db, result_id, user)
    patent = result.patent
    return schemas.ResultDetail(
        id=result.id, title=patent.title, assignee=patent.assignee, year=patent.filing_year,
        tier=result.tier, score=scoring.compute_quant_score(patent), confidence=result.overlap_level,
        abstract=patent.abstract, claim=patent.independent_claim,
        metrics=scoring.compute_metrics(patent), designDifficulty=result.design_difficulty_level,
        confirmNeeded=result.confirm_needed, note=result.note,
    )


@router.patch("/{result_id}/confirm-tag", response_model=schemas.OkResponse)
def confirm_tag(
    result_id: str,
    payload: schemas.ConfirmTagRequest,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    result = _get_owned_result(db, result_id, user)
    result.confirm_needed = payload.confirmNeeded
    result.note = payload.note
    db.commit()
    return schemas.OkResponse(ok=True)
