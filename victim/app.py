# Simple Flask app for DDOS demonstration
# This app is intentionally simple and runs with minimal resources to be easy to overwhelm
from flask import Flask, request
import time
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Main endpoint, returns a simple message
    return "Hello from the Victim Server!"

@app.route('/slow')
def slow():
    # This endpoint is no longer artificially slow; any slowness is due to real resource exhaustion
    return "This was a slow response!"

@app.route('/status')
def status():
    # Returns a simple status message and the number of bytes read from the request
    return f"Victim server is running. Requests: {request.environ.get('wsgi.input').tell() if request.environ.get('wsgi.input') else 0}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    # Run in single-threaded mode to make the app more vulnerable to DDOS
    app.run(host='0.0.0.0', port=port, threaded=False)