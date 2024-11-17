from typing import Any, Dict
from datetime import datetime

def create_response(data: Any, message: str = "Success") -> Dict:
    return {
        "data": data,
        "message": message,
        "timestamp": datetime.utcnow()
    } 