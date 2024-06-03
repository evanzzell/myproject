import logging
import os

from flask import Flask, jsonify, redirect, render_template, request, url_for
from pymongo import MongoClient

app = Flask(__name__) 
logging.basicConfig(filename='app.log', level=logging.DEBUG)

mongo_host = os.getenv('MONGO_HOST', 'mongodb')
mongo_port = int(os.getenv('MONGO_PORT', 27017))
mongo_username = os.getenv('MONGO_USERNAME', 'root')
mongo_password = os.getenv('MONGO_PASSWORD', 'pass')
mongo_auth_source = os.getenv('MONGO_AUTH_SOURCE', 'admin')
mongo_db_name = os.getenv('MONGO_DB_NAME', 'mytododb')

client = MongoClient(host=mongo_host, port=mongo_port, 
                    username=mongo_username, password=mongo_password, 
                    authSource=mongo_auth_source)
db = client[mongo_db_name]
students_collection = db.students


@app.route('/') 
def home(): 
    logging.info('Home page accessed')
    students = students_collection.find() 
    return render_template('index.html', students=students) 

@app.route('/add_student', methods=['POST']) 
def add_student(): 
    if request.method == 'POST': 
        logging.info('Student added')
        student_data = { 
            'name': request.form['name'], 
            'roll_number': request.form['roll_number'], 
            'grade': request.form['grade'] 
        } 
        students_collection.insert_one(student_data) 
    return redirect(url_for('home'))  

@app.route('/api/students/<roll_number>', methods=['GET'])
def get_student(roll_number):
    student = students_collection.find_one({'roll_number': str(roll_number)})
    if student:
        logging.info('Student page accessed')
        return render_template('student.html', student=student)
    else:
        return 'Student not found'

@app.route('/api/students', methods=['GET'])
def get_students():
    logging.info('Students list page accessed')
    students = students_collection.find()
    student_list = []
    for student in students:
        student_list.append({
            'name': student['name'],
            'roll_number': student['roll_number'],
            'grade': student['grade']
        })
    return jsonify(student_list)

@app.route('/api/students', methods=['POST'])
def add_student_api():
    data = request.json
    if 'name' in data and 'roll_number' in data and 'grade' in data:
        students_collection.insert_one(data)
        return jsonify({'message': 'Student added successfully'}), 201
    else:
        return jsonify({'message': 'Missing required fields'}), 400

if __name__ == '__main__': 
	app.run(host='0.0.0.0', debug=True) 
