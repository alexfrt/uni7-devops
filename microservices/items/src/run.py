from faker import Faker
from flask import Flask, jsonify
import json_logging, logging, sys


app = Flask(__name__)
data = []
fake = Faker()

json_logging.init_flask(enable_json=True)
json_logging.init_request_instrument(app)
logger = logging.getLogger("test-logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


@app.route('/allItems', methods=['GET'])
def all_orders():
    logger.info("all_orders()")
    return jsonify(data), 200


@app.route('/item/<int:num>', methods=['GET'])
def get_order(num):
    logger.info("get_order()")
    return jsonify(data[num]), 200


def create_items(num):
    return {
        'id': num,
        'desc': fake.bs()
    }


def create_data():
    return [create_items(num) for num in range(1, 100)]


if __name__ == '__main__':
    data = create_data()
    app.run(host='0.0.0.0', port=5000, debug=False)
