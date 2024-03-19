from datetime import datetime

from pydantic import BaseModel
from typing import Union


class AppStats(BaseModel):
    volume: Union[int, float]
    conversion: Union[int, float]
    unique_users_count: int
    created_invoice_count: int
    paid_invoice_count: int
    start_at: datetime
    end_at: datetime
