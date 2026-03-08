import json
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.dashboard import best_sellers, employee_kpi, summary
from app.core.config import settings
from app.core.database import get_db

router = APIRouter(prefix="/data", tags=["data"])


@router.post("/cloud-snapshot")
def cloud_snapshot(db: Session = Depends(get_db)):
    payload = {
        "created_at": datetime.utcnow().isoformat(),
        "summary_month": summary(period="month", db=db),
        "summary_year": summary(period="year", db=db),
        "best_sellers": best_sellers(db=db),
        "employee_kpi": employee_kpi(db=db),
    }
    output_dir = Path(settings.cloud_storage_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / f"snapshot-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}.json"
    file_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"message": "Đã lưu snapshot cloud", "path": str(file_path)}


@router.get("/export")
def export_report(db: Session = Depends(get_db)):
    output_dir = Path("./exports")
    output_dir.mkdir(exist_ok=True)
    file_path = output_dir / "business-report.json"
    payload = {
        "summary_week": summary(period="week", db=db),
        "summary_month": summary(period="month", db=db),
        "summary_quarter": summary(period="quarter", db=db),
        "summary_year": summary(period="year", db=db),
        "best_sellers": best_sellers(db=db),
        "employee_kpi": employee_kpi(db=db),
    }
    file_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return FileResponse(file_path)
