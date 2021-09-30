from fastapi import FastAPI
import sys
import pandas as pd
from datetime import datetime as dt
import pyodbc
from pydantic import BaseModel


class PersonData(BaseModel):
    person_id: int
    first_name: str
    last_name: str

class del_data(BaseModel):
    person_id : int


try:
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=DESKTOP-959UNBS;"
        "Database=mydb;"
        "Trusted_Connection=yes;"
    )

    print("Connected Succesfully")

except:
    print("Cannot connect to DB" + str(sys.exc_info()[1]))


app = FastAPI()

# Getting data from database using this Api
@app.get("/get_data")
def get_data():
    query = "SELECT * FROM [mydb].[dbo].[Table_1] order by PersonID ASC"
    data = pd.read_sql(query, conn).fillna("")
    obj = data.to_dict(orient="records")
    return obj


# Inserting data in to databse this ......
@app.post("/post_data")
def post_data(person_data: PersonData):
    print(person_data)
    modified_date = str(dt.today())[:19]

    cursor = conn.cursor()
    query = """
    INSERT INTO [mydb].[dbo].[Table_1]
    (PersonID, FirstName, LastName, ModifiedDate) VALUES ({}, '{}', '{}','{}')
    """.format(
        person_data.person_id,
        person_data.first_name,
        person_data.last_name,
        modified_date,
    )
    print("QUERY: ", query)
    cursor.execute(query)
    cursor.commit()
    cursor.close()
    return {
        "suscess": True,
        "data": {
            "PersonID": person_data.person_id,
            "First Name": person_data.first_name,
            "Last Name": person_data.last_name,
            "ModifiedDate": modified_date,
        },
    }


# Update data in database using that api
@app.post("/update_data")
def update_data(person_data: PersonData):

    cursor = conn.cursor()
    update_query = """
    UPDATE [mydb].[dbo].[Table_1]
    SET FirstName= '{}', LastName = '{}' 
    WHERE PersonID={};""".format(
        person_data.first_name, person_data.last_name, person_data.person_id
    )
    print("QUERY: ", update_query)

    cursor.execute(update_query)
    cursor.commit()
    cursor.close()
    return (
        {
            "success": True,
        },
    )


# Delete a complete row data using this delete method
@app.delete("/delete_data>")
def del_data(delete_data: del_data):

    cursor = conn.cursor()
    delete_query = """
    DELETE FROM [mydb].[dbo].[Table_1]
    WHERE PersonID={};""".format(
        delete_data.person_id
    )
    print("QUERY: ", delete_query)

    cursor.execute(delete_query)
    cursor.commit()
    cursor.close()
    return ({"message": "Data delete successfully"},)
