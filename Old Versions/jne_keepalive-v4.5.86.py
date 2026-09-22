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

# --- Configuration ---
TARGET_URL = "https://css.jne.co.id/beranda"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36 Edg/153.0.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://css.jne.co.id/"
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_header():
    clear_screen()
    title = Text("🚀 JNE CSS KEEP-ALIVE (DIAGNOSTIC MODE)", justify="center", style="bold white")
    subtitle = Text("Debugging server response", justify="center", style="dim white")
    title.append("\n")
    title.append(subtitle)
    console.print(Panel(title, border_style="cyan", padding=(1, 2)))

def run_diagnostics():
    draw_header()
    
    console.print("\n[dim]Check your browser DevTools for these values:[/]")
    ci_val = Prompt.ask("[bold green]?[/] Paste your [bold yellow]ci_session[/] value").strip()
    csrf_val = Prompt.ask("[bold green]?[/] Paste your [bold yellow]CSRF_TOKEN[/] value").strip()
    
    if not ci_val or not csrf_val:
        console.print("[red]✖ Both values are required.[/]")
        input("Press Enter to exit...")
        sys.exit(0)

    with console.status("[bold cyan]Sending test request to JNE servers...", spinner="dots"):
        try:
            test_cookies = {
                "ci_session": ci_val,
                "CSRF_TOKEN": csrf_val
            }
            response = requests.get(TARGET_URL, cookies=test_cookies, headers=HEADERS, timeout=10)
            
            console.print("\n[bold yellow]=== DIAGNOSTIC RESULTS ===[/]")
            console.print(f"Status Code: [bold cyan]{response.status_code}[/]")
            console.print(f"Final URL:   [bold cyan]{response.url}[/]")
            
            # Save the HTML to a file to see what the server ACTUALLY sent
            with open("debug_response.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            
            console.print("\n[bold green]✔ Server response saved to 'debug_response.html'[/]")
            console.print("[bold white]Please look at the console output above, and then double-click 'debug_response.html' in your folder to open it in your browser.[/]")
            
        except requests.RequestException as e:
            console.print(f"\n[bold red]✖ Network error:[/] {e}")

if __name__ == "__main__":
    try:
        run_diagnostics()
    except Exception:
        console.print_exception()
    
    input("\nPress Enter to exit diagnostic mode...")