#!/usr/bin/env bash

LATEST_VERSION="v1.3.0"

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)";
echo '# Set PATH, MANPATH, etc., for Homebrew.' >> /Users/$USER/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/$USER/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
brew install python;
brew install media-info;
brew install node;
curl -L https://github.com/Virtuality360/VideoPipeline/releases/download/$LATEST_VERSION/Upload.zip > ~/Downloads/videoUploader.zip;
sudo unzip ~/Downloads/videoUploader.zip -d /usr/local/bin/;
sudo touch /usr/local/bin/Upload/.env;
sudo echo "AWS_ACCESS_KEY_ID=" >> Upload/.env;
sudo echo "AWS_SECRET_ACCESS_KEY=" >> Upload/.env;
sudo echo "PGUSER=" >> Upload/.env;
sudo echo "PGPASSWORD=" >> Upload/.env;
sudo echo "PGDATABSE=v360psql" >> Upload/.env;
sudo echo "PGHOST=db1.server.internal" >> Upload/.env;
sudo echo "PGPORT=5432" >> Upload/.env;
python3 -m pip install --upgrade pip;
pip3 install -r /usr/local/bin/Upload/requirements.txt;
echo "export PATH=$PATH:/usr/local/bin/Upload/)" >> /Users/$USER/.zshrc;
curl https://owncloud.myaesportal.com/s/evlhxLrYMoXzvx8/download --output ~/Downloads/Extract-me-app-pipeline.zip;
sudo unzip ~/Downloads/Extract-me-app-pipeline.zip -d ~;

echo "\n";
echo "Now open /usr/local/bin/Upload/.env to enter the credentials for minio and postgres.";
echo "In a terminal, go to ~/Downloads/extract-me-prod/src and run npm i as well as npm start"
echo "Afterwards, you can run the upload script with Upload/upload.py"