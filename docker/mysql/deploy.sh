#!/bin/sh
sudo docker run -d --name mysql --network spider -v /opt/spider/mysql:/data/db mysql:v1
