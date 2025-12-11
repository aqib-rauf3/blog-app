from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Simple in-memory storage for testing
users_db = {"admin": {"password": "admin123", "email": "admin@example.com"}}
posts_db = [
    {"id": 1, "title": "Welcome to the Blog", "author_name": "admin", "content": "Welcome to our blog!"},
    {"id": 2, "title": "Docker is Awesome", "author_name": "admin", "content": "Docker makes deployment easy."},
    {"id": 3, "title": "PostgreSQL Rocks", "author_name": "admin", "content": "PostgreSQL is a great database."}
]

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "message": "Week 4 API working!",
        "version": "4.0",
        "status": "healthy"
    })

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify({
        "count": len(posts_db),
        "source": "in-memory",
        "posts": posts_db
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in users_db and users_db[username]['password'] == password:
        return jsonify({
            "success": True,
            "message": "Login successful",
            "token": "dummy-jwt-token-for-testing",
            "user": {
                "username": username,
                "email": users_db[username]['email']
            }
        })
    
    return jsonify({
        "success": False,
        "message": "Invalid credentials"
    }), 401

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if username in users_db:
        return jsonify({
            "success": False,
            "message": "User already exists"
        }), 400
    
    users_db[username] = {"password": password, "email": email}
    
    return jsonify({
        "success": True,
        "message": "Registration successful",
        "user": {
            "username": username,
            "email": email
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
