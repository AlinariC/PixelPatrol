#!/usr/bin/env bash
set -e

# This script installs PixelPatrol as a systemd service.
# It clones the repository, installs dependencies and starts the service.

REPO_URL=${REPO_URL:-"https://github.com/AlinariC/PixelPatrol.git"}
INSTALL_DIR=${INSTALL_DIR:-"/opt/pixelpatrol"}
SERVICE_FILE="/etc/systemd/system/pixelpatrol.service"
ALIAS_FILE="/etc/profile.d/pixelpatrol.sh"

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root" >&2
    exit 1
fi

# Clone or update the repository
if [ ! -d "$INSTALL_DIR" ]; then
    git clone "$REPO_URL" "$INSTALL_DIR"
else
    git -C "$INSTALL_DIR" pull
fi

# Install Python dependencies
pip3 install --upgrade flask

# Create systemd service
cat > "$SERVICE_FILE" <<SERVICE
[Unit]
Description=PixelPatrol Licensing Server
After=network.target

[Service]
ExecStart=/usr/bin/python3 $INSTALL_DIR/server.py
WorkingDirectory=$INSTALL_DIR
Restart=always
User=nobody
Group=nobody

[Install]
WantedBy=multi-user.target
SERVICE

# Reload systemd and enable/start the service
systemctl daemon-reload
systemctl enable pixelpatrol.service
systemctl restart pixelpatrol.service

# Add alias for the license management TUI
echo "alias pixelpatrol=\"sudo python3 $INSTALL_DIR/license_tui.py\"" > "$ALIAS_FILE"

echo "PixelPatrol service installed and running."
