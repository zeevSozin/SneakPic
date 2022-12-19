from pydantic import BaseModel
from typing import Optional,List
class picture(BaseModel):
    name:str
    albume_id: Optional[List[str]] = None
    originalPictureUri: str
    processedPictureUri: str
    nativeMetadata: dict
    analiticsMetadata: dict
    isDeleted: bool
    