from pydantic import BaseModel

from typing import Union


class Balance(BaseModel):
    currency_code: str
    available: Union[int, float]
    onhold: Union[int, float]
