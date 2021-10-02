from pydantic import BaseModel

class PersonData(BaseModel):
    person_id: int
    first_name: str
    last_name: str

class del_data(BaseModel):
    person_id : int