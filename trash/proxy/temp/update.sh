#!/bin/bash


#----------------configure/upload files----------------

chmod 744 /temp/init.sh
chmod 744 /temp/sync.sh
chmod 744 /temp/recover.sh
chmod 744 /temp/update.sh


eval $(ssh-agent -s)
ssh-add /temp/.ssh/id_rsa
cd /temp
git add --ignore-errors /temp/
git commit -m "from update.sh" -q
# commits from init service only
git push -f origin master -q


# enable service
systemctl enable mitmproxy



# uninstall virtualbox (this should always be active)
apt-get -qq purge -y virtualbox* >/dev/null



# clear stage files
apt-get -qq autoremove -y >/dev/null
apt-get -qq autoclean -y >/dev/null


# k5shao startup script
su k5shao -c "
cp /temp/user_startup.sh /home/k5shao/.config/autostart-scripts/user_startup.sh
chmod 744 /home/k5shao/.config/autostart-scripts/user_startup.sh"



# restore
usermod -p '!' root
deluser k5shao sudo



# reboot
if [ "${1:-None}" != "test" ]
then
    reboot
fi


