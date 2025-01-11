#!/bin/bash

# enable SPI Interface
echo "Enabling SPI interface..."
sudo sed -i 's/^dtparam=spi=.*/dtparam=spi=on/' /boot/config.txt
sudo sed -i 's/^#dtparam=spi=.*/dtparam=spi=on/' /boot/config.txt
sudo raspi-config nonint do_spi 0
sudo sed -i 's/^dtparam=i2c_arm=.*/dtparam=i2c_arm=on/' /boot/config.txt
sudo sed -i 's/^#dtparam=i2c_arm=.*/dtparam=i2c_arm=on/' /boot/config.txt
sudo raspi-config nonint do_i2c 0

# venv and dependency setup
echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing packages from requirements.txt..."
pip3 install -r requirements.txt
deactivate
echo "Packages installed."

SCRIPT_PATH="$(pwd)/web_server.py"

echo "Creating script to run on boot..."
sudo sed -i '/exit 0/d' /etc/rc.local
echo "source $(pwd)/venv/bin/activate && python3 $SCRIPT_PATH &" | sudo tee -a /etc/rc.local
echo "exit 0" | sudo tee -a /etc/rc.local
#SERVICE_NAME="epaper"
#PYTHON_SCRIPT="web_server.py"
#SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME.service"
#CURRENT_USER=$(whoami)


#sudo bash -c "cat > $SERVICE_PATH" <<EOL
#[Unit]
#Description=My Python Script Service
#After=network.target

#[Service]
#Type=simple
#WorkingDirectory=$(pwd)
#ExecStart=$(pwd)/venv/bin/python3 $(pwd)/$PYTHON_SCRIPT
#Restart=always
#User=$CURRENT_USER

#[Install]
#WantedBy=multi-user.target
#EOL

#sudo systemctl daemon-reload
#sudo systemctl enable $SERVICE_NAME
#sudo systemctl start $SERVICE_NAME

echo "Setup complete!"
read -p "Reboot requried. Reboot now? (y/n): " REBOOT_CHOICE
if [[ "$REBOOT_CHOICE" == "y" || "$REBOOT_CHOICE" == "Y" ]]; then
    echo "Rebooting now..."
    sudo reboot
else
    echo "Reboot skipped. Please remember to reboot at a later time."
fi
