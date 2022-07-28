#! /bin/bash
#
# Provisioning script for server db

#------------------------------------------------------------------------------
# Bash settings
#------------------------------------------------------------------------------

# Enable "Bash strict mode"
set -o errexit   # abort on nonzero exitstatus
set -o nounset   # abort on unbound variable
set -o pipefail  # do not mask errors in piped commands

#------------------------------------------------------------------------------
# Variables
#------------------------------------------------------------------------------

# Location of provisioning scripts and files
export readonly PROVISIONING_SCRIPTS="/vagrant/provisioning/"
# Location of files to be copied to this server
export readonly PROVISIONING_FILES="${PROVISIONING_SCRIPTS}/files/${HOSTNAME}"

# Database name
readonly db_name=Discord_Bots

# Database table
readonly db_table=Sad_Words

# Database user
readonly db_user=user

readonly db_table2=Encouragements

#------------------------------------------------------------------------------
# Functions
#------------------------------------------------------------------------------

# Predicate that returns exit status 0 if the database root password
# is not set, a nonzero exit status otherwise.
is_mysql_root_password_empty() {
  mysqladmin --user=root status > /dev/null 2>&1
}

#------------------------------------------------------------------------------
# Provision server
#------------------------------------------------------------------------------

# First perform common actions for all servers
source ${PROVISIONING_SCRIPTS}/common.sh
source ${PROVISIONING_FILES}/.env

log "=== Starting server specific provisioning tasks on ${HOSTNAME} ==="

log "Installing MariaDB server"

dnf install -y mariadb-server 

log "Enabling MariaDB service"

systemctl enable --now mariadb.service

log "Setting firewall rules"

firewall-cmd --add-service=mysql --permanent
firewall-cmd --reload

log "Securing the database"

if is_mysql_root_password_empty; then
mysql --user=root <<_EOF_
  UPDATE mysql.user SET Password=PASSWORD('${db_root_password}') WHERE User='root';
  DELETE FROM mysql.user WHERE User='';
  DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
  DROP DATABASE IF EXISTS test;
  DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';
  FLUSH PRIVILEGES;
_EOF_
fi

log "Creating database and user"

mysql --user=root --password="${db_root_password}" << _EOF_
CREATE DATABASE IF NOT EXISTS ${db_name};
GRANT ALL ON ${db_name}.* TO '${db_user}'@'%' IDENTIFIED BY '${db_password}';
FLUSH PRIVILEGES;
_EOF_

log "Creating database table"

mysql --user="${db_user}" --password="${db_password}" "${db_name}" <<_EOF_
CREATE TABLE IF NOT EXISTS ${db_table} (
  id int NOT NULL,
  sad_word varchar(50) DEFAULT NULL,
  PRIMARY KEY(id)
);
_EOF_

log "Creating database table 2"

mysql --user="${db_user}" --password="${db_password}" "${db_name}" <<_EOF_
CREATE TABLE IF NOT EXISTS ${db_table2} (
  id int NOT NULL,
  encouragement varchar(255) DEFAULT NULL,
  PRIMARY KEY(id)
);
_EOF_
