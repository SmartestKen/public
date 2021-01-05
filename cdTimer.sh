#!/bin/bash

# kill other timers

# use ./cdTimer.sh hh:mm:ss
mainLoop() {


    
    
    curEpoch=`date +%s`

    # default session 15 minutes
    time=${1:-'0:15:00'}
    IFS=':' read -ra time <<< "$time"


    if [ ${#time[@]} -eq 3 ]
    then
        time=$((10#${time[0]}*3600+10#${time[1]}*60+10#${time[2]}))
    elif [ ${#time[@]} -eq 2 ]
    then
        time=$((10#${time[0]}*60+10#${time[1]}))
    else
        time=$((10#${time[0]}))
    fi
    

    endEpoch=$(($curEpoch+$time))

    

    while [ $curEpoch -lt $endEpoch ]
    do
        echo -ne "\033[2K\r$((($endEpoch-$curEpoch)/60)) minutes left."
        sleep 30
        curEpoch=`date +%s`
    done

    
    echo -ne "\033[2K\rTime's up"


}


for pid in $(pidof -x "cdTimer.sh")
do
    if [ $pid != $$ ] 
    then
        kill $pid
    fi 
done


# remember to pass arguments into the function
mainLoop "$1" &









