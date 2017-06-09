#!/usr/bin/env bash

sudo wget https://github.com/jgm/pandoc/releases/download/1.19.2.1/pandoc-1.19.2.1-1-amd64.deb
sudo dpkg -i pandoc-1.19.2.1-1-amd64.deb
pip install pypandoc