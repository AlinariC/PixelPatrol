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
2. Edit `licenses.json` or use the TUI to add new license keys. Each key
   now stores the customer name, email and expiration date in addition to the
   license string. Keys are automatically generated as 24-character
   alphanumeric strings when added through the TUI.
3. Run the server:
   ```bash
   python3 server.py
   ```
4. The server listens on port 5000. Clients can check a license by sending a GET request to `/check/<license_key>?email=<registered_email>`.

Example:
```bash
curl "http://localhost:5000/check/ABC123?email=user@example.com"
```

The server responds with JSON indicating whether the license is valid and
provides the expiration date. Only the status (`VALID` or `INVALID`) and the
expiration date are returned to the client.

## Managing Licenses

License keys are edited locally using the included text based interface.
Run the `license_tui.py` script to view, add or remove keys. The web server
does not provide endpoints for modifying licenses.

### Text interface

The TUI presents a simple curses-based UI for viewing, adding and removing
license keys. When adding a key you will be prompted for the customer name,
email and expiration date.

```bash
python3 license_tui.py
```

Use the arrow keys to navigate, press `a` to generate and add a new license,
`d` to delete the selected key and `q` to quit. Changes are saved to
`licenses.json`.

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
