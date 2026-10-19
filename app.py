import os
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)

# All configuration comes from environment variables (with safe defaults).
APP_GREETING = os.environ.get("APP_GREETING", "Hello")
DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))
VISITS_FILE = DATA_DIR / "visits.txt"


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/greet")
def greet():
    name = request.args.get("name", "World")
    return jsonify(message=f"{APP_GREETING}, {name}!")


@app.get("/visits")
def visits():
    # Writes to a file so we can see what happens to data when the
    # container is removed (and how a volume keeps it).
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    count = int(VISITS_FILE.read_text()) if VISITS_FILE.exists() else 0
    count += 1
    VISITS_FILE.write_text(str(count))
    return jsonify(visits=count)


if __name__ == "__main__":
    # Local development only; in the container gunicorn runs the app.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
