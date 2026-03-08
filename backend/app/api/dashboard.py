from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.order import Order

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _period_key(date_value):
    iso = date_value.isocalendar()
    quarter = (date_value.month - 1) // 3 + 1
    return {
        "week": f"{date_value.year}-W{iso.week}",
        "month": f"{date_value.year}-{date_value.month:02d}",
        "quarter": f"{date_value.year}-Q{quarter}",
        "year": f"{date_value.year}",
    }


@router.get("/overview")
def get_overview(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    revenue = sum(o.total_amount for o in orders)
    cost = sum(o.cost_amount for o in orders)
    profit = revenue - cost

    trend = {"week": defaultdict(float), "month": defaultdict(float), "quarter": defaultdict(float), "year": defaultdict(float)}
    seller = defaultdict(float)
    staff_perf = defaultdict(lambda: {"revenue": 0.0, "orders": 0, "profit": 0.0})
    payments = defaultdict(float)

    for o in orders:
        keys = _period_key(o.created_at)
        for k, key in keys.items():
            trend[k][key] += o.total_amount

        seller[o.item_name] += o.total_amount
        staff_perf[o.staff_name]["revenue"] += o.total_amount
        staff_perf[o.staff_name]["orders"] += 1
        staff_perf[o.staff_name]["profit"] += o.total_amount - o.cost_amount
        payments[o.payment_method] += o.total_amount

    sorted_sellers = sorted(seller.items(), key=lambda x: x[1], reverse=True)
    staff_kpis = [
        {
            "staff_name": name,
            "revenue": round(data["revenue"], 2),
            "orders": data["orders"],
            "profit": round(data["profit"], 2),
            "avg_ticket": round(data["revenue"] / data["orders"], 2),
        }
        for name, data in staff_perf.items()
    ]

    ai_advice = "Duy trì hoạt động"
    margin = (profit / revenue) if revenue else 0
    if revenue < 50_000_000 and margin < 0.1:
        ai_advice = "Cần xem xét thu hẹp chi phí, chạy khuyến mãi có chọn lọc hoặc cân nhắc dừng kinh doanh nếu xu hướng kéo dài 2 quý."
    elif revenue >= 50_000_000 and margin >= 0.18:
        ai_advice = "Hiệu suất tốt, có thể mở rộng bằng combo giờ thấp điểm hoặc bán online qua nền tảng giao hàng."

    return {
        "cloud_storage": {
            "provider": "S3-compatible",
            "bucket": settings.cloud_bucket_name,
            "region": settings.cloud_region,
            "status": "connected-demo",
        },
        "summary": {
            "orders": len(orders),
            "revenue": round(revenue, 2),
            "cost": round(cost, 2),
            "profit": round(profit, 2),
            "margin": round(margin * 100, 2),
        },
        "trend": {k: dict(v) for k, v in trend.items()},
        "best_sellers": [{"item": name, "revenue": round(total, 2)} for name, total in sorted_sellers[:5]],
        "staff_kpis": sorted(staff_kpis, key=lambda x: x["revenue"], reverse=True),
        "payment_breakdown": dict(payments),
        "ai_advice": ai_advice,
        "liquidity_note": "Có thể xuất dữ liệu JSON/CSV từ endpoint /api/dashboard/export để phục vụ chuyển đổi hệ thống khi dừng dịch vụ.",
    }


@router.get("/export")
def export_data(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return {
        "orders": [
            {
                "id": o.id,
                "staff_name": o.staff_name,
                "item_name": o.item_name,
                "total_amount": o.total_amount,
                "payment_method": o.payment_method,
                "created_at": o.created_at.isoformat() if o.created_at else None,
            }
            for o in orders
        ]
    }
