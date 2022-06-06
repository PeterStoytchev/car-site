sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y git openvpn docker.io docker-compose

sudo cp vpn.conf /etc/openvpn/vpn.conf
sudo cp auth.txt /etc/openvpn/auth.txt
sudo cp bootscript.sh /etc/init.d/
sudo chmod +x /etc/init.d/bootscript.sh

echo "This is asking for VPN credentials!"
sudo systemctl start openvpn@vpn
sudo service openvpn restart