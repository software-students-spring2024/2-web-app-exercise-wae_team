from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/classes')
def classes():
    return render_template('classes.html')

@app.route('/classDetails')
def classDetails():
    return render_template('classDetails.html')

@app.route('/addClass')
def addClass():
    return render_template('addClass.html')

@app.route('/addAssignment')
def addAssignment():
    return render_template('addAssignment.html')

if __name__ == '__main__':
    app.run(debug=True)