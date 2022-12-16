from pydantic import BaseModel, ValidationError, validator
from datetime import date, datetime, time, timedelta
from .modelBase import modelBase
class picture(modelBase):
    name:str
    albume: id
    originalPictureUri: str
    processedPictureUri: str
    nativeMetadata: object
    analiticsMetadata: object

    isDeleted: bool
    