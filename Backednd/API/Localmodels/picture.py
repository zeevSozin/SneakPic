from pydantic import BaseModel,Field
from datetime import date, datetime, time, timedelta
from uuid import UUID, uuid4
from pydantic import BaseModel, NoneStr
from typing import Optional,List
class picture(BaseModel):
    name:str
    albume_id: Optional[List[str]] = None
    originalPictureUri: str
    processedPictureUri: str
    nativeMetadata: dict
    analiticsMetadata: dict
    isDeleted: bool
    