#/bin/bash

/etc/init.d/mongodb start
mongo admin <<EOF
show dbs;
use admin;
db.addUser('admin','admin')
EOF
