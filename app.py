from flask import Flask, render_template
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# MongoDB configuration
client = MongoClient(os.getenv('MONGODB_URI'))
db = client.get_default_database()  # Get default database from the connection string
class_collection = db['Class']
assignment_collection = db['Assignment']

@app.route('/')
def index():
    # Retrieve data from MongoDB collections
    classes = class_collection.find()
    assignments = assignment_collection.find()
    
    # Pass data to the template for rendering
    return render_template('index.html', classes=classes, assignments=assignments)

@app.route('/calendar')
def calendar():
    classes = class_collection.find()
    assignments = assignment_collection.find()
    return render_template('calendar.html', classes=classes, assignments=assignments)

@app.route('/classes')
def classes():
    classes = class_collection.find()
    assignments = assignment_collection.find()
    return render_template('classes.html', classes=classes, assignments=assignments)

@app.route('/classDetails')
def classDetails():
    classes = class_collection.find()
    assignments = assignment_collection.find()
    return render_template('classDetails.html', classes=classes, assignments=assignments)

@app.route('/addClass')
def addClass():
    classes = class_collection.find()
    assignments = assignment_collection.find()
    return render_template('addClass.html', classes=classes, assignments=assignments)

@app.route('/addAssignment')
def addAssignment():
    classes = class_collection.find()
    assignments = assignment_collection.find()
    return render_template('addAssignment.html', classes=classes, assignments=assignments)

if __name__ == '__main__':
    app.run(debug=True)