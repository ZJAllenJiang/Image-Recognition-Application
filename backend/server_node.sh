#!/bin/sh

# get updated list
sudo apt-get update

# install pip3 and ensure python3 version>= 3.5
sudo apt install python3-pip

# install torch, torchvision and PIL module
sudo pip3 install torch==1.3.1+cpu torchvision==0.4.2+cpu -f https://download.pytorch.org/whl/torch_stable.html

# create folder to put server code
sudo mkdir /geni
sudo mkdir /geni/server

# get code from github

sudo wget -P /geni/server https://raw.githubusercontent.com/ZJAllenJiang/Image-Recognition-Application/master/backend/image_server.py
sudo wget -P /geni/server https://raw.githubusercontent.com/ZJAllenJiang/Image-Recognition-Application/master/backend/api.py
sudo wget -P /geni/server https://raw.githubusercontent.com/ZJAllenJiang/Image-Recognition-Application/master/backend/imagenet_class_index.json

# start server on server node
python3 /geni/server/api.py
python3 /geni/server/image_server.py

