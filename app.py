from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import os

app = Flask(__name__)

# Connect to MongoDB (replace with your connection string)
mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://admin:admin@cluster0.s2cjg1l.mongodb.net/")
client = MongoClient(mongo_uri)
db = client.todo_db
tasks = db.tasks

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    task_list = list(tasks.find())
    return jsonify([{'task': t['task']} for t in task_list])

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task = data.get('task')
    if task:
        tasks.insert_one({'task': task})
        return jsonify({'message': 'Task added'})
    return jsonify({'error': 'No task'}), 400

if __name__ == '__main__':
    app.run(debug=True)