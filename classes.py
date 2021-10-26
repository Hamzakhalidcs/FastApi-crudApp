from typing import Text
from pandas.core import base
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

class del_app_review_data(BaseModel):
    user_id : int

class app_insights_model(BaseModel):
    description : str
    sub_description : str
    document_id : int

class app_doc_speciality(BaseModel):
    user_id : int 
    spec_tag : str
    description : str

class app_attachments(BaseModel):
    user_id  : int
    document_url : str
    description : str
    tag : str

class app_prescription(BaseModel):
    user_id : int
    doctor_id : int
    prescription_doc_id : int