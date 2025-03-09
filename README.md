# docker-project
# Docker Productivity Toolkit - README

## 🚀 Overview
This project demonstrates how to efficiently use **Docker** to boost productivity when developing, testing, and deploying a **Flask application with Redis**. It showcases various **Docker tools** like:

- **Docker Desktop** (GUI for managing containers)
- **Docker Compose** (Multi-container orchestration)
- **Docker Compose Watch** (Live code reloading)
- **Docker Scout** (Security scanning)
- **Docker Build Cloud** (Faster builds)
- **Testcontainers** (Automated testing in isolated environments)

## 📌 Prerequisites
- Install **[Docker Desktop](https://www.docker.com/products/docker-desktop/)**
- Install **Python 3.9+**
- Install **Redis** (Optional, since it will run inside a container)
- Install **pytest** (for running automated tests)

## 📂 Project Structure
```
.
├── app.py                  # Flask application
|__ templates               # html file
├── Dockerfile              # Docker instructions to build image
├── docker-compose.yml      # Multi-container setup
├── .dockerignore           # Ignore unnecessary files
├── requirements.txt        # Python dependencies
├── test_app.py             # Testcases using Testcontainers
└── README.md               # Documentation
```

---

## ⚙️ Step 1: Run the Application Locally

```bash
git clone https://github.com/N4si/docker-project.git
cd docker-project
pip3 install -r requirements.txt
python3 app.py  # Run Flask app on localhost:5001
```

Check the application at **http://localhost:5001**.

Test Redis connection:
```bash
redis-cli
KEYS *
LRANGE metrics 0 -1
```

---

## 🐳 Step 2: Containerize with Docker

### 1️⃣ Create a `Dockerfile`
```dockerfile
# Use the official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir flask psutil redis

# Expose the port
EXPOSE 5001

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001", "--debug"]
```

### 2️⃣ Build & Run the Docker Container
```bash
docker build -t flask-monitor .
docker run -p 5001:5001 flask-monitor
```

---

## 🛠️ Step 3: Use Docker Compose for Multi-Container Setup

### 1️⃣ Create `docker-compose.yml`
```yaml

services:
  web:
    build: .
    ports:
      - "5001:5001"
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - FLASK_APP=app.py
      - FLASK_ENV=development
      - FLASK_RUN_HOST=0.0.0.0
      - FLASK_RUN_PORT=5001
    depends_on:
      - redis
    develop:
      watch:
        - action: sync
          path: .
          target: /app
    command: flask run

  redis:
    image: "redis:latest"
    ports:
      - "6379:6379"
```

### 2️⃣ Run the Services
```bash
docker compose up -d
```

### 3️⃣ Stop & Remove Containers
```bash
docker compose down
```

---

## 🔄 Step 4: Enable Live Code Reloading with Docker Compose Watch
```bash
docker compose watch
```

This will sync code changes automatically without rebuilding the container!

---

## 🔎 Step 5: Scan for Security Vulnerabilities with Docker Scout
```bash
docker scout quickview flask-monitor
docker scout cves flask-monitor
```

Use `docker scout` to get security insights and remediation steps!

---

## 🚀 Step 6: Optimize Build Performance with Docker Build Cloud
```bash
docker buildx version
docker buildx create --name mybuilder --use
docker buildx bake --progress=plain
```

Faster builds by caching and running parallel builds.

---

## 🧪 Step 7: Automate Testing with Testcontainers

### 1️⃣ Install Testcontainers
```bash
pip3 install pytest testcontainers
```

### 2️⃣ Create `test_app.py`
```python
import pytest
import redis
import os
from testcontainers.redis import RedisContainer
from app import app

@pytest.fixture(scope="module")
def redis_container():
    with RedisContainer() as redis_container:
        redis_host = redis_container.get_container_host_ip()
        redis_port = redis_container.get_exposed_port(6379)
        os.environ["REDIS_HOST"] = redis_host
        os.environ["REDIS_PORT"] = str(redis_port)
        yield redis_host, redis_port

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_redis_connection(redis_container):
    redis_host, redis_port = redis_container
    r = redis.Redis(host=redis_host, port=int(redis_port), decode_responses=True)
    r.set("test_key", "Hello, Redis!")
    assert r.get("test_key") == "Hello, Redis!"

def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.get_json()
    assert "cpu" in data
    assert "memory" in data
    assert "disk" in data
```

### 3️⃣ Run Tests
```bash
python3 -m pytest test_app.py
```

---

## 🎯 Summary: Key Commands
| Feature                | Command |
|------------------------|---------|
| **Build Image**        | `docker build -t flask-monitor .` |
| **Run Container**      | `docker run -p 5001:5001 flask-monitor` |
| **Start Services**     | `docker compose up -d` |
| **Stop Services**      | `docker compose down` |
| **Live Reload**        | `docker compose watch` |
| **Security Scan**      | `docker scout quickview flask-monitor` |
| **Faster Build**       | `docker buildx bake --progress=plain` |
| **Run Tests**          | `pytest test_app.py` |

---

## 🏆 Conclusion

By using these **Docker tools**, you can:
- **Develop faster** with Docker Compose Watch 🔄
- **Ensure security** with Docker Scout 🔍
- **Optimize builds** using Docker Build Cloud 🚀
- **Automate testing** with Testcontainers ✅

🚀 Now, you're ready to **boost your productivity** with Docker!

---

💡 **Feel free to contribute & star ⭐ the repo!**

