from typing import Text
from pydantic import BaseModel
from datetime import  datetime

class PersonData(BaseModel):
    user_id: int
    name: str
    cnic: str
    phone : str
    mobile : str
    address : str
    city : str
    PostingDate : datetime
    Lastupdate : datetime
    is_doctor : bool
    picture_url : int
    comments : str

class del_data(BaseModel):
    person_id : int



