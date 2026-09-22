@echo off
title JNE CSS Keep-Alive Launcher

echo Checking and installing required Python packages...
pip install -r requirements.txt

echo.
echo Launching application...
python jne_keepalive.py

:: If the app closes or crashes, this pause keeps the terminal open so you can read any errors.
pause