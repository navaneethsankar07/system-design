import os
import time
import socket
from flask import Flask, jsonify, request

app = Flask(__name__)

INSTANCE_ID = os.getenv("INSTANCE_ID", socket.gethostname())
INSTANCE_CAPACITY = os.getenv("INSTANCE_CAPACITY", "normal")


@app.route("/")
def home():
    return jsonify({
        "message": "Load Balancing Lab Backend",
        "instance_id": INSTANCE_ID,
        "capacity": INSTANCE_CAPACITY,
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "instance_id": INSTANCE_ID,
    }), 200


@app.route("/info")
def info():
    return jsonify({
        "instance_id": INSTANCE_ID,
        "hostname": socket.gethostname(),
        "capacity": INSTANCE_CAPACITY,
        "pid": os.getpid(),
    })


@app.route("/work")
def work():
    delay = request.args.get("delay", default=0, type=float)

    # Prevent unreasonable delays during experiments.
    delay = max(0, min(delay, 10))

    start_time = time.perf_counter()
    time.sleep(delay)
    processing_time = time.perf_counter() - start_time

    return jsonify({
        "instance_id": INSTANCE_ID,
        "hostname": socket.gethostname(),
        "delay_requested": delay,
        "processing_time_seconds": round(processing_time, 4),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)