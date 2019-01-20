#!/usr/bin/env bash
sudo apt update
sudo apt -y upgrade
sudo apt install -y python3-pip
pip3 install dill requests_html numpy newspaper3k
python3 ./setup.py 
