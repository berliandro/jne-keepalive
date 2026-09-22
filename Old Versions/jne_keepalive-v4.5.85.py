import time
import requests
import ctypes
import os
import sys

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

console = Console()

# --- Windows API Integration ---
def disable_window_close_button():
    """Disables the 'X' close button on the classic Windows console."""
    if os.name == 'nt':
        try:
            SC_CLOSE = 0xF060
            MF_BYCOMMAND = 0x00000000
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32
            hwnd = kernel32.GetConsoleWindow()
            if hwnd:
                h_menu = user32.GetSystemMenu(hwnd, False)
                if h_menu:
                    user32.DeleteMenu(h_menu, SC_CLOSE, MF_BYCOMMAND)
        except Exception:
            pass

def native_confirm_exit():
    """Shows a native Windows MessageBox to confirm exit."""
    if os.name == 'nt':
        style = 0x04 | 0x30 | 0x100 | 0x40000
        result = ctypes.windll.user32.MessageBoxW(0, 
            "Are you sure you want to stop the JNE Keep-Alive service?\n\nIf you stop this, your session will expire.", 
            "Confirm Exit", style)
        return result == 6
    return True

# --- Configuration ---
TARGET_URL = "https://css.jne.co.id/beranda"

# Updated Headers to act exactly like Microsoft Edge (v153)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36 Edg/153.0.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9"
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_header():
    clear_screen()
    title = Text("🚀 JNE CSS KEEP-ALIVE (PROTECTED)", justify="center", style="bold white")
    subtitle = Text("Window Locked • Press Ctrl+C to Exit", justify="center", style="dim white")
    title.append("\n")
    title.append(subtitle)
    
    console.print(Panel(title, border_style="cyan", padding=(1, 2)))

def validate_session(ci_session, csrf_token):
    """Sends a test request to verify if the server accepts the cookies."""
    with console.status("[bold cyan]Verifying session with JNE servers...", spinner="dots"):
        try:
            test_cookies = {
                "ci_session": ci_session,
                "CSRF_TOKEN": csrf_token
            }
            response = requests.get(TARGET_URL, cookies=test_cookies, headers=HEADERS, timeout=10)
            
            html_content = response.text.lower()
            # FIX: Look specifically for a password input field, not just the word "password"
            if 'type="password"' in html_content or 'name="password"' in html_content:
                return False
            return True
        except requests.RequestException:
            console.print("[bold red]✖ Network error during validation. Check your connection.[/]")
            return False

def get_session_credentials():
    """Prompts for both session cookies and validates them."""
    while True:
        try:
            console.print("\n[dim]Check your browser DevTools for these values:[/]")
            ci_val = Prompt.ask("[bold green]?[/] Paste your [bold yellow]ci_session[/] value").strip()
            csrf_val = Prompt.ask("[bold green]?[/] Paste your [bold yellow]CSRF_TOKEN[/] value").strip()
            
            if not ci_val or not csrf_val:
                console.print("[red]✖ Both values are required.[/]")
                continue

            if validate_session(ci_val, csrf_val):
                return ci_val, csrf_val
            else:
                console.print("[bold red]✖ Invalid or expired session credentials.[/]")
                console.print("[dim]The server rejected them. Please refresh the JNE page, copy the newest values, and try again.[/]")
                
        except KeyboardInterrupt:
            if native_confirm_exit():
                sys.exit(0)
            draw_header()

def wait_with_spinner(seconds):
    """Shows an animated spinner during the idle wait period."""
    with console.status("[bold cyan]Monitoring...", spinner="dots") as status:
        for remaining in range(seconds, 0, -1):
            status.update(f"[bold cyan]Idle • Next heartbeat in {remaining}s[/]")
            time.sleep(1)

def keep_alive_jne():
    disable_window_close_button()
    draw_header()

    ci_session, csrf_token = get_session_credentials()
    
    COOKIES = {
        "ci_session": ci_session,
        "CSRF_TOKEN": csrf_token
    }
    
    console.print("\n[bold green]✔ Session verified and secured! Starting background service...[/]\n")

    while True:
        try:
            response = requests.get(TARGET_URL, cookies=COOKIES, headers=HEADERS, timeout=10)
            current_time = time.strftime('%H:%M:%S')
            html_content = response.text.lower()
            
            # FIX: Same specific check applied to the keep-alive loop
            if 'type="password"' in html_content or 'name="password"' in html_content:
                console.print(f"[[dim]{current_time}[/]] [bold red]⚠ Redirected to login. Session expired unexpectedly![/]")
                console.bell()
            else:
                console.print(f"[[dim]{current_time}[/]] [bold green]✔ Heartbeat sent![/] [dim](Status: {response.status_code})[/]")
            
            wait_with_spinner(180)

        except requests.RequestException as e:
            current_time = time.strftime('%H:%M:%S')
            console.print(f"[[dim]{current_time}[/]] [bold red]✖ Network error:[/] {e}")
            try:
                wait_with_spinner(180)
            except KeyboardInterrupt:
                pass 

        except KeyboardInterrupt:
            console.bell() 
            if native_confirm_exit():
                console.print("\n[bold yellow]Stopping keep-alive service. Goodbye![/]\n")
                break
            else:
                console.print("\n[bold green]✔ Exit cancelled. Resuming service...[/]\n")

if __name__ == "__main__":
    try:
        keep_alive_jne()
    except Exception:
        console.print_exception()