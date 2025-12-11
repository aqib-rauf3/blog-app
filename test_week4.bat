@echo off 
echo Testing Week 4 Application... 
echo. 
echo 1. Testing health endpoint: 
curl http://localhost:5001/api/health 
echo. 
echo 2. Testing posts endpoint: 
curl http://localhost:5001/api/posts 
echo. 
echo 3. Testing registration: 
curl -X POST http://localhost:5001/api/auth/register ^ 
  -H "Content-Type: application/json" ^ 
  -d "{\"username\":\"week4user\",\"email\":\"week4@example.com\",\"password\":\"week4123\"}" 
echo. 
echo 4. Testing login: 
curl -X POST http://localhost:5001/api/auth/login ^ 
  -H "Content-Type: application/json" ^ 
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}" 
echo. 
echo 5. Checking database: 
docker exec blog_postgres psql -U bloguser -d blogdb -c "SELECT username, email FROM users;" 
echo. 
echo === Week 4 Test Complete === 
