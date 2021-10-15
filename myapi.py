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
app_review_table = os.getenv("app_review_table")

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
    SET Name = '{}', CNIC= '{}', Phone = {},
    Mobile= {},  Address = '{}', City = '{}',
    PictureUrl='{}', Comments = '{}'
    WHERE UserId={};""".format(
        database,
        table,
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

#  CRUD for app_reviews
@app.get("/get_app_reviews")
def get_data():
    query = ("SELECT * FROM [{}].[dbo].[{}] order by UserId ASC").format(
        database, app_review_table
    )
    data = pd.read_sql(query, conn).fillna("")
    obj = data.to_dict(orient="records")
    print("QUERY: ", query)
    return obj


@app.post("/post_app_reviews")
def post_app_reviews(app_review: app_reviews):
    cursor = conn.cursor()
    print('checking')
    query_app_reviews= """
    INSERT INTO [{}].[dbo].[{}]
    (UserId, Rating, Comments)
    VALUES ({},  {}, '{}')
    """.format(
        database,
        app_review_table,
        app_review.user_id,
        app_review.rating,
        app_review.comments
    )
    print("QUERY: ", query_app_reviews)
    cursor.execute(query_app_reviews)
    cursor.commit()
    cursor.close()

    return {
        "success": True,
    }

@app.post("/update_app_review_data")
def update_data(update_app_review: app_reviews):

    cursor = conn.cursor()
    update_query = """
    UPDATE [{}].[dbo].[{}]
    SET Rating = {}, Comments = '{}'
    WHERE UserId={};""".format(
        database,
        app_review_table,
        update_app_review.rating,
        update_app_review.comments,
        update_app_review.user_id
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