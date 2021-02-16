#!/bin/bash

wget https://www.statmt.org/europarl/v7/es-en.tgz
wget https://www.statmt.org/europarl/v7/de-en.tgz
tar -xzf de-en.tgz
tar -xzf es-en.tgz

python3 funny_script.py
