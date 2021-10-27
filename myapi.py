from fastapi import FastAPI
import os
import sys
from numpy import record
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
app_insight = os.getenv("app_insights")
doc_spec = os.getenv("doc_spec")
app_attach = os.getenv("app_attachmensts")
app_pres = os.getenv("app_prescription")
app_doc_accessibility = os.getenv("app_doc_accessibility")
app_logins = os.getenv("app_logins")
app_doctors = os.getenv("app_doctor") 

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
    print("checking")
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
        person_data.comments,
    )
    print("QUERY: ", query)
    print("here")
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
        person_data.user_id,
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
    print("checking")
    query_app_reviews = """
    INSERT INTO [{}].[dbo].[{}]
    (UserId, Rating, Comments)
    VALUES ({},  {}, '{}')
    """.format(
        database,
        app_review_table,
        app_review.user_id,
        app_review.rating,
        app_review.comments,
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
        update_app_review.user_id,
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


@app.delete("/delete_app_review_data>")
def del_data(delete_review_data: del_app_review_data):

    cursor = conn.cursor()
    delete_app_review_query = """
    DELETE FROM [{}].[dbo].[{}]
    WHERE UserId = {};""".format(
        database, app_review_table, delete_review_data.user_id
    )
    print("QUERY: ", delete_app_review_query)

    cursor.execute(delete_app_review_query)
    cursor.commit()
    cursor.close()
    return ({"message": "Data delete successfully"},)


#  CRUD for app_insight table
@app.get("/get_data_app_insights")
def get_data():
    query = ("SELECT * FROM [{}].[dbo].[{}]").format(database, app_insight)
    data = pd.read_sql(query, conn).fillna("")
    obj = data.to_dict(orient="records")
    print("QUERY: ", query)
    return obj


@app.post("/post_app_insights")
def post_app_insights(app_insight_model: app_insights_model):
    cursor = conn.cursor()
    query_app_insights = """
    INSERT INTO [{}].[dbo].[{}]
    (Description, SubDescription, DocumentId)
    VALUES ('{}', '{}', {})
    """.format(
        database,
        app_insight,
        app_insight_model.description,
        app_insight_model.sub_description,
        app_insight_model.document_id,
    )
    print("QUERY: ", query_app_insights)
    cursor.execute(query_app_insights)
    cursor.commit()
    cursor.close()

    return {
        "success": True,
    }


@app.post("/update_app_insights")
def update_data(update_app_insights: app_insights_model):

    cursor = conn.cursor()
    update_query = """
    UPDATE [{}].[dbo].[{}]
    SET Description = '{}', SubDescription = '{}'
    WHERE DocumentId={};""".format(
        database,
        app_insight,
        update_app_insights.description,
        update_app_insights.sub_description,
        update_app_insights.document_id,
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

@app.delete("/delete_app_insight_data/{id}")
def del_data(id:int):

    cursor = conn.cursor()
    delete_app_insight = """
    DELETE FROM [{}].[dbo].[{}]
    WHERE DocumentId = {};""".format(
        database, app_insight, id
    )
    print("QUERY: ", delete_app_insight)

    cursor.execute(delete_app_insight)
    cursor.commit()
    cursor.close()
    return ({"message": "Data delete successfully"},)


# CRUD for doc_speciality 

@app.get('/get_data_doc_spec')
def get_doc_spec():
    query = ("SELECT * FROM [{}]. [dbo].[{}]").format(database, doc_spec)
    data = pd.read_sql(query, conn).fillna("")
    obj  = data.to_dict(orient="records")
    print("Query", query)
    return obj


# post_data for app_doc_speciality
@app.post("/post_doc_speciality")
def post_doc_spec(doc_speciality_model : app_doc_speciality):
    cursor = conn.cursor()
    query_doc_spec = """
    INSERT INTO [{}].[dbo].[{}]
    (UserId, SpecialityTag, Description)
    VALUES ({}, '{}', '{}')
    """.format(
        database,
        doc_spec,
        doc_speciality_model.user_id,
        doc_speciality_model.spec_tag,
        doc_speciality_model.description,
    )
    print("QUERY: ", query_doc_spec)
    cursor.execute(query_doc_spec)
    cursor.commit()
    cursor.close()

    return {
        "success": True,
    }


@app.post("/update_doc_spec")
def update_data(update_doc_spec: app_doc_speciality):

    cursor = conn.cursor()
    update_query = """
    UPDATE [{}].[dbo].[{}]
    SET SpecialityTag = '{}', Description = '{}'
    WHERE UserId={};""".format(
        database,
        app_insight,
        update_doc_spec.user_id,
        update_doc_spec.spec_tag,
        update_doc_spec.description,
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

@app.delete("/delete_doc_spec/{id}")
def del_data(id:int):

    cursor = conn.cursor()
    delete = """
    DELETE FROM [{}].[dbo].[{}]
    WHERE DocumentId = {};""".format(
        database, doc_spec, id
    )
    print("QUERY: ", delete)

    cursor.execute(delete)
    cursor.commit()
    cursor.close()
    return ({"message": "Data delete successfully"},)

# CRUD for app_attachments
@app.get("/get_app_attachments_data")
def get_data():
    query = ("SELECT * FROM [{}].[dbo].[{}] order by UserId ASC").format(
        database, app_attach
    )
    data = pd.read_sql(query, conn).fillna("")
    obj = data.to_dict(orient="records")
    print("QUERY: ", query)
    return obj


@app.post("/post_app_attachments")
def post_doc_spec(app_attach_model : app_attachments):
    cursor = conn.cursor()
    query_doc_spec = """
    INSERT INTO [{}].[dbo].[{}]
    (UserId, DocumentUrl, Description, Tag)
    VALUES ({}, '{}', '{}', '{}')
    """.format(
        database,
        app_attach,
        app_attach_model.user_id,
        app_attach_model.document_url,
        app_attach_model.description,
        app_attach_model.tag

    )
    print("QUERY: ", query_doc_spec)
    cursor.execute(query_doc_spec)
    cursor.commit()
    cursor.close()

    return {
        "success": True,
    }


@app.post("/update_app_attachments_data")
def update_data(update_app_attach : app_attachments):

    cursor = conn.cursor()
    update_query = """
    UPDATE [{}].[dbo].[{}]
    SET DocumentUrl = '{}', Description = '{}', Tag = '{}'
    WHERE UserId={};""".format(
        database,
        app_attach,
        update_app_attach.document_url, 
        update_app_attach.description,
        update_app_attach.tag,
        update_app_attach.user_id
        
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

@app.delete("/delete_app_attachments/{id}")
def del_data(id:int):

    cursor = conn.cursor()
    delete_app_attach = """
    DELETE FROM [{}].[dbo].[{}]
    WHERE DocumentId = {};""".format(
        database, app_attach, id
    )
    print("QUERY: ", delete_app_attach)

    cursor.execute(delete_app_attach)
    cursor.commit()
    cursor.close()
    return ({"message": "Data delete successfully"},)


# CRUD for app_prescription
@app.get('/get_data_app_prescription')
def get_doc_spec():
    query = ("SELECT * FROM [{}]. [dbo].[{}]").format(database, app_pres)
    data = pd.read_sql(query, conn).fillna("")
    obj  = data.to_dict(orient="records")
    print("Query", query)
    return obj

@app.post("/post_app_prescription")
def post_doc_spec(app_prescription : app_prescription):
    cursor = conn.cursor()
    query_doc_spec = """
    INSERT INTO [{}].[dbo].[{}]
    (UserId, DoctorId, PrescriptionDocId)
    VALUES ({}, {}, {})
    """.format(
        database,
        app_pres, 
        app_prescription.user_id,
        app_prescription.doctor_id,
        app_prescription.prescription_doc_id

    )
    print("QUERY: ", query_doc_spec)
    cursor.execute(query_doc_spec)
    cursor.commit()
    cursor.close()

    return {
        "success": True,
    }

@app.post("/update_app_prescription_data")
def update_data(update_app_presc : app_prescription):

    cursor = conn.cursor()
    update_query = """
    UPDATE [{}].[dbo].[{}]
    SET DoctorId = {}, PrescriptionDocId = {}
    WHERE UserId={};""".format(
        database,
        app_pres,
        update_app_presc.doctor_id, 
        update_app_presc.prescription_doc_id,
        update_app_presc.user_id
        
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

@app.delete("/delete_app_prescription/{id}")
def del_data(id:int):

    cursor = conn.cursor()
    delete_app_presc = """
    DELETE FROM [{}].[dbo].[{}]
    WHERE DocumentId = {};""".format(
        database, app_attach, id
    )
    print("QUERY: ", delete_app_presc)

    cursor.execute(delete_app_presc)
    cursor.commit()
    cursor.close()
    return ({"message": "Data delete successfully"},)

# CRUD for app_doctors
@app.get('/get_data_app_doctor')
def get_doc_spec():
    query = ("SELECT * FROM [{}]. [dbo].[{}]").format(database, app_doctors)
    data = pd.read_sql(query, conn).fillna("")
    obj  = data.to_dict(orient="records")
    print("Query", query)
    return obj

@app.post("/post_app_doctors")
def post_doc_spec(app_docs : app_doctor):
    cursor = conn.cursor()
    query = """
    INSERT INTO [{}].[dbo].[{}]
    (UserId, YearOfExperience, Gender, Availability)
    VALUES ({}, {}, '{}', '{}')
    """.format(
        database,
        app_doctors,
        app_docs.user_id,
        app_docs.year_of_experience,
        app_docs.gender,
        app_docs.availability

    )
    print("QUERY: ", query)
    cursor.execute(query)
    cursor.commit()
    cursor.close()

    return {
        "success": True,
    }

@app.post("/update_app_docs_data")
def update_data(update_app_docs : app_doctor):

    cursor = conn.cursor()
    update_query = """
    UPDATE [{}].[dbo].[{}]
    SET YearOfExperience = {}, Gender = '{}', Availability = '{}'
    WHERE UserId={};""".format(
        database,
        app_doctors,
        update_app_docs.year_of_experience,
        update_app_docs.gender,
        update_app_docs.availability,
        update_app_docs.user_id
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

@app.delete("/delete_app_doctors/{id}")
def del_data(id:int):

    cursor = conn.cursor()
    delete_app_presc = """
    DELETE FROM [{}].[dbo].[{}]
    WHERE DocumentId = {};""".format(
        database, app_doctors, id
    )
    print("QUERY: ", delete_app_presc)

    cursor.execute(delete_app_presc)
    cursor.commit()
    cursor.close()
    return ({"message": "Data delete successfully"},)

# CRUD for app_logins
@app.get('/get_data_app_logins')
def get_doc_spec():
    query = ("SELECT * FROM [{}]. [dbo].[{}]").format(database, app_logins)
    data = pd.read_sql(query, conn).fillna("")
    obj  = data.to_dict(orient="records")
    print("Query", query)
    return obj

@app.post("/post_app_logins")
def post_doc_spec(app_log : app_login):
    cursor = conn.cursor()
    query = """
    INSERT INTO [{}].[dbo].[{}]
    (UserId, UserName, Password)
    VALUES ({}, '{}', '{}')
    """.format(
        database,
        app_logins,
        app_log.user_id,
        app_log.user_name,
        app_log.password


    )
    print("QUERY: ", query)
    cursor.execute(query)
    cursor.commit()
    cursor.close()

    return {
        "success": True,
    }

@app.post("/update_app_logins_data")
def update_data(update_app_log : app_login):

    cursor = conn.cursor()
    update_query = """
    UPDATE [{}].[dbo].[{}]
    SET UserName = '{}', Password = '{}'
    WHERE UserId={};""".format(
        database,
        update_app_log.user_name,
        update_app_log.password,
        update_app_log.user_id
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

@app.delete("/delete_app_logins/{id}")
def del_data(id:int):

    cursor = conn.cursor()
    delete_app_presc = """
    DELETE FROM [{}].[dbo].[{}]
    WHERE DocumentId = {};""".format(
        database, app_logins, id
    )
    print("QUERY: ", delete_app_presc)

    cursor.execute(delete_app_presc)
    cursor.commit()
    cursor.close()
    return ({"message": "Data delete successfully"},)

# CRUD for app_doc_accessibility_tags
@app.get('/get_data_app_doc_accessibility_tags')
def get_doc_spec():
    query = ("SELECT * FROM [{}]. [dbo].[{}]").format(database, app_doc_accessibility)
    data = pd.read_sql(query, conn).fillna("")
    obj  = data.to_dict(orient="records")
    print("Query", query)
    return obj

@app.post("/post_app_doc_accessibility_tags")
def post_doc_spec(app_acc_tags : app_doc_accessibility_tags):
    cursor = conn.cursor()
    query = """
    INSERT INTO [{}].[dbo].[{}]
    (UserId, Tag, Comments)
    VALUES ({}, '{}', '{}')
    """.format(
        database,
        app_doc_accessibility,
        app_acc_tags.user_id,
        app_acc_tags.tag,
        app_acc_tags.comments

    )
    print("QUERY: ", query)
    cursor.execute(query)
    cursor.commit()
    cursor.close()

    return {
        "success": True,
    }

@app.post("/update_app_accessibility_tags")
def update_data(update_app_acc_tags : app_doc_accessibility_tags):

    cursor = conn.cursor()
    update_query = """
    UPDATE [{}].[dbo].[{}]
    SET Tag = '{}', Comments = '{}'
    WHERE UserId={};""".format(
        database,
        app_doc_accessibility,
        update_app_acc_tags.tag,
        update_app_acc_tags.comments,
        update_app_acc_tags.user_id
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

@app.delete("/delete_app_accessibility_tags/{id}")
def del_data(id:int):

    cursor = conn.cursor()
    delete_app_presc = """
    DELETE FROM [{}].[dbo].[{}]
    WHERE DocumentId = {};""".format(
        database, app_doc_accessibility, id
    )
    print("QUERY: ", delete_app_presc)

    cursor.execute(delete_app_presc)
    cursor.commit()
    cursor.close()
    return ({"message": "Data delete successfully"},)