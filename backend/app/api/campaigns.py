from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dashboard import summary
from app.core.config import settings
from app.core.database import get_db

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/advice")
def ai_advice(db: Session = Depends(get_db)):
    monthly = summary(period="month", db=db)
    yearly = summary(period="year", db=db)
    trend = monthly["revenue"] / (yearly["revenue"] / 12) if yearly["revenue"] else 0

    if monthly["margin"] < 15:
        action = "Cần tối ưu giá vốn hoặc cắt khuyến mại không hiệu quả"
    elif trend > 1.2:
        action = "Doanh thu tăng tốt, có thể mở rộng thêm kênh bán online"
    elif trend < 0.8:
        action = "Doanh thu đang giảm, cân nhắc tái cấu trúc trước khi mở rộng"
    else:
        action = "Giữ ổn định và thử nghiệm upsell combo đồ uống"

    return {
        "provider": settings.ai_provider,
        "generated_at": datetime.utcnow().isoformat(),
        "insight": action,
        "decision_hint": "Tiếp tục vận hành" if monthly["margin"] >= 12 else "Theo dõi để quyết định dừng/mở rộng",
    }
