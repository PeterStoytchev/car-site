CURRENT_LOG="mysql-bin.000003"
CURRENT_POS="600"

start_pod_stmt="CHANGE MASTER TO MASTER_HOST='94.fontyslab.com',MASTER_PORT=21401,MASTER_USER='mydb_slave_user',MASTER_PASSWORD='mydb_slave_pwd',MASTER_LOG_FILE='$CURRENT_LOG',MASTER_LOG_POS=$CURRENT_POS; START SLAVE;"
start_pod_cmd='export MYSQL_PWD=111; mysql -u root -e "'
start_pod_cmd+="$start_pod_stmt"
start_pod_cmd+='"'

sudo docker exec mysql_pod sh -c "$start_pod_cmd"