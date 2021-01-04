# su
# /temp/recover.sh
apt-get install redshift
redshift -O 5000
# g for gamma
redshift -O 3000 -g .5
redshift -x
# activation code
# iris-giveaway

# remember to disable chrome address bar search suggestion

# optional installation
apt-get -qq install -y --no-install-recommends vlc

# sage
apt-get -qq install -y git m4 gfortran libssl-dev python-pip >/dev/null 
su k5shao -c "
git clone https://github.com/sagemath/sage.git -q
cd sage
git checkout mnRules -q
git pull -q
make --quiet configure
./configure --with-python=3 >/dev/null 2>&1
make --quiet -j3 >/dev/null 2>&1"

# disable wallet and install google chrome 
# not sure if still needed by root_setup.sh
su k5shao -c "
echo '[Migration]
alreadyMigrated=true

[Wallet]
Enabled=false' > /home/k5shao/.config/kwalletrc"


# virtualbox (recommends are needed for qt)
# https://www.linuxbabe.com/virtualbox/access-usb-from-virtualbox-guest-os
# to get usb access
apt-get -qq install -y virtualbox
# remove virtualbox files
apt-get -qq purge -y virtualbox* 
rm ~/"VirtualBox VMs" -Rf
rm ~/.config/VirtualBox/ -Rf





# matlab and activation
mkdir /home/k5shao/matlabTemp
mount -o loop /home/k5shao/Downloads/MatlabR2018b_LinuxX64_DVD1_downloader.ga.iso /home/k5shao/matlabTemp
/home/k5shao/matlabTemp/install
umount /home/k5shao/matlabTemp
mount -o loop /home/k5shao/Downloads/MatlabR2018b_LinuxX64_DVD2_downloader.ga.iso /home/k5shao/matlabTemp
umount /home/k5shao/matlabTemp
rmdir /home/k5shao/matlabTemp
cp /home/k5shao/Downloads/Matlab\ R2018b\ Linux64\ Crack\ Only/license_standalone.lic /usr/local/MATLAB/R2018b/licenses/
cp -f /home/k5shao/Downloads/Matlab\ R2018b\ Linux64\ Crack\ Only/bin/glnxa64/matlab_startup_plugins/lmgrimpl/libmwlmgrimpl.so /usr/local/MATLAB/R2018b/bin/glnxa64/matlab_startup_plugins/lmgrimpl/





# pwm module if needed
wget -O /temp/intelpwm.sh "https://raw.githubusercontent.com/SmartestKen/SiteInfo/master/intelpwm.sh" -q
chmod 744 /temp/intelpwm.sh

apt-get -qq install -y --no-install-recommends intel-gpu-tools >/dev/null
echo '
[Unit]
Description=LED PWM frequency 
[Service]
Type=forking
ExecStart=/temp/intelpwm.sh
Restart=on-failure
RestartSec=10
[Install]
WantedBy=graphical.target' > /etc/systemd/system/intelpwm.service

systemctl enable intelpwm 





# cleanning at the end
rm /home/k5shao/root_fresh_install.sh
/temp/update.sh


#-----------------useful command-------------------

xinput --list --short

# 17 mouse index
xinput --list-props 17
xinput --set-prop 17 "Coordinate Transformation Matrix" 1.5 0 0 0 1.5 0 0 0 1


# detect keyinput
xev
# keycode, function
xmodmap -e "keycode 135 = Prior"

# supported resolution/check video driver
# /check nvidia install/check intel_pwm value
# https://www.nvidia.com/en-us/drivers/unix/
xrandr
lshw -c video
nvidia-smi
intel_reg read 0xC8254

# get screen specs (ASCII string part) 
apt-get -qq install -y read-edid edid-decode
get-edid|edid-decode




# remove extra packages
apt -qq autoremove -y

# remove git cache (file history)
git rm -r --cached .

# get partition info and mount point
lsblk
# zero write partition (change to iso if making image, with bs=4k)
dd status=progress if=/dev/zero of=/dev/sdb bs=100M && sync  
# entire removal process, -vm for viewing, -k for killing
fuser -vmk /media/k5shao/0632-E4D1
umount /dev/sdb1
udisksctl power-off -b /dev/sdb


# Mount Iphone (use mkdir one time)
idevicepair pair
fusermount -u /home/k5shao/Iphone; rmdir /home/k5shao/Iphone; mkdir /home/k5shao/Iphone; ifuse /home/k5shao/Iphone


scanimage  --resolution 300 --format=jpeg --batch=./out%d.jpg --source 'ADF Duplex' --mode color
./magick convert out*.jpg output.pdf
./magick import ./out10.jpg
# entire screen
./magick import -window root ./out10.jpg





# give/remove password/sudo
echo 'root:123'|chpasswd
usermod -p '!' root
usermod -aG sudo k5shao
deluser k5shao sudo

# utility to adjust microphone quality
# (also check palseaudio to see if switch to headset microphone)
# in alsamixer, keep press right arrow till boost column
alsamixer
arecord -fS24_3LE -r48 test.wav

# record audio
# https://superuser.com/questions/597227/linux-arecord-capture-sound-card-output-rather-than-microphone-input
parec -d alsa_output.pci-0000_00_1f.3.analog-stereo.monitor --file-format=wav output.wav

# netstat -atunp
# dolphin fish://k5shao@ieng6.ucsd.edu:22
# https://helpmanual.io/help/certutil/

# 1. testing env (--dump-dom)
chromium-browser --headless --disable-gpu https://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt
