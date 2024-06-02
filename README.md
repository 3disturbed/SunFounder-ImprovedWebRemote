
![robot](https://github.com/3disturbed/SunFounder-ImprovedWebRemote/assets/9502162/d33223ab-b864-45be-901a-f65f519c3c3c)
# SunFounder-ImprovedWebRemote
Improved web remote for the SunFounder Smart Car Robot
# Sunfounder Smart Robot Web Remote

Welcome to **Dark Firebeard's Sunfounder Smart Robot Web Remote** project! This repository contains an exciting and more responsive web-based remote control solution for the Sunfounder Smart Robot, utilizing the Sunfounder Robot Hat. Our goal is to provide a user-friendly and efficient interface to control your robot with ease.

## Features

- **Real-Time Control**: Experience instantaneous control of your Sunfounder Smart Robot with minimal latency.
- **Web-Based Interface**: Control your robot from any device with a web browser, no need for additional software.
- **Responsive Design**: The interface adjusts to any screen size, ensuring a seamless experience on desktops, tablets, and smartphones.
- **Live Video Feed**: View a live video feed from the robot's camera directly on the web interface.
- **Text-to-Speech (TTS)**: Communicate through your robot with pre-set phrases at the press of a button.
- **Easy Setup**: Simplified setup process to get your robot up and running in no time.

- WASD For Driving
- Cursor keys control robot head
- 1 - 9 to say phrases
- Q quickly recenter robot head.

## Getting Started

Follow these simple steps to set up your Sunfounder Smart Robot Web Remote:

### Prerequisites

- Raspberry Pi with Raspbian installed
- Sunfounder Smart Robot Kit
- Sunfounder Robot Hat
- Python 3.6 or higher

### Installation

1. **Clone the Repository**:
    ```sh
    git clone     git clone https://github.com/3disturbed/SunFounder-ImprovedWebRemote.git
    cd sunfounder-smart-robot-web-remote
    ```

2. **Install Required Python Packages**:
    ```sh
    pip3 install -r requirements.txt
    ```

### Running the Web Remote

You can run the web remote either as a systemd service (daemon) or manually. 

#### Running as a Systemd Service

1. **Create a Systemd Service File**:
    ```sh
    sudo nano /etc/systemd/system/robot_control.service
    ```
    Add the following content:
    ```ini
    [Unit]
    Description=Web Remote Service
    After=network.target

    [Service]
    User=root
    WorkingDirectory=/home/pi/sunfounder-smart-robot-web-remote
    ExecStart=/usr/bin/python3 /home/pi/sunfounder-smart-robot-web-remote/webremote.py
    Restart=always
    Environment=PYTHONUNBUFFERED=1
    StandardOutput=journal+console
    StandardError=journal+console
    SyslogIdentifier=webremote

    [Install]
    WantedBy=multi-user.target
    ```

2. **Reload systemd and Enable the Service**:
    ```sh
    sudo systemctl daemon-reload
    sudo systemctl enable robot_control.service
    sudo systemctl start robot_control.service
    ```

3. **Check the Service Status**:
    ```sh
    sudo systemctl status robot_control.service
    ```

4. **Access the Web Interface**:
    Open your web browser and go to `http://<your-raspberry-pi-ip>:5001` to access the web remote interface.

#### Running Manually

1. **Start the Web Remote**:
    ```sh
    sudo python3 /home/pi/sunfounder-smart-robot-web-remote/webremote.py
    ```

2. **Access the Web Interface**:
    Open your web browser and go to `http://<your-raspberry-pi-ip>:5001` to access the web remote interface.

## Usage

1. **Control Your Robot**:
    - Use the on-screen buttons or your keyboard to control the robot's movements.
    - Connect a game controller for a more immersive experience.

2. **View Live Video Feed**:
    - See what your robot sees in real-time through the live video feed.

3. **Send Text-to-Speech Commands**:
    - Use the pre-set phrases to communicate through your robot.

## Troubleshooting

- If the web interface is not accessible, check the service status:
    ```sh
    sudo systemctl status robot_control.service
    ```
- Ensure all dependencies are installed correctly and the Raspberry Pi is connected to your network.

## Contributions

We welcome contributions! Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Sunfounder](https://www.sunfounder.com) for their Smart Robot Kit and Robot Hat.

---

Enjoy controlling your Sunfounder Smart Robot with our responsive and easy-to-use web remote! If you have any questions or feedback, feel free to open an issue on GitHub.

Happy Roboting!
