##Sms gateway for gammu

#Instalation

see gammu config in `gammu-smsdrc`

sudo apt-get install gammu gammu-smsd

sudo chgrp dialout /dev/ttyUSB0

sudo chgrp dialout /opt/smstd/
sudo chgrp dialout /opt/smstd/log.txt

sudo usermod -a -G dialout graf

/dev/ttyUSB0 

gammu-config


sudo service gammu-smsd stop

chmod g+w /opt/smstd/log.txt