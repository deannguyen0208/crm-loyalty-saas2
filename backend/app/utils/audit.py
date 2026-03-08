from datetime import datetime


def audit_log(action: str, actor: str) -> str:
    return f"[{datetime.utcnow().isoformat()}] {actor}: {action}"
