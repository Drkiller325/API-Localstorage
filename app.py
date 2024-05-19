from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret'  # Use a secure secret in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=1)  # 1 minute expiration for demo purposes
jwt = JWTManager(app)
CORS(app)

tasks = []
users = {
    "admin": {"password": "password", "role": "ADMIN"}
}

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'VISITOR')
    if username in users:
        return jsonify({"msg": "User already exists"}), 400
    users[username] = {"password": password, "role": role}
    return jsonify({"msg": "User registered"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = users.get(username)
    if user and user["password"] == password:
        access_token = create_access_token(identity={"username": username, "role": user["role"]})
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Invalid credentials"}), 401

@app.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
@jwt_required()
def add_task():
    current_user = get_jwt_identity()
    role = current_user['role']
    if role not in ['ADMIN', 'WRITER']:
        return jsonify({"msg": "Permission denied"}), 403

    data = request.get_json()
    task = {"id": len(tasks) + 1, "name": data['name'], "completed": False}
    tasks.append(task)
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user = get_jwt_identity()
    role = current_user['role']
    if role not in ['ADMIN', 'WRITER']:
        return jsonify({"msg": "Permission denied"}), 403

    data = request.get_json()
    for task in tasks:
        if task['id'] == task_id:
            task['name'] = data.get('name', task['name'])
            task['completed'] = data.get('completed', task['completed'])
            return jsonify(task)
    return jsonify({"msg": "Task not found"}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user = get_jwt_identity()
    role = current_user['role']
    if role != 'ADMIN':
        return jsonify({"msg": "Permission denied"}), 403

    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({"msg": "Task deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
