from flask import Flask, jsonify
import requests

app = Flask(__name__)

servers = [
    "http://localhost:5000",
    "http://localhost:5001",
    "http://localhost:5002"
]

# Function to get least loaded server
def get_best_server():
    best_server = None
    lowest_load = float('inf')

    for server in servers:
        try:
            response = requests.get(f"{server}/stats")
            data = response.json()

            # Simple load formula
            load = data["cpu_usage"] + data["memory_usage"]

            if load < lowest_load:
                lowest_load = load
                best_server = server

        except Exception as e:
            print(f"Error contacting {server}: {e}")

    return best_server


@app.route('/product')
def load_balanced_product():

    best_server = get_best_server()

    if not best_server:
        return jsonify({
            "error": "No backend servers available"
        }), 500

    # Forward request
    response = requests.get(f"{best_server}/product")

    return response.json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)