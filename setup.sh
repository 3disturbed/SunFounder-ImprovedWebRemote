#!/bin/bash

echo "Starting setup for Sunfounder Smart Robot Web Remote..."

# Update the package list and upgrade all packages
echo "Updating system..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Python 3 and pip
echo "Installing Python 3 and pip..."
sudo apt-get install -y python3 python3-pip

# Install Flask and Flask-SocketIO
echo "Installing Flask and Flask-SocketIO..."
sudo pip3 install flask flask-socketio

# Install OpenCV
echo "Installing OpenCV..."
sudo apt-get install -y python3-opencv

# Install additional required Python packages
echo "Installing additional required Python packages..."
sudo pip3 install eventlet

# Install dependencies for the Sunfounder Smart Robot
echo "Installing dependencies for Sunfounder Smart Robot..."
sudo apt-get install -y i2c-tools python3-smbus

# Clone the repository
echo "Cloning the repository..."
cd /home/pi
git clone https://github.com/3disturbed/SunFounder-ImprovedWebRemote.git
cd SunFounder-ImprovedWebRemote

# Create a systemd service file
echo "Creating systemd service file..."
sudo bash -c 'cat << EOF > /etc/systemd/system/robot_control.service
[Unit]
Description=Web Remote Service
After=network.target

[Service]
User=root
WorkingDirectory=/home/pi/SunFounder-ImprovedWebRemote
ExecStart=/usr/bin/python3 /home/pi/SunFounder-ImprovedWebRemote/webremote.py
Restart=always
Environment=PYTHONUNBUFFERED=1
StandardOutput=journal+console
StandardError=journal+console
SyslogIdentifier=webremote

[Install]
WantedBy=multi-user.target
EOF'

# Reload systemd to apply the new service
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Enable and start the service
echo "Enabling and starting the robot control service..."
sudo systemctl enable robot_control.service
sudo systemctl start robot_control.service

echo "Setup complete. You can now access the web interface at http://<your-raspberry-pi-ip>:5001"
