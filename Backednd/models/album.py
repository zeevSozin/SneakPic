from pydantic import BaseModel, ValidationError, validator
from datetime import date, datetime, time, timedelta
from .modelBase import modelBase
from .picture import picture
class album(modelBase):
    name: str
    description: str 
    count: int
    picturs: list[picture]
    isDeleted:bool

    @validator('description')
    def checkDescriptionLength(cls, v):
        assert len(v)>100, f'only 100 characters allowed!!'
        return v

