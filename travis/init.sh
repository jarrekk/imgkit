#!/usr/bin/env bash

sudo apt-get install -y openssl build-essential xorg libssl-dev
wget https://downloads.wkhtmltopdf.org/0.12/0.12.4/wkhtmltox-0.12.4.tar.bz2
tar -xf wkhtmltox-0.12.3_linux-generic-amd64.tar.xz
cd wkhtmltox
sudo chown root:root bin/wkhtmltopdf
sudo cp -r * /usr/
