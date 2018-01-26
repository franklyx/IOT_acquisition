#!/bin/sh
sudo docker run -d --name redis --network spider -p 6379:6379 redis:v1
