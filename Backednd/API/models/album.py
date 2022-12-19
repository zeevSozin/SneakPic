from pydantic import BaseModel
from typing import Optional,List
class album(BaseModel):
    name: str
    description: Optional[str] = None
    count: int
    picturs: Optional[List[str]] =None
    isDeleted:bool



