echo "Starting setup script in configuration $1"

sudo apt-get update -y
sudo apt-get full-upgrade -y

if [ "$1" == "master" ]; then
    sudo apt-get install -y docker.io docker-compose
else
    sudo apt-get install -y openvpn docker.io docker-compose
fi
echo "Finished installing updates and dependencies!"

if [ "$1" == "master" ]; then
    sudo docker run -d --mount source=mysql_master/conf/mysql.conf.cnf,target=/etc/mysql/conf.d/mysql.conf.cnf --env-file mysql_master/mysql_master.env --name mysql_master -p 3306:3306 mysql:5.7
    
    echo "Master composition is built and up! Waiting for 15 seconds, so that the DB can boot!"
    sleep 15

    priv_stmt='GRANT REPLICATION SLAVE ON *.* TO "mydb_slave_user"@"%" IDENTIFIED BY "mydb_slave_pwd"; FLUSH PRIVILEGES;'
    sudo docker exec mysql_master sh -c "export MYSQL_PWD=111; mysql -u root -e '$priv_stmt'"

    echo "Replication permissions set!"

    MS_STATUS=`sudo docker exec mysql_master sh -c 'export MYSQL_PWD=111; mysql -u root -e "SHOW MASTER STATUS"'`
    CURRENT_LOG=`echo $MS_STATUS | awk '{print $6}'`
    CURRENT_POS=`echo $MS_STATUS | awk '{print $7}'`

    echo "Master bin log info (if needed for pod db init)"
    echo $MS_STATUS
    echo $CURRENT_LOG
    echo $CURRENT_POS

    echo "Master setup finised!"
else
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
fi