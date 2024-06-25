from pydantic import BaseModel
from typing import Union

from ..const import Assets, Fiat


class ExchangeRate(BaseModel):
    is_valid: bool
    source: Union[Assets, Fiat]
    target: Fiat
    rate: Union[int, float]
