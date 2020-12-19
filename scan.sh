#!/bin/bash

# assume magick executable and scan directory exists




folder_name=`date +%s`
mkdir /home/private/scan/$folder_name
scanimage  --resolution 300 --format=jpeg --batch=/home/private/scan/$folder_name/%d.jpg --source 'ADF Duplex' --mode color




if [ "${1:-None}" = "pdf" ]
then
    /home/public/magick convert /home/private/scan/$folder_name/*.jpg /home/private/scan/$folder_name/scan.pdf
fi


# nothing in the folder (failure)
if [ -z "$(ls -A /home/private/scan/$folder_name)" ]
then
   rm -rf /home/private/scan/$folder_name
fi
