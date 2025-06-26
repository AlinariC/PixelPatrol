import json
from datetime import datetime, date
from flask import Flask, jsonify, request

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
    """Validate a license key using the provided email."""
    info = LICENSES.get(license_key)
    email = request.args.get('email', '').strip().lower()
    if not info or info.get('email', '').lower() != email:
        return jsonify({'status': 'INVALID'})

    expired = False
    exp = info.get('expires')
    if exp:
        try:
            exp_date = datetime.strptime(exp, '%Y-%m-%d').date()
            expired = exp_date < date.today()
        except ValueError:
            pass

    status = 'VALID' if not expired else 'INVALID'
    payload = {
        'status': status,
        'expires': exp,
    }
    return jsonify(payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
