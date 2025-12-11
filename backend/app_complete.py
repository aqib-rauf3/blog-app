from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import redis
import json
from datetime import datetime, timedelta
import bcrypt
import jwt
from functools import wraps

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'devweek4-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Redis connection
redis_client = redis.Redis(host='blog_redis', port=6379, decode_responses=True)

# Database connection
def get_db_connection():
    conn = psycopg2.connect('postgresql://bloguser:blogpass@blog_postgres:5432/blogdb')
    conn.autocommit = True
    return conn

# JWT Token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Bearer token malformed'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Decode token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user_id, *args, **kwargs)
    
    return decorated

# Health endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'API working!',
        'version': '4.0',
        'timestamp': datetime.utcnow().isoformat()
    })

# User Registration
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Validation
    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if user exists
        cur.execute('SELECT id FROM users WHERE username = %s OR email = %s', (username, email))
        if cur.fetchone():
            return jsonify({'error': 'Username or email already exists'}), 409
        
        # Create user
        cur.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING id',
            (username, email, hashed_password)
        )
        user_id = cur.fetchone()[0]
        
        # Generate JWT token
        token_payload = {
            'user_id': str(user_id),
            'username': username,
            'exp': datetime.utcnow() + app.config['JWT_ACCESS_TOKEN_EXPIRES']
        }
        token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')
        
        cur.close()
        conn.close()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': str(user_id),
                'username': username,
                'email': email
            },
            'token': token
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# User Login
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Find user by username or email
        cur.execute(
            'SELECT id, username, email, password_hash FROM users WHERE username = %s OR email = %s',
            (username, username)
        )
        user = cur.fetchone()
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Verify password
        if bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            # Generate JWT token
            token_payload = {
                'user_id': str(user[0]),
                'username': user[1],
                'exp': datetime.utcnow() + app.config['JWT_ACCESS_TOKEN_EXPIRES']
            }
            token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')
            
            cur.close()
            conn.close()
            
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'id': str(user[0]),
                    'username': user[1],
                    'email': user[2]
                },
                'token': token
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get current user profile
@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user(current_user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            'SELECT id, username, email, created_at FROM users WHERE id = %s',
            (current_user_id,)
        )
        user = cur.fetchone()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        cur.close()
        conn.close()
        
        return jsonify({
            'user': {
                'id': str(user[0]),
                'username': user[1],
                'email': user[2],
                'created_at': user[3]
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get all posts (public)
@app.route('/api/posts', methods=['GET'])
def get_posts():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute('''
            SELECT p.*, u.username as author_name
            FROM posts p
            LEFT JOIN users u ON p.author_id = u.id
            ORDER BY p.created_at DESC
        ''')
        posts = cur.fetchall()
        
        # Convert to list of dicts
        posts_list = []
        for post in posts:
            post_dict = dict(post)
            # Convert UUID to string if needed
            for key in ['id', 'author_id']:
                if key in post_dict and post_dict[key]:
                    post_dict[key] = str(post_dict[key])
            posts_list.append(post_dict)
        
        cur.close()
        conn.close()
        
        return jsonify({
            'posts': posts_list,
            'count': len(posts_list),
            'source': 'database'
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'posts': [], 'count': 0}), 500

# Create new post (protected)
@app.route('/api/posts', methods=['POST'])
@token_required
def create_post(current_user_id):
    data = request.get_json()
    
    title = data.get('title')
    content = data.get('content')
    
    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            'INSERT INTO posts (title, content, author_id) VALUES (%s, %s, %s) RETURNING id',
            (title, content, current_user_id)
        )
        post_id = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        return jsonify({
            'message': 'Post created successfully',
            'post_id': str(post_id)
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Database info endpoint
@app.route('/api/db-info', methods=['GET'])
def get_db_info():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get table names
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = [row[0] for row in cur.fetchall()]
        
        # Get counts
        cur.execute('SELECT COUNT(*) FROM posts')
        post_count = cur.fetchone()[0]
        
        cur.execute('SELECT COUNT(*) FROM users')
        user_count = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        return jsonify({
            'database': 'blogdb',
            'tables': tables,
            'post_count': post_count,
            'user_count': user_count
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)