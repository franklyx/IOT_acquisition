#!/bin/sh

if sudo docker images | grep 'emqtt';then 
   
   echo 'you alreadly had mongo Docker image'

else

    echo 'not find mongo images,let`s pull it from docker from internet'
    sudo docker pull 10.9.40.181:5000/keda/emqtt
fi
