from pydantic import BaseModel
from typing import Union


class ExchangeRate(BaseModel):
    is_valid: bool
    is_crypto: bool
    is_fiat: bool
    source: str
    target: str
    rate: float
