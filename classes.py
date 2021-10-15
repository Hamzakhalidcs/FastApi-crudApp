from pydantic import BaseModel
from datetime import  datetime

class PersonData(BaseModel):
    user_id: int
    name: str
    cnic: str
    phone: str
    mobile: str
    address: str
    city: str
    picture_url: int
    comments: str


class del_data(BaseModel):
    user_id: int

class app_reviews(BaseModel):
    user_id : int
    rating : int
    comments : str