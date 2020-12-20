# Thanks: https://gist.githubusercontent.com/mugifly/a29f34df7de8960d72245fcb124513c7/raw/switchbot-cmd.py

# https://wiki.debian.org/UnattendedUpgrades
apt-get install unattended-upgrades apt-listchanges

sudo apt-get install -y python-pip libglib2.0-dev bluez-tools
sudo pip install --upgrade  bluepy google-api-python-client google-auth-httplib2 google-auth-oauthlib
sudo hciconfig hci0 down
sudo btmgmt le on
sudo hciconfig hci0 up

# desktop
scp -r switchbot pi@192.168.11.14:

sudo cp switchbot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable switchbot.service
sudo systemctl start switchbot.service
