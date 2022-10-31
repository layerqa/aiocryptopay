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
    fee: Optional[Union[int, float]]
    pay_url: str
    description: Optional[str]
    created_at: datetime
    usd_rate: Optional[Union[int, float]]
    allow_comments: bool
    allow_anonymous: bool
    expiration_date: Optional[str]
    paid_at: Optional[datetime]
    paid_anonymously: Optional[bool]
    comment: Optional[str]
    hidden_message: Optional[str]
    payload: Optional[str]
    paid_btn_name: Optional[Union[PaidButtons, str]]
    paid_btn_url: Optional[str]