from flask import Flask, json, jsonify, request
import json_logging, logging, sys
import requests
from prometheus_client import start_http_server, Summary


app = Flask(__name__)

json_logging.init_flask(enable_json=True)
json_logging.init_request_instrument(app)
logger = logging.getLogger("test-logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

@app.route('/orders', methods=['GET'])
@REQUEST_TIME.time()
def orders():
    logger.info("orders")
    count = request.args.get('count')
    data = requests.get('http://demo_orders:5000/allOrders', headers={"X-Correlation-ID":json_logging.get_correlation_id()}).json()
    if count:
        return jsonify(data[:int(count)]), 200
    else:
        return jsonify(data), 200

@app.route('/detail/<int:order_id>', methods=['GET'])
@REQUEST_TIME.time()
def detail(order_id):
    logger.info("detail")
    data = requests.get('http://demo_aggregate:5000/detail/{}'.format(order_id), headers={"X-Correlation-ID":json_logging.get_correlation_id()}).json()
    return jsonify(data), 200


@app.route('/custSearch/<string:name>', methods=['GET'])
@REQUEST_TIME.time()
def cust_search(name):
    logger.info("cust_search")
    payload = {'name': name}
    data = requests.post('http://demo_orders:5000/custSearch', json=payload, headers={"X-Correlation-ID":json_logging.get_correlation_id()}).json()
    return jsonify(data), 200


if __name__ == '__main__':
    start_http_server(8000)
    app.run(host='0.0.0.0', port=5000, debug=False)
