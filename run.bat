@echo off

if not exist ".venv" (
    python -m venv .venv
    call .venv\Scripts\activate.bat
    python -m pip install -r requirements.txt
)

call .venv\Scripts\activate.bat
python run.py
deactivate