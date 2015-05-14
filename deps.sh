#!/bin/sh

sudo aptitude install -y libfprint-dev
sudo aptitude install -y python3-cffi
sudo aptitude install -y python3-pymongo
git clone https://github.com/franciscod/pyfprint-cffi.git

