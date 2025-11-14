import os
from flask import Flask, jsonify
import redis

app = Flask(__name__)

# --- Environment variable setup ---
MESSAGE = os.environ.get("GREETING_MESSAGE", "Hello from default config!")
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")

# --- Redis Connection ---
try:
    cache = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), decode_responses=True)
    cache.set('key', 'Database is reachable!')
except Exception as e:
    cache = None
    print(f"Could not connect to Redis: {e}")

@app.route('/')
def hello():
    # Attempt to retrieve a value from Redis
    if cache:
        redis_status = cache.get('key')
    else:
        redis_status = "Redis Not Configured/Reachable"
        
    return jsonify({
        "message": MESSAGE,
        "redis_status": redis_status,
        "hostname": os.uname()[1] # A DevOps quick check to see which container is serving
    })

if __name__ == '__main__':
    # Use 0.0.0.0 for container networking
    app.run(host='0.0.0.0', port=5000)
