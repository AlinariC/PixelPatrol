# PixelPatrol

PixelPacific Licensing Server for PiBells.

## Requirements
- Python 3
- Flask (`pip install flask`)

## Usage
1. Edit `licenses.json` to include all valid license keys.
2. Run the server:
   ```bash
   python3 server.py
   ```
3. The server listens on port 5000. Clients can check a license by sending a GET request to `/check/<license_key>`.

Example:
```bash
curl http://localhost:5000/check/ABC123
```

The server responds with JSON indicating whether the license is valid.
