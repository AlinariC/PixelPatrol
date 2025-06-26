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

## Install as a system service

Run the provided `install_service.sh` script as root to deploy PixelPatrol as a
systemd service. The script clones the repository to `/opt/pixelpatrol`,
installs Flask and registers a service called `pixelpatrol.service`.

```bash
sudo ./install_service.sh
```

After installation, control the service with `systemctl`:

```bash
sudo systemctl status pixelpatrol.service
```
