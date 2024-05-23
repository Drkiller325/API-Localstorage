from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from flasgger import Swagger, swag_from

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret'  # Use a secure secret in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=1)  # 1 minute expiration for demo purposes
jwt = JWTManager(app)
CORS(app)

swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Task Manager API",
        "description": "API documentation for the Task Manager app",
        "version": "1.0.0"
    },
    "host": "localhost:5000",
    "schemes": [
        "http"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
})

tasks = []
users = {
    "admin": {"password": "password", "role": "ADMIN"},
    "visitor": {"password": "visit", "role": "VISITOR"}
}

@app.route('/api/register', methods=['POST'])
@swag_from({
    'tags': ['User Management'],
    'description': 'Register a new user',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'},
                    'role': {'type': 'string'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        201: {'description': 'User registered'},
        400: {'description': 'User already exists'}
    }
})
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
@swag_from({
    'tags': ['User Management'],
    'description': 'Login a user and get a JWT token',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        200: {'description': 'Successful login, returns access token'},
        401: {'description': 'Invalid credentials'}
    }
})
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
@swag_from({
    'tags': ['Task Management'],
    'description': 'Get list of tasks',
    'responses': {
        200: {'description': 'List of tasks'}
    }
})
def get_tasks():
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Task Management'],
    'description': 'Add a new task',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'category': {'type': 'string'}
                },
                'required': ['name', 'category']
            }
        }
    ],
    'responses': {
        201: {'description': 'Task created'},
        400: {'description': 'Task name and category are required'},
        403: {'description': 'Permission denied'}
    }
})
def add_task():
    current_user = get_jwt_identity()
    role = current_user['role']
    if role not in ['ADMIN', 'WRITER']:
        return jsonify({"msg": "Permission denied"}), 403

    data = request.get_json()
    task_name = data.get('name')
    task_category = data.get('category')  # New: Get category from request
    if not task_name or not task_category:
        return jsonify({"msg": "Task name and category are required"}), 400

    task = {"id": len(tasks) + 1, "name": task_name, "category": task_category, "completed": False}
    tasks.append(task)
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['Task Management'],
    'description': 'Update a task',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'required': True,
            'type': 'string',
            'description': 'JWT token'
        },
        {
            'name': 'task_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID of the task to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'category': {'type': 'string'},
                    'completed': {'type': 'boolean'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Task updated'},
        404: {'description': 'Task not found'},
        403: {'description': 'Permission denied'}
    },
    'security': [{'Bearer': []}]
})
def update_task(task_id):
    current_user = get_jwt_identity()
    role = current_user['role']
    if role not in ['ADMIN', 'WRITER']:
        return jsonify({"msg": "Permission denied"}), 403

    data = request.get_json()
    for task in tasks:
        if task['id'] == task_id:
            task['name'] = data.get('name', task['name'])
            task['category'] = data.get('category', task['category'])
            task['completed'] = data.get('completed', task['completed'])
            return jsonify(task)
    return jsonify({"msg": "Task not found"}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'tags': ['Task Management'],
    'description': 'Delete a task',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'required': True,
            'type': 'string',
            'description': 'JWT token'
        },
        {
            'name': 'task_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID of the task to delete'
        }
    ],
    'responses': {
        200: {'description': 'Task deleted'},
        404: {'description': 'Task not found'},
        403: {'description': 'Permission denied'}
    },
    'security': [{'Bearer': []}]
})
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
