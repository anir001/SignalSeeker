@echo off
call venv\Scripts\activate.bat
python --version

call python main.py
cmd /k