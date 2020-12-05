import redis
from flask import Flask, jsonify
import json_logging, logging, sys

app = Flask(__name__)
redis = redis.Redis(host='redis', port=6379, db=0)

json_logging.init_flask(enable_json=True)
json_logging.init_request_instrument(app)
logger = logging.getLogger("test-logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

@app.route('/')
def hello_world():
    logger.info('hi there')
    return jsonify('Hello, World!')

@app.route('/visitor')
def visitor():
    redis.incr('visitor')
    visitor_num = redis.get('visitor').decode("utf-8")
    logger.info(f'{visitor_num} visitor entered successfully')
    return jsonify(f'{visitor_num} visitor entered successfully')

@app.route('/visitor/reset')
def reset_visitor():
    redis.set('visitor', 0)
    visitor_num = redis.get('visitor').decode("utf-8")
    logger.info(f'{visitor_num} reseted successfully')
    return jsonify(f'{visitor_num} reseted successfully')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)