import logging
import sys
from random import gammavariate
from time import sleep

import json_logging
import prometheus_client
import redis
from flask import Flask, Response, jsonify

from instrumentation import logging, prometheus

app = Flask(__name__)
logging.setup_logger(app)
prometheus.setup_metrics(app)
redis = redis.Redis(host='redis', port=6379, db=0)


@app.route('/')
def hello_world():
    sleep(gammavariate(1.5, 2))
    return jsonify('OK')


@app.route('/visitor')
def visitor():
    redis.incr('visitor')
    return {'visitor': redis.get('visitor').decode("utf-8")}


@app.route('/visitor/reset')
def reset_visitor():
    redis.set('visitor', 0)
    return {'visitor': redis.get('visitor').decode("utf-8")}


@app.route('/metrics')
def metrics():
    return Response(prometheus_client.generate_latest(), mimetype=str('text/plain; version=0.0.4; charset=utf-8'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)
