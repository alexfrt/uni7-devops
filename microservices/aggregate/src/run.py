from flask import Flask, jsonify, request
import json_logging, logging, sys
import requests


app = Flask(__name__)

json_logging.init_flask(enable_json=True)
json_logging.init_request_instrument(app)
logger = logging.getLogger("test-logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


@app.route('/detail/<int:order_id>', methods=['GET'])
def detail(order_id):
    logger.info("detail")
    order = requests.get('http://demo_orders:5000/order/{}'.format(order_id), headers={"X-Correlation-ID":json_logging.get_correlation_id()}).json()
    items = [_fetch_item(item_id) for item_id in order.get('items', [])]
    del order['items']
    order['items'] = items
    return jsonify(order), 200


def _fetch_item(item_id):
    return requests.get('http://demo_items:5000/item/{}'.format(item_id), headers={"X-Correlation-ID":json_logging.get_correlation_id()}).json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)