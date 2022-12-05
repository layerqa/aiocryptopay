from pydantic import BaseModel

from typing import Union, Optional
from datetime import datetime

from ..const import Assets


class Transfer(BaseModel):
    transfer_id: int
    user_id: int
    asset: Union[Assets, str]
    amount: Union[int, float]
    status: str
    completed_at: datetime
    comment: Optional[str]
