from flask import Flask, request, jsonify 
from flask_cors import CORS 
import psycopg2 
from psycopg2.extras import RealDictCursor 
import redis 
import json 
from datetime import datetime, timedelta 
import uuid 
import bcrypt 
import jwt 
from functools import wraps 
 
app = Flask(__name__) 
CORS(app) 
 
app.config['SECRET_KEY'] = 'week3-secret-key-change-me' 
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1) 
 
redis_client = redis.Redis(host='blog_redis', port=6379, decode_responses=True) 
 
def get_db_connection(): 
    conn = psycopg2.connect('postgresql://bloguser:blogpass@blog_postgres:5432/blogdb') 
    conn.autocommit = True 
    return conn 
 
@app.route('/api/health', methods=['GET']) 
def health_check(): 
    return jsonify({'status': 'healthy', 'message': 'API working!'}) 
 
@app.route('/api/posts', methods=['GET']) 
def get_posts(): 
    try: 
        conn = get_db_connection() 
        cur = conn.cursor(cursor_factory=RealDictCursor) 
        cur.execute('SELECT p.*, u.username as author_name FROM posts p LEFT JOIN users u ON p.author_id = u.id ORDER BY p.created_at DESC') 
        posts = cur.fetchall() 
        cur.close() 
        conn.close() 
        return jsonify({'posts': posts, 'count': len(posts), 'source': 'database'}) 
    except Exception as e: 
        return jsonify({'error': str(e), 'posts': [], 'count': 0}), 500 
 
@app.route('/api/auth/login', methods=['POST']) 
def login(): 
    return jsonify({'message': 'Login endpoint - TODO: Implement JWT'}) 
 
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5001, debug=True) 
