from flask import Flask, render_template, jsonify
import psutil
import datetime

app = Flask(__name__)

def get_system_metrics():
    return {
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'cpu': psutil.cpu_percent(interval=1),
        'memory': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent
    }

@app.route('/')
def index():
    metrics = get_system_metrics()
    return render_template('index.html', metrics=metrics)

@app.route('/metrics')
def metrics():
    return jsonify(get_system_metrics())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
