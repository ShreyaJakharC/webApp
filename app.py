# USED THE CODE GIVEN MY PROFESSOR AT DOME POINT BUT IT FUNCTIONS DIFFERENTLY.
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
 
    return render_template('index.html')


@app.route('/read')
def read():
  
    docs = db.boston1.find({}).sort("created_at", -1) # sort in descending order of created_at timestamp
    return render_template('read.html', docs=docs) # render the read template


@app.route('/create')
def create():
    
    return render_template('create.html') # render the create template


@app.route('/create', methods=['POST'])
def create_post():
   
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
   
    doc = db.boston1.find_one({"_id": ObjectId(mongoid)})
    return render_template('edit.html', mongoid=mongoid, doc=doc) # render the edit template


@app.route('/delete/<mongoid>')
def delete(mongoid):
   
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
