from faker import Faker
from flask import Flask, jsonify, request
import json_logging, logging, sys
import random
import time


app = Flask(__name__)
data = []
fake = Faker()

json_logging.init_flask(enable_json=True)
json_logging.init_request_instrument(app)
logger = logging.getLogger("test-logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


@app.route('/allOrders', methods=['GET'])
def all_orders():
    time.sleep(random.randint(0, 10))
    logger.info("all_orders()")
    return jsonify(data), 200


@app.route('/order/<int:num>', methods=['GET'])
def get_order(num):
    time.sleep(random.randint(0, 10))
    logger.info("get_order()")
    return jsonify(data[num]), 200


@app.route('/custSearch', methods=['POST'])
def cust_search():
    time.sleep(random.randint(0, 10))
    logger.info("cust_search()")
    json = request.get_json()
    name = json.get('name', '')
    result = [order for order in data if name in order['cust']]
    return jsonify(result), 200


def create_order(num):
    return {
        'id': num,
        'cust': fake.name(),
        'items': [random.randint(1, 100) for _ in range(1, random.randint(1, 10))]
    }


def create_data():
    return [create_order(num) for num in range(1, 1000)]


if __name__ == '__main__':
    data = create_data()
    app.run(host='0.0.0.0', port=5000, debug=False)
