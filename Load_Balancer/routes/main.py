
from flask import Flask, jsonify,Blueprint
import requests
import logging
main_bp = Blueprint('main', __name__)

# servers = [
#     "http://0.0.0.0:5001",
#     "http://0.0.0.0:5002",
#     "http://0.0.0.0:5003",
# ]
servers = [
    "http://localhost:5001",
    "http://localhost:5002",
    "http://localhost:5003",
]
# Function to get least loaded server
def get_best_server():
    best_server = None
    lowest_load = float('inf')

    for server in servers:
        try:
            print(f"Checking load for {server}")

            response = requests.get(f"{server}/api/stats")
            print(f"Response from {server}: {response.status_code}")

            data = response.json()
            print(f"Load data from {server}: {data}")

            cpu = data["cpu_usage_percent"]
            memory = data["memory"]["usage_percent"]

            load = cpu + memory

            print(f"Calculated load for {server}: {load}")
            print(f"Current lowest load: {lowest_load}, Best server: {best_server}")

            if load < lowest_load:
                lowest_load = load
                best_server = server

        except Exception as e:
            print(f"Error contacting {server}: {e}")

    return best_server

@main_bp.route('/products', methods=["GET"])
def load_balanced_product():
    try:

        print("Getting the best server for /products")
        best_server = get_best_server()
        print(f"Best server selected: {best_server}")
        if not best_server:
            return jsonify({
                "error": "No backend servers available"
            }), 500

        # Forward request
        response = requests.get(f"{best_server}/api/products")

        return response.json()
    
    except Exception as e:
        logging.error(f"Error in load_balanced_product: {e}")
        return jsonify({
            "error": "Failed to fetch products"
        }), 500