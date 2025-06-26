import json
from flask import Flask, jsonify, request

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


@app.route('/licenses', methods=['GET', 'POST'])
def manage_licenses():
    """Return the license list or add a new license."""
    if request.method == 'GET':
        return jsonify({'licenses': sorted(LICENSES)})

    data = request.get_json(silent=True) or {}
    new_license = data.get('license')
    if not new_license:
        return jsonify({'error': 'license key required'}), 400
    if new_license in LICENSES:
        return jsonify({'message': 'license already exists'}), 400

    LICENSES.add(new_license)
    with open('licenses.json', 'w') as f:
        json.dump(sorted(LICENSES), f)
    return jsonify({'message': 'license added', 'license': new_license}), 201


@app.route('/licenses/<license_key>', methods=['DELETE'])
def delete_license(license_key):
    """Delete a license key."""
    if license_key not in LICENSES:
        return jsonify({'error': 'license not found'}), 404

    LICENSES.remove(license_key)
    with open('licenses.json', 'w') as f:
        json.dump(sorted(LICENSES), f)
    return jsonify({'message': 'license deleted', 'license': license_key})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
