#!/bin/bash

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    python3 -m pip install -r requirements.txt
fi

source .venv/bin/activate
python run.py
deactivate