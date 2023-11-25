from pydantic import BaseModel

from typing import Union
from datetime import datetime

from ..const import Assets, CheckStatus


class Check(BaseModel):
    check_id: int
    hash: str
    asset: Union[Assets, str]
    amount: Union[int, float]
    bot_check_url: str
    status: Union[CheckStatus, str]
    created_at: datetime
