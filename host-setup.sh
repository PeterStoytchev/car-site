sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y git openvpn docker.io docker-compose

sudo cp vpn.conf /etc/openvpn/vpn.conf
sudo cp bootscript.sh /etc/init.d/

sudo service openvpn restart
sudo systemctl start openvpn@vpn