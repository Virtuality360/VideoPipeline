#!/usr/bin/env bash

LATEST_VERSION="v1.3.0";

curl -L https://github.com/Virtuality360/VideoPipeline/releases/download/$LATEST_VERSION/Upload.zip > ~/Downloads/videoUploader.zip;
sudo unzip ~/Downloads/videoUploader.zip -d ~/Downloads/;
sudo mv ~/Downloads/Upload/upload.py /usr/local/bin/Upload/upload.py;
sudo rm -rf ~/Downloads/Upload.zip ~/Downloads/Upload/