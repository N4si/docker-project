from flask import Flask, render_template, jsonify
import psutil
import datetime
import redis
import os
import ast  # Safer than eval()

app = Flask(__name__)

# Get Redis host & port from environment variables (use defaults for local)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Connect to Redis
try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    redis_client.ping()  # Test connection
except redis.exceptions.ConnectionError:
    print("⚠️ Warning: Redis is not running! The app will work, but metrics won't be saved.")
    redis_client = None  # Handle case when Redis is unavailable

def get_system_metrics():
    metrics = {
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'cpu': psutil.cpu_percent(interval=1),
        'memory': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent
    }

    # Store in Redis (keep only last 5 metrics)
    if redis_client:
        redis_client.lpush("metrics", str(metrics))
        redis_client.ltrim("metrics", 0, 4)

    return metrics

@app.route('/')
def index():
    if redis_client:
        metrics_list = redis_client.lrange("metrics", 0, -1)
        metrics = [ast.literal_eval(m) for m in metrics_list]  # Safer conversion
    else:
        metrics = []
    return render_template('index.html', metrics=metrics)

@app.route('/metrics')
def metrics():
    return jsonify(get_system_metrics())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
