@echo off 
echo ===== WEEK 4 FINAL VERIFICATION ===== 
echo. 
echo 1. Health Check: 
curl http://localhost:5001/api/health 
echo. 
echo 2. List Posts: 
curl http://localhost:5001/api/posts 
echo. 
echo 3. Test Admin Login: 
curl -X POST http://localhost:5001/api/auth/login -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"admin123\"}" 
echo. 
echo 4. Database State: 
docker exec blog_postgres psql -U bloguser -d blogdb -c "SELECT id, username, email FROM users ORDER BY id;" 
echo. 
echo 5. Posts with Authors: 
docker exec blog_postgres psql -U bloguser -d blogdb -c "SELECT p.id, p.title, u.username FROM posts p LEFT JOIN users u ON p.author_id = u.id;" 
echo. 
echo === FRONTEND: http://localhost:8081 === 
echo === BACKEND: http://localhost:5001 === 
echo ===== WEEK 4 COMPLETE! ===== 
