#!/bin/sh

python -m venv venv
source venv/bin/activate
pip install flask
python api/index.py
