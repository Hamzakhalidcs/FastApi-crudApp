from fastapi import FastAPI
import os
import sys
import pandas as pd
from datetime import datetime as dt
import pyodbc
from classes import *
from dotenv import load_dotenv

load_dotenv()

driver = os.getenv("driver")
server = os.getenv("server")
database = os.getenv("database")
table = os.getenv("table_name")

try:
    conn = pyodbc.connect(
        "Driver= {};"
        "Server={};"
        "Database={};"
        "port = 1433;"
        "Trusted_Connection=yes;".format(driver, server, database)
    )
    print("Connected Succesfully")

except:
    print("Cannot connect to DB" + str(sys.exc_info()[1]))


app = FastAPI()

# Getting data from database using this Api
@app.get("/get_data")
def get_data():
    query = ("SELECT * FROM [{}].[dbo].[{}] order by UserId ASC").format(
        database, table
    )
    data = pd.read_sql(query, conn).fillna("")
    obj = data.to_dict(orient="records")
    print("QUERY: ", query)
    return obj


# Inserting data using post request
@app.post("/post_data")
def post_data(person_data: PersonData):
    cursor = conn.cursor()
    print('checking')
    query = """
    INSERT INTO [{}].[dbo].[{}]
    (UserId, Name, CNIC, Phone, Mobile, Address,
    City, PictureUrl, Comments)
    VALUES ({}, '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}')
    """.format(
        database,
        table,
        person_data.user_id,
        person_data.name,
        person_data.cnic,
        person_data.phone,
        person_data.mobile,
        person_data.address,
        person_data.city,
        # person_data.posting_date,
        person_data.picture_url,
        person_data.comments
    )
    print("QUERY: ", query)
    print('here')
    cursor.execute(query)
    cursor.commit()
    cursor.close()

    return {
        "success": True,
    }


# Update data in database using that api
@app.post("/update_data")
def update_data(person_data: PersonData):

    cursor = conn.cursor()
    update_query = """
    UPDATE [{}].[dbo].[{}]
    SET UserId= {}, Name = '{}', CNIC= '{}', Phone = {},
    Mobile= {},  Address = '{}', City = '{}',
    PictureUrl='{}', Comments = '{}'
    WHERE UserId={};""".format(
        database,
        table,
        person_data.user_id,
        person_data.name,
        person_data.cnic,
        person_data.phone,
        person_data.mobile,
        person_data.address,
        person_data.city,
        person_data.picture_url,
        person_data.comments,
        person_data.user_id
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
    DELETE FROM [{}].[dbo].[{}]
    WHERE UserId = {};""".format(
        database, table, delete_data.user_id
    )
    print("QUERY: ", delete_query)

    cursor.execute(delete_query)
    cursor.commit()
    cursor.close()
    return ({"message": "Data delete successfully"},)
