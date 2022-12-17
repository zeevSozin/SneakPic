from pydantic import BaseModel,validator, Field
from datetime import date, datetime, time, timedelta
from typing import List
from .picture import picture
from pydantic import BaseModel,NoneStr
from uuid import UUID, uuid4
from typing import Optional
from typing_extensions import Annotated
class album(BaseModel):
    name: str
    description: Optional[str] = None
    count: int
    picturs: Optional[List[str]] =None
    isDeleted:bool



