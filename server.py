import json
from flask import Flask, jsonify

app = Flask(__name__)

# Load license data from licenses.json
try:
    with open('licenses.json', 'r') as f:
        LICENSES = set(json.load(f))
except FileNotFoundError:
    LICENSES = set()

@app.route('/check/<license_key>')
def check_license(license_key):
    """Check if the provided license key is valid."""
    if license_key in LICENSES:
        status = 'valid'
    else:
        status = 'invalid'
    return jsonify({'license': license_key, 'status': status})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
