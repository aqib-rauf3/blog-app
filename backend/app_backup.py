from flask import Flask, jsonify 
from flask_cors import CORS 
import os 
import psycopg2 
from psycopg2.extras import RealDictCursor 
from datetime import datetime 
 
app = Flask(__name__) 
CORS(app) 
 
def get_db_connection(): 
    conn = psycopg2.connect('postgresql://bloguser:blogpass@blog_postgres:5432/blogdb') 
    conn.autocommit = True 
    return conn 
 
@app.route('/api/health', methods=['GET']) 
def health_check(): 
    return jsonify({'status': 'healthy', 'message': 'API working!'}) 
 
@app.route('/api/posts', methods=['GET']) 
def get_posts(): 
    conn = get_db_connection() 
    cur = conn.cursor(cursor_factory=RealDictCursor) 
    cur.execute('SELECT * FROM posts ORDER BY created_at DESC;') 
    posts = cur.fetchall() 
    cur.close() 
    conn.close() 
    return jsonify({'posts': posts, 'count': len(posts)}) 
 
@app.route('/api', methods=['GET']) 
def home(): 
    return jsonify({'message': 'Blog API', 'endpoints': ['/api/health', '/api/posts']}) 
 
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5001, debug=True) 
