if [ "$1" == "master" ]; then
    echo "Starting master..."
    sudo docker-compose -f docker-compose-master.yml start -d
    echo "Master composition started!"
else
    echo "Starting pod..."
    sudo sysctl net.ipv4.conf.all.forwarding=1
    sudo iptables -P FORWARD ACCEPT
    echo "Forwarding and iptables changed!"

    sudo openvpn --config vpn.conf --daemon remote
    echo "VPN connected in daemon mode!"

    sudo docker-compose -f docker-compose-pod.yml start -d

    echo "Pod composition started!"
fi