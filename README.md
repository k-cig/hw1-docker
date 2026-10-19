# HW-1: Containerized Flask app

1. Build: `docker build -t hw1-app:1.0 .`
2. Run: `docker run -d --name hw1 -p 8000:8000 -e APP_GREETING=Merhaba -v hw1-data:/data hw1-app:1.0`
3. Test: `curl http://localhost:8000/health` · `curl "http://localhost:8000/greet?name=Kemal"` · `curl http://localhost:8000/visits`
4. Stop and remove: `docker rm -f hw1` (the `hw1-data` volume keeps the visit count)
