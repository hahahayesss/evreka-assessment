import os
import pika
import json
from app import repository
from flask import Flask, request, jsonify

app = Flask(__name__)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
QUEUE_NAME = "location_queue"

REQUEST_KEYS = [
    "device_id",
    "latitude",
    "longitude",
    "speed",
    "timestamp"
]


def _send_to_queue(message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST
        )
    )
    channel = connection.channel()
    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(message)
    )
    connection.close()


@app.route("/api/locations/range", methods=["GET"])
def get_by_range():
    device_id = request.args.get("device_id")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    if not (device_id and start_date and end_date):
        return jsonify({"error": "Request not validated"}), 400

    try:
        data = repository.find_by_range(device_id, start_date, end_date)
        print(data)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/locations/latest", methods=["GET"])
def get_latest():
    device_id = request.args.get('device_id')
    if not device_id:
        return jsonify({"error": "Request not validated"}), 400

    try:
        data = repository.find_by_latest(device_id)
        if data:
            return jsonify(data), 200
        else:
            return jsonify({"error": "No data found for the device"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/locations", methods=["POST"])
def create_location():
    data = request.json
    if not all(k in data for k in REQUEST_KEYS):
        return jsonify({"error": "Request body not validated"}), 400
    _send_to_queue(data)
    return jsonify({"message": "Data submitted successfully"}), 200


if __name__ == "__main__":
    app.run()
