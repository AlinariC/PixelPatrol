# PixelPatrol

PixelPacific Licensing Server for PiBells.

## Requirements
- Python 3
- Flask (`pip install flask`)

## Usage
1. Clone the repository and enter the directory:
   ```bash
   git clone https://github.com/AlinariC/PixelPatrol.git
   cd PixelPatrol
   ```
2. Edit `licenses.json` to include all valid license keys.
3. Run the server:
   ```bash
   python3 server.py
   ```
4. The server listens on port 5000. Clients can check a license by sending a GET request to `/check/<license_key>`.

Example:
```bash
curl http://localhost:5000/check/ABC123
```

The server responds with JSON indicating whether the license is valid.

## Managing Licenses

PixelPatrol exposes additional endpoints for viewing, adding and deleting
licenses. All responses are JSON.

- `GET /licenses` - return the current list of licenses.
- `POST /licenses` - add a license key. The request body should be JSON with a
  `license` field.
- `DELETE /licenses/<license>` - remove the specified license key.

Example adding a license:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"license": "NEWKEY"}' http://localhost:5000/licenses
```

### Text interface

For local administration without exposing the HTTP endpoints, run the
`license_tui.py` script. It presents a simple curses-based UI for viewing,
adding and removing license keys.

```bash
python3 license_tui.py
```

Use the arrow keys to navigate, press `a` to add a new license, `d` to delete
the selected key and `q` to quit. Changes are saved to `licenses.json`.

## Install as a system service

Run the `install_service.sh` script as root to deploy PixelPatrol as a
systemd service. The script clones the repository to `/opt/pixelpatrol`,
installs Flask and registers a service called `pixelpatrol.service`.

```bash
curl -fsSL https://raw.githubusercontent.com/AlinariC/PixelPatrol/main/install_service.sh | sudo bash
```

After installation, control the service with `systemctl`:

```bash
sudo systemctl status pixelpatrol.service
```
