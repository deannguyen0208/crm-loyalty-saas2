from fastapi import APIRouter

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.get("")
def list_campaigns():
    return [
        {"id": 1, "name": "Happy Hour 14-16h", "channel": "In-store", "objective": "Tăng traffic giờ thấp điểm", "is_active": True},
        {"id": 2, "name": "Combo sáng", "channel": "Facebook", "objective": "Tăng AOV", "is_active": True},
    ]
