@echo off

if not exist ".venv" (
    python -m venv .venv
    python -m pip install -r requirements.txt
)

call .venv\Scripts\activate.bat
python main.py
deactivate