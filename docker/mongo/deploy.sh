#!/bin/sh
sudo docker run -d --name mongodb --network spider -v /opt/spider/mongodb:/data/db -p 27017:27017 mongodb:v1
