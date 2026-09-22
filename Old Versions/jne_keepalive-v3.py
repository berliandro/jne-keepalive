import time
import requests
import ctypes
import os
import sys

# Rich UI components
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text

console = Console()

# --- Windows API Integration ---
def disable_window_close_button():
    """Disables the 'X' close button on the Windows console."""
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

# --- Configuration ---
TARGET_URL = "https://css.jne.co.id/"
COOKIE_NAME = "ci_session"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_header():
    clear_screen()
    title = Text("🚀 JNE CSS KEEP-ALIVE (PROTECTED)", justify="center", style="bold white")
    subtitle = Text("Window Locked • Ctrl+C to Exit", justify="center", style="dim white")
    title.append("\n")
    title.append(subtitle)
    
    console.print(Panel(title, border_style="cyan", padding=(1, 2)))

def wait_with_spinner(seconds):
    """Shows an animated spinner and countdown timer."""
    with console.status("[bold cyan]Initializing...", spinner="dots") as status:
        for remaining in range(seconds, 0, -1):
            status.update(f"[bold cyan]Idle • Next heartbeat in {remaining}s[/]")
            time.sleep(1)

def keep_alive_jne():
    disable_window_close_button()
    draw_header()

    # Prompt for session ID with modern UI
    while True:
        try:
            cookie_value = Prompt.ask(f"[bold green]?[/] Please paste your [bold yellow]{COOKIE_NAME}[/] value")
            if cookie_value.strip():
                break
            console.print("[red]✖ Session ID cannot be empty.[/]")
        except KeyboardInterrupt:
            console.print("\n")
            if Confirm.ask("[bold red]⚠ Abort setup and exit?[/]"):
                sys.exit(0)
            draw_header()

    COOKIES = {COOKIE_NAME: cookie_value.strip()}
    console.print("\n[bold green]✔ Session secured! Starting background service...[/]\n")

    while True:
        try:
            # 1. Send the heartbeat
            response = requests.get(TARGET_URL, cookies=COOKIES, headers=HEADERS, timeout=10)
            current_time = time.strftime('%H:%M:%S')
            
            if "login" in response.url.lower():
                console.print(f"[[dim]{current_time}[/]] [bold red]⚠ Redirected to login. Session expired![/]")
            else:
                console.print(f"[[dim]{current_time}[/]] [bold green]✔ Heartbeat sent![/] [dim](Status: {response.status_code})[/]")
            
            # 2. Wait with modern animated spinner (180 seconds)
            wait_with_spinner(180)

        except requests.RequestException as e:
            current_time = time.strftime('%H:%M:%S')
            console.print(f"[[dim]{current_time}[/]] [bold red]✖ Network error:[/] {e}")
            try:
                wait_with_spinner(180)
            except KeyboardInterrupt:
                pass # Handled by the block below

        except KeyboardInterrupt:
            console.print("\n")
            # 3. Intercept exit attempt with modern confirmation prompt
            console.bell() # Plays the Windows alert sound
            if Confirm.ask("[bold red]⚠ INTERCEPT: Are you sure you want to stop the service?[/]"):
                console.print("[bold yellow]Stopping keep-alive service. Goodbye![/]\n")
                break
            else:
                console.print("[bold green]✔ Exit cancelled. Resuming service...[/]\n")

if __name__ == "__main__":
    try:
        keep_alive_jne()
    except Exception as e:
        console.print_exception()
        input("Press Enter to exit...")