import time
import requests
import traceback
import rookiepy

def keep_alive_jne():
    target_domain = "jne.co.id" 
    target_url = "https://css.jne.co.id/" 
    
    print(f"Attempting to grab Edge cookies for {target_domain} using rookiepy...")
    
    try:
        # Extract cookies using rookiepy
        raw_cookies = rookiepy.edge(domains=[target_domain])
        
        # Convert to format requests can use
        session_cookies = {cookie['name']: cookie['value'] for cookie in raw_cookies}
        
        if not session_cookies:
             print("\n[ERROR] No JNE cookies found. Are you logged in on Edge?")
             return
             
        print("\nSuccessfully grabbed Edge session! Starting heartbeat loop...")
    except Exception as e:
        print("\n[ERROR] Failed to get cookies. Detailed error below:")
        traceback.print_exc()
        return

    while True:
        try:
            # Send heartbeat with the extracted dictionary
            response = requests.get(target_url, cookies=session_cookies, timeout=10)
            
            if "login" in response.url.lower():
                print(f"[{time.strftime('%H:%M:%S')}] WARNING: Redirected to login. Session expired.")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] Heartbeat sent. Server sees you as active.")
                
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Network error: {e}")
            
        time.sleep(180)

if __name__ == "__main__":
    try:
        keep_alive_jne()
    except KeyboardInterrupt:
        print("\nScript stopped by user.")
    finally:
        input("\nPress Enter to close this window...")