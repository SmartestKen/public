#!/bin/bash
# assume /home/public/temp as the src location
# every 15 minutes (900)
# no self update, exclude any init.sh file
# root_setup -> download git repo directly to /temp
# https://unix.stackexchange.com/questions/272197/why-cant-mv-deal-with-existence-of-same-name-directory-in-destination
# https://unix.stackexchange.com/questions/24395/rewrite-existing-file-so-that-it-gets-replaced-by-new-version-atomically-only-o
# https://serverfault.com/questions/676221/is-mv-with-wildcard-still-atomic/676231

updateLoop() {
    
    # assume a full executable copy at /temp (and git already setup)
    # assume nothing about /tempCopy
    /temp/startup.sh 
    /temp/sync.sh
    /temp/enforceTimer.sh
    
    
    eval $(ssh-agent -s)    
    ssh-add /temp/.ssh/id_rsa

    rm -rf /tempCopy/.stage
    mkdir /tempCopy/.stage
    rm -rf /tempCopy/.trash
    mkdir /tempCopy/.trash
    
    
    shopt -s nullglob
    cd /temp
    declare -a collection=("init.sh" "mitmproxy_config.py" "siteFilter.txt" "startup.sh" "sync.sh" "enforceTimer.sh" "recover.sh" "update.sh" "github_instruction.sh" "user_startup.sh")
    prev_folder_stat=-1
    correct_time=0
    
    
    
    
    while true
    do
    
        # avoid bios time hack
        if [ $correct_time -eq 0 ]
        then
            internet_time=`wget -qSO- --max-redirect=0 google.com 2>&1`
            if [ $? -eq 8 ]
            then
                date -s "$(grep Date: <<< "$internet_time" | cut -d' ' -f5-8)Z"
                correct_time=1
            # retry 10 seconds later
            else
                sleep 10
            fi                

            
        else
        
        
            
            

            current_stat=`stat -c %Y /home/public/temp`
            # i.e. always add at the startup
            if [ $? -eq 0 ] && [ $current_stat -ne $last_stat ]
            then            
                for file in "${collection[@]}"
                do
                    # echo "/home/public/temp/$file"
                    if [ -e /home/public/temp/$file ]
                    then
                        # fail to copy, stop
                        cp /home/public/temp/$file /tempCopy/.stage/
                        if [ $? -ne 0 ]
                        then
                            echo "fail to copy $file at `date`" >>/tempCopy/log.txt
                            rm -f /tempCopy/.stage/$file
                            continue
                        fi
                        # copy to stage succeed, make .sh executable
                        if [ "${file#*.}" = "sh" ]
                        then
                            chmod 744 /tempCopy/.stage/$file
                        fi
                    fi
                done
                
                
                if [ "$(ls -A /tempCopy/.stage/)" ]
                then
                    cur_time=`date +%s`
                    mkdir /tempCopy/$cur_time
                    mv /tempCopy/.stage/* /tempCopy/$cur_time/
                fi
                
                last_stat=$current_stat
            fi
        
        
        

        

            
            allow_time=$((`date +%s`-600))
            most_uptodate_dir=-1
            # assume nullglob
            for time in /tempCopy/*/
            do
                # string trim syntax ##,#,%%,% (remove the last slash, then everything 
                # till the second to last slash)
                # https://aty.sdsu.edu/bibliog/latex/debian/bash.html
                time="${time%/}"
                time="${time##*/}"
                echo "I read this folder $time"
                
                # put same folder in /home/public/temp
                # will activate the option to remove from the queue
                if [ -d "/home/public/temp_remove/$time" ]
                then
                    rm -rf /tempCopy/$time
                    continue
                fi
                
                
                
                if [ $time -le $allow_time ]
                then
                    echo "good folder $time"
                    rm -rf /tempCopy/$most_uptodate_dir
                    most_uptodate_dir=$time
                # the end of good dir, can start update
                else
                    break
                fi                    
            done
            
            if [ $most_uptodate_dir -ne -1 ]
            then
                
                mv /tempCopy/$most_uptodate_dir/* /temp/
                # remove after update
                rm -rf /tempCopy/$most_uptodate_dir
                git add --ignore-errors /temp/
                git commit -m "$most_uptodate_dir" -q >/dev/null
                # commits from init service only
                git push -f origin master -q
                echo "last updated at `date`" >>/tempCopy/log.txt
                
                
                # updated
                /temp/startup.sh reinit
                /temp/sync.sh
                /temp/enforceTimer.sh 
                
                # sync.sh will kill the ssh-agent, hence need to restart
                eval $(ssh-agent -s)    
                ssh-add /temp/.ssh/id_rsa
            fi
            
            
            
            sleep 180
        fi
        
        
    done
}                


for pid in $(pidof -x "init.sh")
do
    if [ $pid != $$ ] 
    then
        kill $pid
    fi 
done

pkill ssh-agent
updateLoop &
