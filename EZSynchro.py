"""
EZSynchro - Automated Synchro Report Generator
A sleek CLI tool for streamlined traffic simulation automation
"""

import pyautogui
import time
import sys
import os
import subprocess
import platform
from pathlib import Path
import argparse
from datetime import datetime
from typing import Optional

# ANSI color codes for styling
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    """Display the epic EZSynchro banner"""
    banner = f"""
{Colors.OKCYAN}╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  {Colors.BOLD}███████╗███████╗███████╗██╗   ██╗███╗   ██╗ ██████╗██╗  ██╗██████╗  ██████╗{Colors.ENDC}{Colors.OKCYAN}  ║
║  {Colors.BOLD}██╔════╝╚══███╔╝██╔════╝╚██╗ ██╔╝████╗  ██║██╔════╝██║  ██║██╔══██╗██╔═══██╗{Colors.ENDC}{Colors.OKCYAN} ║
║  {Colors.BOLD}█████╗    ███╔╝ ███████╗ ╚████╔╝ ██╔██╗ ██║██║     ███████║██████╔╝██║   ██║{Colors.ENDC}{Colors.OKCYAN} ║
║  {Colors.BOLD}██╔══╝   ███╔╝  ╚════██║  ╚██╔╝  ██║╚██╗██║██║     ██╔══██║██╔══██╗██║   ██║{Colors.ENDC}{Colors.OKCYAN} ║
║  {Colors.BOLD}███████╗███████╗███████║   ██║   ██║ ╚████║╚██████╗██║  ██║██║  ██║╚██████╔╝{Colors.ENDC}{Colors.OKCYAN} ║
║  {Colors.BOLD}╚══════╝╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝{Colors.ENDC}{Colors.OKCYAN}  ║
║                                                                               ║
║                        {Colors.BOLD}Automated Report Printer{Colors.ENDC}{Colors.OKCYAN}                               ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
    print(banner)

def print_status(step, message, status="info"):
    """Print formatted status messages with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # Include milliseconds
    
    if status == "info":
        color = Colors.OKBLUE
        icon = "🏁"
    elif status == "success":
        color = Colors.OKGREEN
        icon = "✓"
    elif status == "warning":
        color = Colors.WARNING
        icon = "⚠"
    elif status == "error":
        color = Colors.FAIL
        icon = "✗"
    else:
        color = Colors.ENDC
        icon = "•"
    
    print(f"{Colors.BOLD}[{timestamp}]{Colors.ENDC} {color}{icon} Step {step}:{Colors.ENDC} {message}")

def print_progress_bar(current, total, width=50):
    """Display a sleek progress bar"""
    progress = int((current / total) * width)
    bar = "█" * progress + "░" * (width - progress)
    percentage = int((current / total) * 100)
    print(f"\r{Colors.OKCYAN}Progress: [{bar}] {percentage}%{Colors.ENDC}", end="", flush=True)

def countdown(seconds, message="Starting"):
    """Animated countdown with style"""
    for i in range(seconds, 0, -1):
        print(f"\r{Colors.WARNING}{message} in {i} seconds...{Colors.ENDC}", end="", flush=True)
        time.sleep(1)
    print(f"\r{Colors.OKGREEN}{message} now!{Colors.ENDC}" + " " * 30)

def open_folder(folder_path: str):
    """Open folder in system file manager"""
    try:
        system = platform.system()
        if system == "Windows":
            os.startfile(folder_path)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", folder_path])
        elif system == "Linux":
            subprocess.run(["xdg-open", folder_path])
        else:
            print(f"{Colors.WARNING}⚠ Cannot open folder on {system} system{Colors.ENDC}")
            return False
        return True
    except Exception as e:
        print(f"{Colors.WARNING}⚠ Failed to open folder: {e}{Colors.ENDC}")
        return False

def validate_folder_path(path: str) -> bool:
    """Validate if the folder path exists"""
    return Path(path).exists() and Path(path).is_dir()

def get_user_inputs() -> tuple[str, int, bool, bool]:
    """Get and validate user inputs """
    print(f"\n{Colors.BOLD}{Colors.OKCYAN}╔══════════════════════════════════════════════════════════╗")
    print(f"║                    CONFIGURATION                         ║")
    print(f"╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
    
    # Get folder path
    default_path = r"C:\Users\DrewCobean\OneDrive - Paradigm\Desktop\Synchro"
    
    print(f"\n{Colors.BOLD}Output Directory:{Colors.ENDC}")
    print(f"  Default: {Colors.OKCYAN}{default_path}{Colors.ENDC}")
    folder_input = input(f"  → Enter path (or press ENTER for default): ").strip()
    
    folder_path = folder_input if folder_input else default_path
    
    if not validate_folder_path(folder_path):
        print(f"  {Colors.WARNING}⚠ Warning:{Colors.ENDC} Path '{folder_path}' may not exist")
        confirm = input(f"  → Continue anyway? [{Colors.OKGREEN}y{Colors.ENDC}/{Colors.FAIL}n{Colors.ENDC}]: ").lower()
        if confirm != 'y':
            print(f"\n{Colors.FAIL}╔══════════════════════════════════════╗")
            print(f"║  {Colors.BOLD}✗ OPERATION CANCELLED{Colors.ENDC}{Colors.FAIL}               ║")
            print(f"║    Invalid path specified            ║")
            print(f"╚══════════════════════════════════════╝{Colors.ENDC}")
            sys.exit(1)
    else:
        print(f"  {Colors.OKGREEN}✓ Valid path confirmed{Colors.ENDC}")
    
    # Get number of scenarios
    print(f"\n{Colors.BOLD}Scenario Count:{Colors.ENDC}")
    while True:
        try:
            num_input = input("  → Number of scenarios to process: ")
            num_scenarios = int(num_input)
            if num_scenarios <= 0:
                print(f"  {Colors.FAIL}✗ Number must be positive!{Colors.ENDC}")
                continue
            elif num_scenarios > 16:
                print(f"  {Colors.FAIL}✗ Can only handle up to 16 scenarios!{Colors.ENDC}")
                continue
            break
            
        
        except ValueError:
            print(f"  {Colors.FAIL}✗ Please enter a valid number{Colors.ENDC}")
    
    print(f"  {Colors.OKGREEN}✓ Will process {num_scenarios} scenario(s){Colors.ENDC}")

    # PDF export option
    print(f"\n{Colors.BOLD}Export Format:{Colors.ENDC}")
    txt_input = input(f"  → Export as .txt? [{Colors.OKGREEN}y{Colors.ENDC}/{Colors.FAIL}n{Colors.ENDC}]: ").lower()
    export_pdf = txt_input == 'n'

    if export_pdf:
        print(f"  {Colors.OKGREEN}✓ PDF export enabled{Colors.ENDC}")
    else:
        print(f"  {Colors.OKGREEN}✓ .txt export{Colors.ENDC}")
    
    # Ask about opening folder
    print(f"\n{Colors.BOLD}Options:{Colors.ENDC}")
    open_folder_input = input(f"  → Open output folder when complete? [{Colors.OKGREEN}y{Colors.ENDC}/{Colors.FAIL}n{Colors.ENDC}]: ").lower()
    open_folder_after = open_folder_input != 'n'
    
    return folder_path, num_scenarios, open_folder_after, export_pdf

def key_burst(keys: list):
    """Key bursts with zero delays"""
    for key in keys:
        if isinstance(key, tuple):  # For hotkeys
            pyautogui.hotkey(*key)
        else:
            pyautogui.press(key)

def automate_synchro_process(folder_path: str, num_scenarios: int, export_pdf: bool = False):
    """Synchro report processing automation"""
    pyautogui.PAUSE = 0.005  
    pyautogui.FAILSAFE = True

    tab_count = 10 if export_pdf else 6
    final_sleep = 20 if export_pdf else 0.4
    extra_sleep = 1 if export_pdf else 0

    print(f"{Colors.WARNING}⚠ Failsafe enabled - move mouse to corner to emergency stop{Colors.ENDC}")
    
    try:
        for scenario in range(1, num_scenarios + 1):
            start_time = time.time()
            print(f"\n{Colors.BOLD}{Colors.HEADER}┌─ Processing Scenario {scenario}/{num_scenarios} ─┐{Colors.ENDC}")
            
            step = 1
            total_steps = 8 if scenario == 1 else 9
            
            # Scenario selection for subsequent scenarios
            if scenario > 1:
                print_status(step, "Selecting scenario...", "info")
                pyautogui.click(-300, 110)
                time.sleep(0.05)
                print_progress_bar(step, total_steps)
                step += 1
                
                scenario_y = 160 + (25 * (scenario - 2))
                print_status(step, f"Selecting scenario {scenario}...", "info")
                pyautogui.click(-300, scenario_y)
                time.sleep(0.05)  
                print_progress_bar(step, total_steps)
                step += 1
            
            # Main automation sequence
            print_status(step, "Clicking Synchro interface...", "info")
            pyautogui.click(-1200, 700)
            time.sleep(0.05)  
            print_progress_bar(step, total_steps)
            step += 1
            
            print_status(step, "Opening create report menu...", "info")
            pyautogui.hotkey('ctrl', 'r')
            time.sleep(0.05)  
            print_progress_bar(step, total_steps)
            step += 1
            
            print_status(step, "Navigating report interface...", "info")
            key_burst(['tab'] * tab_count) 
            print_progress_bar(step, total_steps)
            step += 1
            
            print_status(step, "Opening export dialog...", "info")
            pyautogui.press('enter')
            time.sleep(0.8+extra_sleep)
            print_progress_bar(step, total_steps)
            step += 1
            
            # File handling
            if scenario == 1:
                print_status(step, "Setting output directory...", "info")
                pyautogui.hotkey('ctrl', 'l')
                time.sleep(0.02)  
                pyautogui.write(folder_path)
                pyautogui.press('enter')
                time.sleep(0.4)  
                print_progress_bar(step, total_steps)
                step += 1
                
                print_status(step, "Navigating directory...", "info")
                key_burst(['f6'] * 3)
                key_burst(['down', 'up'])
                print_progress_bar(step, total_steps)
                step += 1
                
            else:
                print_status(step, f"Selecting file {scenario}...", "info")
                pyautogui.hotkey('alt', 'd')
                time.sleep(0.02)  
                
                key_burst(['f6'] * 3)
                key_burst(['down'] * (scenario - 1))
                print_progress_bar(step, total_steps)
                step += 1
            
            print_status(step, f"{'Processing PDF export' if export_pdf else 'Processing .txt export'}...", "info")
            pyautogui.press('enter')
            time.sleep(0.15)
            if export_pdf:
                time.sleep(0.15)  
                key_burst(['left'])
                time.sleep(0.15)  
            pyautogui.press('enter')
            time.sleep(final_sleep)   
            print_progress_bar(step, total_steps)
            
            elapsed = time.time() - start_time
            print(f"\n{Colors.OKGREEN}└─ Scenario {scenario} completed in {elapsed:.2f}s ─┘{Colors.ENDC}")
        
        return True  # Success
        
    except pyautogui.FailSafeException:
        print(f"\n{Colors.WARNING}╔══════════════════════════════════════════════════════════╗")
        print(f"║  {Colors.BOLD}⚠ AUTOMATION STOPPED BY FAILSAFE{Colors.ENDC}{Colors.WARNING}                   ║")
        print(f"╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
        return False
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}╔══════════════════════════════════════════════════════════╗")
        print(f"║  {Colors.BOLD}⚠ AUTOMATION CANCELLED BY USER{Colors.ENDC}{Colors.WARNING}                      ║")
        print(f"║    User stopped process (Ctrl+C)                ║")
        print(f"╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
        return False
    except Exception as e:
        print(f"\n{Colors.FAIL}╔══════════════════════════════════════════════════════════╗")
        print(f"║  {Colors.BOLD}✗ AUTOMATION ERROR{Colors.ENDC}{Colors.FAIL}                               ║")
        print(f"║    Error: {str(e)[:45]:<45} ║")
        print(f"╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
        return False

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="EZSynchro - Automated Synchro Report Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Colors.OKCYAN}Examples:
  ezsynchro                                    # Interactive mode
  ezsynchro --path ./reports --count 5        # Direct execution
  ezsynchro --path ./reports --count 5 --open # Open folder when done
  ezsynchro --peed                           # High speed mode
  ezsynchro --pdf                             # Expor as .pdf
  
Safety Features:
  • Move mouse to any corner to emergency stop
  • Press Ctrl+C to interrupt at any time
  • Automatic failsafe protection enabled
  
{Colors.ENDC}
        """
    )
    
    parser.add_argument(
        "--path", "-p",
        help="Folder path for saving reports",
        default=None
    )
    
    parser.add_argument(
        "--count", "-c",
        type=int,
        help="Number of scenarios to process",
        default=None
    )
    
    parser.add_argument(
        "--open", "-o",
        action="store_true",
        help="Open output folder when complete"
    )
    
    parser.add_argument(
        "--speed", "-sp",
        action="store_true",
        help="Enable high-speed mode"
    )
    
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Skip banner display"
    )

    parser.add_argument(
    "--pdf",
    action="store_true",
    help="Export as .pdf instead of .txt (longer processing time)"
    )
    
    args = parser.parse_args()
    
    # Apply high speed mode
    if args.speed:
        print(f"{Colors.WARNING}🚀 HIGH SPEED MODE ENABLED{Colors.ENDC}")
    
    try:
        if not args.no_banner:
            print_banner()
        
        # Get inputs (either from args or interactive)
        if args.path and args.count:
            folder_path = args.path
            num_scenarios = args.count
            open_folder_after = args.open
            export_pdf = args.pdf
            
            if not validate_folder_path(folder_path):
                print(f"\n{Colors.FAIL}╔══════════════════════════════════════╗")
                print(f"║  {Colors.BOLD}✗ INVALID PATH SPECIFIED{Colors.ENDC}{Colors.FAIL}             ║")
                print(f"║    Path does not exist or inaccessible ║")
                print(f"╚══════════════════════════════════════╝{Colors.ENDC}")
                sys.exit(1)
                
            print(f"\n{Colors.OKGREEN}✓ Command-line configuration accepted{Colors.ENDC}")
            print(f"  Path: {Colors.OKCYAN}{folder_path}{Colors.ENDC}")
            print(f"  Scenarios: {Colors.OKCYAN}{num_scenarios}{Colors.ENDC}")
            print(f"  Open folder: {Colors.OKCYAN}{'Yes' if open_folder_after else 'No'}{Colors.ENDC}")
            if args.speed:
                print(f"  Mode: {Colors.WARNING}🚀 HIGH SPEED 🚀{Colors.ENDC}")
        else:
            folder_path, num_scenarios, open_folder_after, export_pdf = get_user_inputs()
        
        print(f"\n{Colors.BOLD}Ready to start automation.{Colors.ENDC}")
        print(f"{Colors.WARNING}Ensure Synchro application is visible and accessible.{Colors.ENDC}")
        
        try:
            input(f"\n{Colors.BOLD}Press ENTER to begin or Ctrl+C to cancel...{Colors.ENDC}")
            print(f"{Colors.OKGREEN}🚀 Starting automation process... 🚀{Colors.ENDC}")
            
            start_total = time.time()
            success = automate_synchro_process(folder_path, num_scenarios, export_pdf)
            total_elapsed = time.time() - start_total
            
            if success:
                #  success message
                #scenarios_per_second = num_scenarios / total_elapsed
                print(f"\n{Colors.OKGREEN}╔════════════════════════════════════════════════════════════╗")
                print(f"║  {Colors.BOLD}🚀 AUTOMATION COMPLETED SUCCESSFULLY 🚀{Colors.ENDC}{Colors.OKGREEN}                ║")
                print(f"║    Generated {num_scenarios} report(s) in {total_elapsed:.1f} seconds                    ║")
                print(f"║    Output: {folder_path[:35]:<35}             ║")
                print(f"╚════════════════════════════════════════════════════════════╝{Colors.ENDC}")
                
                # Open folder if requested
                if open_folder_after:
                    print(f"\n{Colors.OKBLUE}Opening output folder...{Colors.ENDC}")
                    if open_folder(folder_path):
                        print(f"{Colors.OKGREEN}✓ Folder opened successfully{Colors.ENDC}")
                    
        except KeyboardInterrupt:
            print(f"\n{Colors.FAIL}╔══════════════════════════════════════╗")
            print(f"║  {Colors.BOLD}✗ AUTOMATION CANCELLED{Colors.ENDC}{Colors.FAIL}                     ║")
            print(f"║    User aborted process       ║")
            print(f"╚══════════════════════════════════════╝{Colors.ENDC}")
            sys.exit(0)
        
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Automation Cancelled! 🚀{Colors.ENDC}")
        sys.exit(0)

if __name__ == "__main__":
    main()
