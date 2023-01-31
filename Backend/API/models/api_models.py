from pydantic import BaseModel as PydanticBaseModel
from typing import Optional,List

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True


class album(BaseModel):
    name: str
    description: Optional[str] = None
    count: int
    pictures: Optional[List[str]] =None
    isDeleted:str

class picture(BaseModel):
    name:str
    albume_id: Optional[List[str]] = None
    originalPictureUri: str
    processedPictureUri: str
    analiticsMetadata: dict
    isDeleted: str

class picture_in_album(BaseModel):
    album_name: str
    picture_name: str

class albumName(BaseModel):
    album_name: str

class albumId(BaseModel):
    album_id: str
    
class picture_id(BaseModel):
    picture_id: str



class filters(BaseModel):
    filter_list: list[str]

class picturUpload(albumName):
    file_path: str