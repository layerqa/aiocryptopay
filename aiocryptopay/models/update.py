from pydantic import BaseModel
from datetime import datetime

from .invoice import Invoice


class Update(BaseModel):
    update_id: int
    update_type: str
    request_date: datetime
    payload: Invoice
