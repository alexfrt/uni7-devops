import logging
import sys
import time

import json_logging
from flask import Flask, jsonify, request


def setup_logger(app):
    json_logging.init_flask(enable_json=True)
    json_logging.init_request_instrument(app)
