from pydantic import BaseModel
from typing import Union


class ExchangeRate(BaseModel):
    is_valid: bool
    source: str
    target: str
    rate: Union[int, float]
