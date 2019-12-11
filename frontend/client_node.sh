#!/bin/sh

sudo apt update  

sudo apt install apache2  

sudo a2enmod cgi

sudo systemctl restart apache2

sudo wget -P /etc/apache2/conf-available https://raw.githubusercontent.com/ZJAllenJiang/Image-Recognition-Application/master/frontend/cgi-enabled.conf

sudo mkdir /var/www/html/cgi-enabled

sudo a2enmod cgi-enabled

sudo systemctl restart apache2

sudo wget -P /var/www/html https://raw.githubusercontent.com/ZJAllenJiang/Image-Recognition-Application/master/frontend/upload.html

sudo chmod 755 /var/www/html/upload.html

sudo wget -P /var/www/html/cgi-enabled https://raw.githubusercontent.com/ZJAllenJiang/Image-Recognition-Application/master/frontend/client.py

sudo chmod 755 /var/www/html/cgi-enabled/client.py

sudo chmod 777 /var/www/html/cgi-enabled

