echo "Starting setup script"

sudo apt-get update -y
sudo apt-get full-upgrade -y

sudo apt-get install -y openvpn docker.io docker-compose

echo "Finished installing updates and dependencies!"
echo "Connecting to VPN..."

sudo openvpn --config vpn.conf --daemon remote
echo "VPN connected in daemon mode!"

sudo sysctl net.ipv4.conf.all.forwarding=1
sudo iptables -P FORWARD ACCEPT
echo "Forwarding and iptables changed!"

sudo docker-compose build
sudo docker-compose up -d

echo "Pod composition is built and up! Waiting for 15 seconds, so that the DB can boot!"
sleep 15

CURRENT_LOG="mysql-bin.000003"
CURRENT_POS="600"

start_pod_stmt="CHANGE MASTER TO MASTER_HOST='192.168.1.118',MASTER_USER='mydb_slave_user',MASTER_PASSWORD='mydb_slave_pwd',MASTER_LOG_FILE='$CURRENT_LOG',MASTER_LOG_POS=$CURRENT_POS; START SLAVE;"
start_pod_cmd='export MYSQL_PWD=111; mysql -u root -e "'
start_pod_cmd+="$start_pod_stmt"
start_pod_cmd+='"'

sudo docker exec mysql_pod sh -c "$start_pod_cmd"

echo "Replication config changed with $start_pod_cmd"
echo "Pod setup finised!"
