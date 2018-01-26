#!/bin/sh

if sudo docker images | grep 'mongodb';then 
   
   echo 'you alreadly had mongo Docker image'

else

    echo 'not find mongo images,let`s pull it from docker from internet'
    sudo docker pull mongodb
fi
