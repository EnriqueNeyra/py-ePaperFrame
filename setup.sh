#!/bin/bash

# enable SPI Interface
echo "Enabling SPI interface..."
sudo sed -i 's/^dtparam=spi=.*/dtparam=spi=on/' /boot/config.txt
sudo sed -i 's/^#dtparam=spi=.*/dtparam=spi=on/' /boot/config.txt
sudo raspi-config nonint do_spi 0
sudo sed -i 's/^dtparam=i2c_arm=.*/dtparam=i2c_arm=on/' /boot/config.txt
sudo sed -i 's/^#dtparam=i2c_arm=.*/dtparam=i2c_arm=on/' /boot/config.txt
sudo raspi-config nonint do_i2c 0

echo "Installing required pythonh package(s)"
sudo apt-get install python3-qrcode
sudo apt-get install python3-flask

echo "Setting up python script epaper service"
PYTHON_SCRIPT="web_server.py"
SERVICE_NAME="epaper.service"
SERVICE_PATH="/etc/systemd/system/${SERVICE_NAME}"
CURRENT_USER=${SUDO_USER:-$(whoami)}

sudo tee "$SERVICE_PATH" > /dev/null <<EOF
[Unit]
Description=Flask Web Server
After=network.target

[Service]
ExecStart=/usr/bin/python3 $(pwd)/web_server.py
WorkingDirectory=$(pwd)
Restart=always
User=$CURRENT_USER

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl start "$SERVICE_NAME"
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl status "$SERVICE_NAME"

echo "Setup complete!"
#read -p "Reboot requried. Reboot now? (y/n): " REBOOT_CHOICE
#if [[ "$REBOOT_CHOICE" == "y" || "$REBOOT_CHOICE" == "Y" ]]; then
    #echo "Rebooting now..."
    #sudo reboot
#else
    #echo "Reboot skipped. Please remember to reboot at a later time."
#fi
