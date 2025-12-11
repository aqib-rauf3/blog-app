CREATE TABLE IF NOT EXISTS users ( 
    id SERIAL PRIMARY KEY, 
    username VARCHAR(80) UNIQUE NOT NULL, 
    email VARCHAR(120) UNIQUE NOT NULL, 
    password_hash VARCHAR(200) NOT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
); 
 
CREATE TABLE IF NOT EXISTS posts ( 
    id SERIAL PRIMARY KEY, 
    title VARCHAR(200) NOT NULL, 
    content TEXT NOT NULL, 
    author_id INTEGER REFERENCES users(id), 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
); 
 
-- Insert admin user (password: admin123) 
INSERT INTO users (username, email, password_hash) VALUES 
('admin', 'admin@example.com', '\$2b\$12\$VjvPSOxQ7l1BQMXZk4wDVOJqS6sT4tFF8B7cUYnVtL6yK8pW6tFkK') 
ON CONFLICT (username) DO NOTHING; 
 
-- Insert sample posts with author_id 1 (admin) 
INSERT INTO posts (title, content, author_id) VALUES 
('Welcome to the Blog', 'This is our first blog post!', 1), 
('Docker is Awesome', 'Containers make deployment easy!', 1), 
('PostgreSQL Rocks', 'Relational databases are powerful.', 1) 
ON CONFLICT DO NOTHING; 
