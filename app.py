#!/usr/bin/env python3

from collections import UserString
from flask import Flask, render_template, request, redirect, url_for, make_response
from markupsafe import escape
import pymongo
import datetime
from bson.objectid import ObjectId
import os
import subprocess
#import bcrypt

# instantiate the app
app = Flask(__name__)



# load credentials and configuration options from .env file
# if you do not yet have a file named .env, make one based on the template in env.example
import credentials
config = credentials.get()

# turn on debugging if in development mode
if config['FLASK_ENV'] == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode

# make one persistent connection to the database
connection = pymongo.MongoClient(config['MONGO_HOST'], 27017, 
                                username=config['MONGO_USER'],
                                password=config['MONGO_PASSWORD'],
                                authSource=config['MONGO_DBNAME'])
db = connection[config['MONGO_DBNAME']] # store a reference to the database
db1 = connection[config['MONGO_DBNAME']] # store a reference to the database

'''
url = "mongodb+srv://sc8941:<Happyuion>@databasewebapp.h90wse9.mongodb.net/?retryWrites=true&w=majority"
connection = pymongo.MongoClient(url)
db = connection[config['sc8941']]
'''


# set up the routes
@app.route('/')
def home():
    """
    Route for the home page
    """
    return render_template('index.html')

# @app.route('/boston')
# def boston():
#     """
#     Route for GET requests to the create page.
#     Displays a form users can fill out to create a new document.
#     """
#     return render_template('boston.html') # render the create template

# @app.route('/boston', methods=['POST'])
# def vac_boston ():
#     place = request.form['placeb']
#     address = request.form['addressb']
#     # create a new document with the data the user entered
#     doc = {
#         # "_id": ObjectId(mongoid), 
#         "place": place, 
#         "address": address, 
#     }
#     db.boston.insert_one(doc) # insert a new document

#     return redirect(url_for('home'))


@app.route('/create')
def create():
    """
    Route for GET requests to the create page.
    Displays a form users can fill out to create a new document.
    """
    return render_template('create.html') # render the create template

@app.route('/boston/create', methods=['POST'])
def create_post():
    """
    Route for POST requests to the create page.
    Accepts the form submission data for a new document and saves the document to the database.
    """
    place = request.form['placeb']
    address = request.form['addressb']
    # create a new document with the data the user entered
    doc = {
        # "_id": ObjectId(mongoid), 
        "place": place, 
        "address": address, 
    }
    db.boston.insert_one(doc) # insert a new document

    return redirect(url_for('create')) # tell the browser to make a request for the /read route


@app.route('/edit/<mongoid>')
def edit(mongoid):
    """
    Route for GET requests to the edit page.
    Displays a form users can fill out to edit an existing record.
    """
    doc = db.boston.find_one({"_id": ObjectId(mongoid)})
    return render_template('edit.html', mongoid=mongoid, doc=doc) # render the edit template


@app.route('/edit/<mongoid>', methods=['POST'])
def edit_post(mongoid):
    """
    Route for POST requests to the edit page.
    Accepts the form submission data for the specified document and updates the document in the database.
    """
    place = request.form['placeb']
    address = request.form['addressb']
    # create a new document with the data the user entered
    doc = {
        # "_id": ObjectId(mongoid), 
        "place": place, 
        "address": address, 
        "created_at": datetime.datetime.utcnow()
    }
    db.boston.insert_one(doc) # insert a new document 


    db.boston.update_one(
        {"_id": ObjectId(mongoid)}, # match criteria
        { "$set": doc }
    )

    return redirect(url_for('create')) # tell the browser to make a request for the /read route


@app.route('/delete/<mongoid>')
def delete(mongoid):
    """
    Route for GET requests to the delete page.
    Deletes the specified record from the database, and then redirects the browser to the read page.
    """
    db.boston.delete_one({"_id": ObjectId(mongoid)})
    return redirect(url_for('create')) # tell the web browser to make a request for the /read route.






@app.route('/read')
def read():
    """
    Route for GET requests to the read page.
    Displays some information for the user with links to other pages.
    """
    docs = db.boston.find({}).sort("created_at", -1) # sort in descending order of created_at timestamp
    return render_template('read.html', docs=docs) # render the read template



# @app.route('/signin')
# def signin():
#     """
#     Route for GET requests to the create page.
#     Displays a form users can fill out to create a new document.
#     """
#     return render_template('signin.html') # render the create template

# @app.route('/signin', methods=['POST'])
# def create_signin():
#     """
#     Route for POST requests to the create page.
#     Accepts the form submission data for a new document and saves the document to the database.
#     """
    
#     email1 = request.form['semail']
#     password = request.form['sloginpassword']
    
#     user = db.info.find_one({'username': email1})

#     if user:
#         '''
#         if bcrypt.hashpw(password.encode("utf-8"), user["password"].encode("utf-8")) == user["password"].encode("utf-8"):
#         # Redirect to the home page
#         '''
#         return redirect(url_for('home'))
#     else:
#         # Show an error message
#         return render_template('create.html', error='Invalid email or password')


# @app.route('/login')
# def login():
#     """
#     Route for GET requests to the create page.
#     Displays a form users can fill out to create a new document.
#     """
#     return render_template('login.html') # render the create template


# @app.route('/login', methods=['POST'])
# def create_login():
#     """
#     Route for POST requests to the create page.
#     Accepts the form submission data for a new document and saves the document to the database.
#     """
#     email = request.form['femail']
#     password = request.form['floginpassword']
#     # create a new document with the data the user entered
#     users = {
#         # "_id": ObjectId(mongoid), 
#         "email": email, 
#         "password": password, 
#     }
#     db.info.insert_one(users) # insert a new document
#     return redirect(url_for('home')) # tell the browser to make a request for the /read route



# @app.route('/create')
# def create():
#     """
#     Route for GET requests to the create page.
#     Displays a form users can fill out to create a new document.
#     """
#     return render_template('create.html') # render the create template

# @app.route('/create', methods=['POST'])
# def create_post():
#     """
#     Route for POST requests to the create page.
#     Accepts the form submission data for a new document and saves the document to the database.
#     """
#     username = request.form["fusername"]
#     name = request.form['fapplication']
#     message = request.form['fmessage']

#     # create a new document with the data the user entered
#     doc = {
#         "username": username,
#         "name": name,
#         "message": message, 
#         "created_at": datetime.datetime.utcnow()
#     }
    
#     db.exampleapp.insert_one(doc) # insert a new document

#     return redirect(url_for('read')) # tell the browser to make a request for the /read route


# @app.route('/edit/<mongoid>')
# def edit(mongoid):
#     """
#     Route for GET requests to the edit page.
#     Displays a form users can fill out to edit an existing record.
#     """
#     doc = db.exampleapp.find_one({"_id": ObjectId(mongoid)})
#     return render_template('edit.html', mongoid=mongoid, doc=doc) # render the edit template


# @app.route('/edit/<mongoid>', methods=['POST'])
# def edit_post(mongoid):
#     """
#     Route for POST requests to the edit page.
#     Accepts the form submission data for the specified document and updates the document in the database.
#     """
#     username = request.form["fusername"]
#     name = request.form['fapplication']
#     message = request.form['fmessage']
    

#     doc = {
#         # "_id": ObjectId(mongoid), 
#         "username": username,
#         "name": name, 
#         "message": message, 
#         "created_at": datetime.datetime.utcnow()
#     }

#     db.exampleapp.update_one(
#         {"_id": ObjectId(mongoid)}, # match criteria
#         { "$set": doc }
#     )

#     return redirect(url_for('read')) # tell the browser to make a request for the /read route


# @app.route('/delete/<mongoid>')
# def delete(mongoid):
#     """
#     Route for GET requests to the delete page.
#     Deletes the specified record from the database, and then redirects the browser to the read page.
#     """
#     db.exampleapp.delete_one({"_id": ObjectId(mongoid)})
#     return redirect(url_for('read')) # tell the web browser to make a request for the /read route.




@app.errorhandler(Exception)
def handle_error(e):
    """
    Output any errors - good for debugging.
    """
    return render_template('error.html', error=e) # render the edit template


if __name__ == "__main__":
    #import logging

    #logging.basicConfig(filename='/home/ak8257/error.log',level=logging.DEBUG)
    app.run(debug = True)
