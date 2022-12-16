from pydantic import BaseModel, ValidationError, validator
from datetime import date, datetime, time, timedelta
class modelBase(BaseModel):
    id: int
    creatinDate:datetime
    def __init__(self):
        self.id+=1
        self.creationDate = datetime.now