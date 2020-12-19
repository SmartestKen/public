#!/bin/bash


# assume magick executable and scan directory exists 

if [ "${1:-None}" != "None" ]
then
    /home/public/magick import /home/private/scan/$1.jpg
else
    /home/public/magick import /home/private/scan/`date +%s`.jpg
fi
    
