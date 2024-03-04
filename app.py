from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

app = Flask(__name__)

# MongoDB configuration
print(os.environ)
print(os.getenv('MONGODB_URI'))
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
    return render_template('classes.html', classes=classes)

@app.route('/class_details/<string:class_id>')
def class_details(class_id):
    class_obj_id = ObjectId(class_id)
    class_details = class_collection.find_one({'_id': class_obj_id})
    assignments = assignment_collection.find({'class': class_details['className']})
    return render_template('classDetails.html', class_details=class_details, assignments=assignments)

@app.route('/search_classes', methods=['POST'])
def search_classes():
    if request.method == 'POST':
        search_query = request.form.get('search_class', '')
        classes = class_collection.find({'className': {'$regex': search_query, '$options': 'i'}})
        return render_template('searchedClasses.html', searched_classes=classes)

    return redirect(url_for('classes'))

@app.route('/addClass')
def addClass():
    classes = class_collection.find()
    assignments = assignment_collection.find()
    return render_template('addClass.html', classes=classes, assignments=assignments)

@app.route('/submitClass', methods=['POST'])
def submit_class():
    if request.method == 'POST':
        # Get form data
        class_name = request.form['className']
        weight_homework = request.form.get('weightHomework', type=int)
        weight_midterm = request.form.get('weightMidterm', type=int)
        weight_final = request.form.get('weightFinal', type=int)
        weight_other = request.form.get('weightOther', type=int)
        notes = request.form['notes']

        # Insert data into MongoDB Class collection
        class_data = {
            'className': class_name,
            'weightHomework': weight_homework,
            'weightMidterm': weight_midterm,
            'weightFinal': weight_final,
            'weightOther': weight_other,
            'notes': notes
        }
        class_collection.insert_one(class_data)

        # Redirect to a confirmation page or any other page
        return render_template('index.html')
    
@app.route('/update_class/<string:class_id>', methods=['POST'])
def update_class(class_id):
    if request.method == 'POST':
        # Get form data
        class_name = request.form['className']
        weight_homework = request.form.get('weightHomework', type=int)
        weight_midterm = request.form.get('weightMidterm', type=int)
        weight_final = request.form.get('weightFinal', type=int)
        weight_other = request.form.get('weightOther', type=int)
        notes = request.form['notes']

        # Update data in MongoDB Class collection
        class_collection.update_one(
            {'_id': ObjectId(class_id)},
            {
                '$set': {
                    'className': class_name,
                    'weightHomework': weight_homework,
                    'weightMidterm': weight_midterm,
                    'weightFinal': weight_final,
                    'weightOther': weight_other,
                    'notes': notes
                }
            }
        )

        # Redirect to the class details page after updating
        return redirect(url_for('class_details', class_id=class_id))

@app.route('/delete_class/<string:class_id>', methods=['POST'])
def delete_class(class_id):
    result = class_collection.delete_one({'_id': ObjectId(class_id)})
    return redirect(url_for('index'))

@app.route('/addAssignment')
def addAssignment():
    classes = class_collection.find()
    assignments = assignment_collection.find()
    return render_template('addAssignment.html', classes=classes, assignments=assignments)

@app.route('/submitAssignment', methods=['POST'])
def submit_assignment():
    if request.method == 'POST':
        assignment_name = request.form['assignmentName']
        class_name = request.form['class']
        assignment_type = request.form['assignmentType']
        status = request.form['status']
        due_date = request.form['dueDate']
        reminder_date = request.form['reminderDate']
        weight = request.form.get('weight', type=int)
        notes = request.form['notes']

        assignment_data = {
            'assignmentName': assignment_name,
            'class': class_name,
            'assignmentType': assignment_type,
            'status': status,
            'due': due_date,
            'reminder': reminder_date,
            'weight': weight,
            'notes': notes
        }
        assignment_collection.insert_one(assignment_data)

        return render_template('index.html')
    
@app.route('/search_assignments', methods=['POST'])
def search_assignments():
    if request.method == 'POST':
        search_query = request.form.get('search_assignment', '')
        searched_assignments = assignment_collection.find({'assignmentName': {'$regex': search_query, '$options': 'i'}})
        
        return render_template('searchedAssignments.html', searched_assignments=searched_assignments)

    return redirect(url_for('classes'))
    
@app.route('/assignment_details/<string:assignment_id>')
def assignment_details(assignment_id):
    assignment_obj_id = ObjectId(assignment_id)
    assignment_details = assignment_collection.find_one({'_id': assignment_obj_id})
    return render_template('assignmentDetails.html', assignment_details=assignment_details)

@app.route('/update_assignment/<string:assignment_id>', methods=['POST'])
def update_assignment(assignment_id):
    if request.method == 'POST':
        # Get form data
        assignment_name = request.form['assignmentName']
        class_name = request.form['class']
        assignment_type = request.form['assignmentType']
        status = request.form['status']
        due_date = request.form['dueDate']
        reminder_date = request.form['reminderDate']
        weight = request.form['weight']
        notes = request.form['notes']

        # Update data in MongoDB Assignment collection
        assignment_collection.update_one(
            {'_id': ObjectId(assignment_id)},
            {
                '$set': {
                    'assignmentName': assignment_name,
                    'class': class_name,
                    'assignmentType': assignment_type,
                    'status': status,
                    'due': due_date,
                    'reminder': reminder_date,
                    'weight': weight,
                    'notes': notes
                }
            }
        )

        # Redirect to the assignment details page after updating
        return redirect(url_for('assignment_details', assignment_id=assignment_id))

@app.route('/delete_assignment/<string:assignment_id>', methods=['POST'])
def delete_assignment(assignment_id):
    result = assignment_collection.delete_one({'_id': ObjectId(assignment_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)