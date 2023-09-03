from pydantic import BaseModel

from typing import Union, Optional
from datetime import datetime

from ..const import Assets, PaidButtons, InvoiceStatus


class Invoice(BaseModel):
    invoice_id: int
    status: Union[InvoiceStatus, str]
    hash: str
    asset: Union[Assets, str]
    amount: Union[int, float]
    fee: Optional[Union[int, float]] = None
    pay_url: str
    description: Optional[str] = None
    created_at: datetime
    usd_rate: Optional[Union[int, float]] = None
    allow_comments: bool
    allow_anonymous: bool
    expiration_date: Optional[str] = None
    paid_at: Optional[datetime] = None
    paid_anonymously: Optional[bool] = None
    comment: Optional[str] = None
    hidden_message: Optional[str] = None
    payload: Optional[str] = None
    paid_btn_name: Optional[Union[PaidButtons, str]] = None
    paid_btn_url: Optional[str] = None
