#!/bin/sh

python -m venv venv
source venv/bin/activate
pip install flask openpyxl
python api/index.py
