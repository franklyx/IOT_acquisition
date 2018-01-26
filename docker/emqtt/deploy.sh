#!/bin/sh
sudo docker run -d --name emqtt --network spider -p 18083:18083 -p 1883:1883 emqtt:v1
