apt-get update;

apt -y install python3-pip;

# Postgres installation steps from: https://tecadmin.net/install-postgresql-server-on-ubuntu/
apt-get -y install wget ca-certificates;

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -;

apt-get -y install lsb-release;

sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list';

apt-get update;

apt-get -y install postgresql postgresql-contrib;

pip3 install -r requirements.txt;