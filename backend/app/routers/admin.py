from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import require_admin

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/sync-logs", response_model=list[schemas.SyncLogOut])
def sync_logs(db: Session = Depends(get_db), _: models.User = Depends(require_admin)):
    logs = db.query(models.SyncLog).order_by(models.SyncLog.synced_at.desc()).all()
    return [
        schemas.SyncLogOut(
            source=log.source,
            time=log.synced_at.strftime("%Y.%m.%d %H:%M"),
            status=log.status,
            records=f"{log.records:,}" if log.records is not None else "—",
        )
        for log in logs
    ]
