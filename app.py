
#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, make_response
from markupsafe import escape
import pymongo
import datetime
from bson.objectid import ObjectId
import os
import subprocess
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

# set up the routes

@app.route('/')
def home():
    """
    Route for the home page.
    Simply returns to the browser the content of the index.html file located in the templates folder.
    """
    return render_template('index.html')


@app.route('/read')
def read():
    """
    Route for GET requests to the read page.
    Displays some information for the user with links to other pages.
    """
    docs = db.boston1.find({}).sort("created_at", -1) # sort in descending order of created_at timestamp
    return render_template('read.html', docs=docs) # render the read template


@app.route('/create')
def create():
    """
    Route for GET requests to the create page.
    Displays a form users can fill out to create a new document.
    """
    return render_template('create.html') # render the create template


@app.route('/create', methods=['POST'])
def create_post():
    """
    Route for POST requests to the create page.
    Accepts the form submission data for a new document and saves the document to the database.
    """
    name = request.form['name']
    place = request.form['place']
    address = request.form['address']

    doc = {
        # "_id": ObjectId(mongoid), 
        "name": name,
        "place": place, 
        "address": address, 
        "created_at": datetime.datetime.utcnow()
    }
    db.boston1.insert_one(doc) # insert a new document

    return redirect(url_for('read')) # tell the browser to make a request for the /read route


@app.route('/edit/<mongoid>')
def edit(mongoid):
    """
    Route for GET requests to the edit page.
    Displays a form users can fill out to edit an existing record.
    """
    doc = db.boston1.find_one({"_id": ObjectId(mongoid)})
    return render_template('edit.html', mongoid=mongoid, doc=doc) # render the edit template


@app.route('/delete/<mongoid>')
def delete(mongoid):
    """
    Route for GET requests to the delete page.
    Deletes the specified record from the database, and then redirects the browser to the read page.
    """
    db.boston1.delete_one({"_id": ObjectId(mongoid)})
    return redirect(url_for('read')) # tell the web browser to make a request for the /read route.



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
