@echo off
title JNE CSS Keep-Alive Launcher

echo Checking and installing required Python packages...
pip install -q -r requirements.txt

echo.
echo Launching application in secure window...

:: Point conhost to the new v3.2 filename
start "JNE Keep-Alive" conhost.exe python jne_keepalive-v3.2.py

exit