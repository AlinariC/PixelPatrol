import json
from datetime import datetime, date
from flask import Flask, jsonify

app = Flask(__name__)

# Load license data from licenses.json
try:
    with open('licenses.json', 'r') as f:
        data = json.load(f)
        if data and isinstance(data[0], str):
            LICENSES = {
                key: {
                    'name': '',
                    'email': '',
                    'expires': ''
                } for key in data
            }
        else:
            LICENSES = {item['key']: item for item in data}
except FileNotFoundError:
    LICENSES = {}

@app.route('/check/<license_key>')
def check_license(license_key):
    """Check if the provided license key is valid."""
    info = LICENSES.get(license_key)
    if not info:
        return jsonify({'license': license_key, 'status': 'invalid'})

    expired = False
    exp = info.get('expires')
    if exp:
        try:
            exp_date = datetime.strptime(exp, '%Y-%m-%d').date()
            expired = exp_date < date.today()
        except ValueError:
            pass

    status = 'valid' if not expired else 'expired'
    payload = {
        'license': license_key,
        'status': status,
        'name': info.get('name'),
        'email': info.get('email'),
        'expires': exp,
    }
    return jsonify(payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
