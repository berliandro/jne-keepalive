@echo off
title JNE CSS Keep-Alive Launcher

echo Checking required Python packages...
pip install -q -r requirements.txt

echo.
echo Launching application in secure window...

:: Added 'cmd /c' and '& pause' so the window stays open if it crashes!
start "JNE Keep-Alive" conhost.exe cmd /c "python jne_keepalive-v5.stable.py & pause"

exit