#!/usr/bin/env bash
source "./venv/bin/activate"
python -m pip install -r requirements.txt 2>/dev/null >/dev/null
python scheduler.py
