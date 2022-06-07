if [ "$1" == "master" ]; then
    echo "Starting master..."
    sudo docker start mysql_master
    echo "Master composition started!"
else
    echo "Starting pod..."
    sudo sysctl net.ipv4.conf.all.forwarding=1
    sudo iptables -P FORWARD ACCEPT
    echo "Forwarding and iptables changed!"

    sudo openvpn --config vpn.conf --daemon remote
    echo "VPN connected in daemon mode!"

    sudo docker-compose start -d

    echo "Pod composition started!"
fi