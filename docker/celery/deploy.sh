#!/bin/sh
sudo docker run -d --name $1 --network spider -v `pwd`/code/$1:/opt/spider celery:v1
