# Dockerized Flask Load Balancer

A practical implementation of a **Flask-based application load balancer** using **Docker**.

In this project, I created a Flask application that works as a load balancer and distributes incoming requests among multiple backend application instances running in separate Docker containers.

The load balancer monitors the **CPU and memory utilization** of the available backend servers and forwards the incoming request to the backend server with the lowest calculated load.

---

## 📌 Project Overview

The purpose of this project was to gain practical experience with:

* Flask REST APIs
* Docker and Docker containers
* Running multiple instances of an application
* Application-level load balancing
* Backend server monitoring
* HTTP request forwarding
* Docker networking
* CPU and memory utilization monitoring

Instead of sending every request to a single backend server, the load balancer dynamically selects one of the available backend instances.

---

## 🏗️ Project Structure

```text
Load_Balancer_application/
│
├── app/
│   └── api/
│       ├── api.py
│       └── load_balancer.py
│
└── Load_Balancer/
    ├── app.py
    ├── docker-compose.yml
    ├── Dockerfile
    ├── requirements.txt
    │
    └── routes/
        ├── __init__.py
        └── main.py
```

### File Responsibilities

| File                       | Purpose                                         |
| -------------------------- | ----------------------------------------------- |
| `app.py`                   | Main Flask application entry point              |
| `routes/main.py`           | Flask routes and load-balancer request handling |
| `routes/__init__.py`       | Routes package initialization                   |
| `app/api/api.py`           | Backend API implementation                      |
| `app/api/load_balancer.py` | Load-balancing related functionality            |
| `Dockerfile`               | Defines the Docker image for the application    |
| `docker-compose.yml`       | Defines and runs the containerized services     |
| `requirements.txt`         | Python dependencies                             |

---

# 🏛️ Architecture

The application consists of a **load-balancer service** and multiple backend application instances.

```text
                         Client
                           |
                           |
                    GET /products
                           |
                           v
              +------------------------+
              |    Flask Load Balancer |
              +------------------------+
                           |
                  Check backend load
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
       +-----------+ +-----------+ +-----------+
       | Backend 1 | | Backend 2 | | Backend 3 |
       |   :5001   | |   :5002   | |   :5003   |
       +-----------+ +-----------+ +-----------+
             |             |             |
             +-------------+-------------+
                           |
                    Docker Network
```

The backend application is replicated into **three separate instances**.

```text
Backend 1 → Port 5001
Backend 2 → Port 5002
Backend 3 → Port 5003
```

The load balancer communicates with these backend instances and decides where the request should be sent.

---

# ⚖️ Load Balancing Strategy

This project uses a simple **resource-based load balancing strategy**.

The load balancer maintains the available backend servers:

```python
servers = [
    "http://localhost:5001",
    "http://localhost:5002",
    "http://localhost:5003",
]
```

For every incoming request, the load balancer checks each backend server.

It sends a request to:

```text
/api/stats
```

The backend returns information such as:

```json
{
    "cpu_usage_percent": 25.4,
    "memory": {
        "usage_percent": 41.2
    }
}
```

The load balancer then calculates:

```text
Load = CPU Usage + Memory Usage
```

For example:

```text
Server 1
CPU    = 30%
Memory = 40%

Load = 30 + 40
     = 70
```

The server with the lowest calculated load is selected.

---

# 🔄 Request Flow

Suppose the client sends:

```http
GET /products
```

The following process occurs:

```text
Client
  |
  | GET /products
  v
Load Balancer
  |
  |--- GET /api/stats ---> Backend 1
  |
  |--- GET /api/stats ---> Backend 2
  |
  |--- GET /api/stats ---> Backend 3
  |
  v
Calculate server loads
  |
  v
Select least-loaded server
  |
  v
GET /api/products
  |
  v
Selected Backend
  |
  v
Response
  |
  v
Client
```

---

# 🌐 APIs

## Backend Statistics API

```http
GET /api/stats
```

This endpoint provides the resource utilization of a backend instance.

The load balancer uses this information to determine the current load of the server.

Example:

```json
{
    "cpu_usage_percent": 25.4,
    "memory": {
        "usage_percent": 41.2
    }
}
```

---

## Products API

```http
GET /api/products
```

This represents the application endpoint that the load balancer forwards requests to.

The request is sent to whichever backend server has the lowest calculated load.

---

## Load Balancer API

```http
GET /products
```

This endpoint is exposed by the load-balancer application.

When this endpoint receives a request, it:

1. Checks all backend servers.
2. Retrieves CPU utilization.
3. Retrieves memory utilization.
4. Calculates the load of each server.
5. Selects the server with the lowest load.
6. Forwards the request.
7. Returns the backend response.

---

# 🐳 Docker Implementation

Docker is used to run the application instances in isolated containers.

The project uses:

* `Dockerfile` to build the application image.
* `docker-compose.yml` to define and run the services.
* Multiple backend instances to demonstrate application scaling.

The three backend instances run independently:

```text
+-------------------+
| Backend Container |
|       :5001       |
+-------------------+

+-------------------+
| Backend Container |
|       :5002       |
+-------------------+

+-------------------+
| Backend Container |
|       :5003       |
+-------------------+
```

The load balancer communicates with these instances through the Docker networking environment.

---

# 🚀 Running the Project

## 1. Clone the Repository

```bash
git clone <repository-url>
cd Load_Balancer_application
```

## 2. Build the Docker Containers

From the directory containing `docker-compose.yml`:

```bash
docker compose build
```

## 3. Start the Application

```bash
docker compose up
```

Or run it in detached mode:

```bash
docker compose up -d
```

## 4. Check Running Containers

```bash
docker ps
```

This allows you to verify that the load balancer and backend containers are running.

---

# 🧪 Testing

After starting the containers, send a request to the load balancer.

For example:

```bash
curl http://localhost:5000/products
```

The load balancer will check the available backend instances and select the backend with the lowest calculated resource load.

The application logs can be used to observe the process:

```text
Checking load for http://localhost:5001
Response from http://localhost:5001: 200
Calculated load for http://localhost:5001: ...

Checking load for http://localhost:5002
Response from http://localhost:5002: 200
Calculated load for http://localhost:5002: ...

Checking load for http://localhost:5003
Response from http://localhost:5003: 200
Calculated load for http://localhost:5003: ...

Best server selected: ...
```

---

# 🧰 Technologies

* **Python**
* **Flask**
* **REST APIs**
* **Docker**
* **Docker Compose**
* **Python Requests**
* **CPU/Memory Monitoring**
* **HTTP**

---

# 📚 What I Learned

Through this practical implementation, I gained hands-on experience with:

### Flask

* Creating Flask applications
* Using Flask Blueprints
* Creating REST API endpoints
* Forwarding HTTP requests

### Docker

* Creating Docker images
* Writing a `Dockerfile`
* Using Docker Compose
* Running multiple containers
* Working with containerized applications

### Load Balancing

* Understanding why load balancing is required
* Running multiple backend instances
* Monitoring backend resource utilization
* Selecting a backend dynamically
* Forwarding requests between services

### Networking

* Communicating between application instances
* Working with ports
* Understanding the role of Docker networking in distributed applications

---

# ⚠️ Limitations

This project is primarily a **learning/practical implementation** of load balancing.

It is not intended to replace production-grade load balancers.

The current implementation has several limitations:

* The load calculation is intentionally simple.
* CPU and memory are simply added together.
* No weighted resource calculation is used.
* Health checking is basic.
* No advanced retry mechanism is implemented.
* No sophisticated failure handling is implemented.
* The load balancer itself can become a single point of failure.
* No HTTPS termination is implemented.

Production systems commonly use dedicated solutions such as Nginx, HAProxy, Envoy, or cloud load-balancing services.

---

# 🎯 Practical Objective

The primary objective of this project was to understand how a web application can be **replicated across multiple containers** and how a separate service can distribute incoming requests among those instances.

The project demonstrates the basic relationship between:

```text
Docker
   +
Multiple Application Instances
   +
Backend APIs
   +
Resource Monitoring
   +
Request Forwarding
   =
Application Load Balancing
```

---

# 👨‍💻 Author

**Abdul Samad Tariq**

BS Computer Science Student

This project was developed as a practical exercise to gain hands-on experience with **Docker, Flask, backend APIs, networking, containerization, and load-balancing concepts**.
