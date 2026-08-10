import app
from flask import Flask,jsonify,Blueprint
import subprocess
import re
import random
api_bp = Blueprint("api", __name__)

def get_system_stats():
    # Run top in batch mode (-b) for single snapshot (-n 1)
    output = subprocess.check_output(["top", "-b", "-n", "1"]).decode("utf-8")

    cpu_usage = None
    mem_usage = {}

    for line in output.split("\n"):
        # CPU line example:
        # %Cpu(s):  2.3 us,  1.0 sy,  0.0 ni, 96.5 id, ...
        if "%Cpu(s)" in line:
            cpu_match = re.search(r"(\d+\.\d+)\s+id", line)
            if cpu_match:
                idle = float(cpu_match.group(1))
                cpu_usage = round(100 - idle, 2)

        # Memory line example:
        # MiB Mem :  15946.0 total,  10234.3 free,  ...
        if "MiB Mem" in line or "KiB Mem" in line:
            nums = re.findall(r"([\d\.]+)", line)
            if len(nums) >= 3:
                total = float(nums[0])
                free = float(nums[1])
                used = float(nums[2])

                mem_usage = {
                    "total": total,
                    "used": used,
                    "free": free,
                    "usage_percent": round((used / total) * 100, 2)
                }

    return {
        "cpu_usage_percent": cpu_usage,
        "memory": mem_usage
    }


@api_bp.route("/stats", methods=["GET"])
def stats():
    try:
        data = get_system_stats()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



##Random Api here

products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 1200,
        "stock": 15
    },
    {
        "id": 2,
        "name": "Smartphone",
        "price": 800,
        "stock": 30
    },
    {
        "id": 3,
        "name": "Headphones",
        "price": 150,
        "stock": 50
    },
    {
        "id": 4,
        "name": "Keyboard",
        "price": 70,
        "stock": 25
    },
    {
        "id": 5,
        "name": "Mouse",
        "price": 40,
        "stock": 40
    }
]

# API 1 -> Get all products
@api_bp.route('/products', methods=['GET'])
def get_products():
    return jsonify({
        "success": True,
        "products": products
    })


# API 2 -> Get random product
@api_bp.route('/random-product', methods=['GET'])
def random_product():
    product = random.choice(products)

    return jsonify({
        "success": True,
        "product": product
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)