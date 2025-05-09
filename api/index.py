from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import os
from flask.helpers import send_from_directory

app = Flask(__name__, static_folder='../static', template_folder='../templates')

# Connect to MongoDB (replace with your connection string)
mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://admin:admin@cluster0.s2cjg1l.mongodb.net/")
client = MongoClient(mongo_uri)
db = client.todo_db
tasks = db.tasks

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        task_list = list(tasks.find())
        return jsonify([{'task': t['task']} for t in task_list])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def add_task():
    try:
        data = request.get_json()
        task = data.get('task')
        if task:
            tasks.insert_one({'task': task})
            return jsonify({'message': 'Task added'})
        return jsonify({'error': 'No task'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

app.debug = True