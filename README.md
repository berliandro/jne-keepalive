# JNE CSS Keep-Alive

Automated session keep-alive heartbeat utility for the JNE Corporate Shipping System (CSS) (https://css.jne.co.id/), built with modern terminal UI (rich) and native Windows API safety controls.

## Features
* **Automated Heartbeat**: Pings authenticated dashboard (/beranda) every 180 seconds with a live countdown spinner.
* **Instant Credential Validation**: Tests ci_session and CSRF_TOKEN against server routing before locking in.
* **Console Close Protection**: Disables classic console 'X' close button via Win32 API (conhost.exe).
* **Native Exit Interception**: Intercepts Ctrl+C to trigger a system-level Windows MessageBox confirmation dialog.
* **Browser Signature Parity**: Configured with Microsoft Edge User-Agent and headers to satisfy CodeIgniter backend checks.

## Tech Stack & Requirements
* **OS**: Windows 10 / 11
* **Runtime**: Python 3.8+
* **Dependencies**: requests, rich, PyInstaller (optional)

## Repository Structure
jne-css-keepalive/
├── jne_keepalive-v3.2.py
├── requirements.txt
├── start.bat
└── README.md

## Installation & Quick Start

### Option A: Run via Batch Launcher (Recommended)
1. Place all files (jne_keepalive-v3.2.py, requirements.txt, start.bat) in D:\! Coding\jne-css-keepalive\.
2. Double-click start.bat.

### Option B: Build Standalone Binary (.exe)
pip install pyinstaller
python -m PyInstaller --onefile jne_keepalive-v3.2.py

Find the compiled executable inside the generated dist/ folder.

## Usage Guide
1. Log into JNE CSS (https://css.jne.co.id/) using Microsoft Edge.
2. Open DevTools (F12) > Application tab > Cookies.
3. Copy ci_session and CSRF_TOKEN.
4. Run the application and paste the requested values.

## Safety & Exit Controls
* **X Button**: Disabled in legacy console host (conhost.exe).
* **Keyboard Interrupt**: Press Ctrl + C.
* **Confirmation Prompt**: Native Windows dialog asks to confirm stop (Yes/No).

## Troubleshooting
* **Invalid/Expired Credentials**: JNE session keys expire quickly. Re-login in Edge and grab fresh token values.
* **Immediate Window Close**: Launch via start.bat to force conhost.exe.
