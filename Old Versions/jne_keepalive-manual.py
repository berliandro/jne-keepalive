import time
import requests

# 1. Configuration
TARGET_URL = "https://css.jne.co.id/"
COOKIE_NAME = "ci_session" 
COOKIE_VALUE = "PASTE_HERE" 

COOKIES = {COOKIE_NAME: COOKIE_VALUE}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def keep_alive_jne():
    print("Starting JNE Keep-Alive script...")
    print("Press Ctrl+C to stop.\n")

    while True:
        try:
            response = requests.get(TARGET_URL, cookies=COOKIES, headers=HEADERS, timeout=10)
            
            # Check if the server accepted the cookie or bounced back to the login page
            if "login" in response.url.lower():
                print(f"[{time.strftime('%H:%M:%S')}] WARNING: Redirected to login. Session expired or incorrect cookie value.")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] Heartbeat sent! Server response: {response.status_code}")
                
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Network error: {e}")
            
        time.sleep(180)  # Ping every 3 minutes

if __name__ == "__main__":
    try:
        keep_alive_jne()
    except KeyboardInterrupt:
        print("\nScript stopped by user.")
    finally:
        input("\nPress Enter to exit...")