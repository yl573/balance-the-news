#!/usr/bin/env bash
git clone https://github.com/yl573/balance-the-news.git
cd balance-the-news
sudo apt update
sudo apt install -y python3-pip
pip3 install dill requests_html numpy newspaper3k
python3 ./setup.py 
# tmux new -s right python3 extract.py right