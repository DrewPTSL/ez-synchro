#!/usr/bin/env python3
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
║                    {Colors.BOLD}Automated Traffic Simulation Processor{Colors.ENDC}{Colors.OKCYAN}                     ║
║                              {Colors.BOLD}🏁 PLAID MODE 🏁{Colors.ENDC}{Colors.OKCYAN}                              ║
║                           {Colors.BOLD}"They've gone to PLAID!"{Colors.ENDC}{Colors.OKCYAN}                          ║
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

def get_user_inputs() -> tuple[str, int, bool]:
    """Get and validate user inputs with epic styling"""
    print(f"\n{Colors.BOLD}{Colors.OKCYAN}╔══════════════════════════════════════════════════════════╗")
    print(f"║                    CONFIGURATION                         ║")
    print(f"╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
    
    # Get folder path
    default_path = r"C:"
    
    print(f"\n{Colors.BOLD}Output Directory:{Colors.ENDC}")
    print(f"  Default: {Colors.OKCYAN}{default_path}{Colors.ENDC}")
    folder_input = input(f"  → Enter path (or press ENTER for default): ").strip()
    
    folder_path = folder_input if folder_input else default_path
    
    if not validate_folder_path(folder_path):
        print(f"  {Colors.WARNING}⚠ Warning:{Colors.ENDC} Path '{folder_path}' may not exist")
        confirm = input(f"  → Continue anyway? [{Colors.OKGREEN}y{Colors.ENDC}/{Colors.FAIL}N{Colors.ENDC}]: ").lower()
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
            break
        except ValueError:
            print(f"  {Colors.FAIL}✗ Please enter a valid number{Colors.ENDC}")
    
    print(f"  {Colors.OKGREEN}✓ Will process {num_scenarios} scenario(s){Colors.ENDC}")
    
    # Ask about opening folder
    print(f"\n{Colors.BOLD}Options:{Colors.ENDC}")
    open_folder_input = input(f"  → Open output folder when complete? [{Colors.OKGREEN}Y{Colors.ENDC}/{Colors.FAIL}n{Colors.ENDC}]: ").lower()
    open_folder_after = open_folder_input != 'n'
    
    return folder_path, num_scenarios, open_folder_after

def plaid_key_burst(keys: list):
    """PLAID MODE: Instantaneous key bursts with zero delays"""
    for key in keys:
        if isinstance(key, tuple):  # For hotkeys
            pyautogui.hotkey(*key)
        else:
            pyautogui.press(key)
        # NO DELAYS - MAXIMUM PLAID SPEED!

def automate_synchro_process(folder_path: str, num_scenarios: int):
    """PLAID MODE automation - absolute theoretical maximum speed"""
    # PLAID MODE: Zero pause between operations
    pyautogui.PAUSE = 0.005  # Pushed beyond the limit - theoretical minimum
    pyautogui.FAILSAFE = True
    
    print(f"\n{Colors.BOLD}{Colors.OKCYAN}╔══════════════════════════════════════════════════════════╗")
    print(f"║                 🏁 PLAID MODE ENGAGED 🏁                 ║")
    print(f"║               THEY'VE GONE TO PLAID!                     ║")
    print(f"║           THEORETICAL MAXIMUM SPEED ACHIEVED             ║")
    print(f"╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
    print(f"{Colors.WARNING}⚠ Failsafe enabled - move mouse to corner to emergency stop{Colors.ENDC}")
    
    try:
        for scenario in range(1, num_scenarios + 1):
            start_time = time.time()
            print(f"\n{Colors.BOLD}{Colors.HEADER}┌─ PLAID Processing Scenario {scenario}/{num_scenarios} ─┐{Colors.ENDC}")
            
            step = 1
            total_steps = 8 if scenario == 1 else 9
            
            # Scenario selection for subsequent scenarios
            if scenario > 1:
                print_status(step, "Lightning scenario selection...", "info")
                pyautogui.click(-300, 110)
                time.sleep(0.05)  # Theoretical minimum for UI response
                print_progress_bar(step, total_steps)
                step += 1
                
                scenario_y = 160 + (25 * (scenario - 2))
                print_status(step, f"Instant scenario {scenario} lock...", "info")
                pyautogui.click(-300, scenario_y)
                time.sleep(0.05)  # Theoretical minimum
                print_progress_bar(step, total_steps)
                step += 1
            
            # Main automation sequence
            print_status(step, "Quantum Synchro targeting...", "info")
            pyautogui.click(-1200, 700)
            time.sleep(0.05)  # Theoretical minimum
            print_progress_bar(step, total_steps)
            step += 1
            
            print_status(step, "Ctrl+R warp speed...", "info")
            pyautogui.hotkey('ctrl', 'r')
            time.sleep(0.05)  # Theoretical minimum
            print_progress_bar(step, total_steps)
            step += 1
            
            print_status(step, "Instantaneous tab burst...", "info")
            plaid_key_burst(['tab'] * 6)  # ZERO delay key burst
            print_progress_bar(step, total_steps)
            step += 1
            
            print_status(step, "Dialog materialization...", "info")
            pyautogui.press('enter')
            time.sleep(0.8)  # Reduced but kept reasonable for dialog loading
            print_progress_bar(step, total_steps)
            step += 1
            
            # File handling
            if scenario == 1:
                print_status(step, "Directory quantum jump...", "info")
                pyautogui.hotkey('ctrl', 'l')
                time.sleep(0.02)  # Near-zero
                pyautogui.write(folder_path)
                pyautogui.press('enter')
                time.sleep(0.4)  # Optimized directory navigation
                print_progress_bar(step, total_steps)
                step += 1
                
                print_status(step, "File system wormhole...", "info")
                plaid_key_burst(['tab'] * 4)
                plaid_key_burst(['down', 'up'])
                print_progress_bar(step, total_steps)
                step += 1
                
            else:
                print_status(step, f"File {scenario} teleportation...", "info")
                pyautogui.hotkey('alt', 'd')
                time.sleep(0.02)  # Near-zero
                
                plaid_key_burst(['tab'] * 5)
                plaid_key_burst(['down'] * (scenario - 1))
                print_progress_bar(step, total_steps)
                step += 1
            
            print_status(step, "Reality finalization...", "info")
            pyautogui.press('enter')
            time.sleep(0.15)  # Aggressive but stable
            pyautogui.press('enter')
            time.sleep(0.4)   # Optimized save time
            print_progress_bar(step, total_steps)
            
            elapsed = time.time() - start_time
            print(f"\n{Colors.OKGREEN}└─ PLAID Scenario {scenario} completed in {elapsed:.2f}s ─┘{Colors.ENDC}")
        
        return True  # Success
        
    except pyautogui.FailSafeException:
        print(f"\n{Colors.WARNING}╔══════════════════════════════════════════════════════════╗")
        print(f"║  {Colors.BOLD}⚠ PLAID MODE CANCELLED BY FAILSAFE{Colors.ENDC}{Colors.WARNING}                   ║")
        print(f"║    Emergency brake applied at light speed!              ║")
        print(f"╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
        return False
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}╔══════════════════════════════════════════════════════════╗")
        print(f"║  {Colors.BOLD}⚠ PLAID MODE CANCELLED BY USER{Colors.ENDC}{Colors.WARNING}                      ║")
        print(f"║    User applied emergency brake (Ctrl+C)                ║")
        print(f"╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
        return False
    except Exception as e:
        print(f"\n{Colors.FAIL}╔══════════════════════════════════════════════════════════╗")
        print(f"║  {Colors.BOLD}✗ PLAID MODE MALFUNCTION{Colors.ENDC}{Colors.FAIL}                               ║")
        print(f"║    Error: {str(e)[:45]:<45} ║")
        print(f"╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
        return False

def main():
    """Main CLI interface with PLAID styling"""
    parser = argparse.ArgumentParser(
        description="EZSynchro - Automated Synchro Report Generator (PLAID MODE)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Colors.OKCYAN}Examples:
  ezsynchro                                    # Interactive mode
  ezsynchro --path ./reports --count 5        # Direct execution
  ezsynchro --path ./reports --count 5 --open # Open folder when done
  ezsynchro --plaid                           # MAXIMUM THEORETICAL SPEED
  
Safety Features:
  • Move mouse to any corner to emergency stop
  • Press Ctrl+C to interrupt at any time
  • Automatic failsafe protection enabled
  
🏁 PLAID MODE: Beyond ludicrous speed - theoretical maximum achieved!
   "They've gone to plaid!" - Spaceballs
   WARNING: This mode operates at the theoretical limits of automation!{Colors.ENDC}
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
        "--plaid", "-pl",
        action="store_true",
        help="Enable PLAID mode (theoretical maximum speed)"
    )
    
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Skip banner display"
    )
    
    args = parser.parse_args()
    
    # Apply PLAID mode settings
    if args.plaid:
        print(f"{Colors.WARNING}🏁 PLAID MODE ENABLED - THEY'VE GONE TO PLAID!{Colors.ENDC}")
        print(f"{Colors.WARNING}   Operating at theoretical maximum speed!{Colors.ENDC}")
    
    try:
        if not args.no_banner:
            print_banner()
        
        # Get inputs (either from args or interactive)
        if args.path and args.count:
            folder_path = args.path
            num_scenarios = args.count
            open_folder_after = args.open
            
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
            if args.plaid:
                print(f"  Mode: {Colors.WARNING}🏁 PLAID SPEED 🏁{Colors.ENDC}")
        else:
            folder_path, num_scenarios, open_folder_after = get_user_inputs()
        
        print(f"\n{Colors.BOLD}Ready to engage PLAID drive.{Colors.ENDC}")
        print(f"{Colors.WARNING}Ensure Synchro application is visible and accessible.{Colors.ENDC}")
        
        try:
            input(f"\n{Colors.BOLD}Press ENTER to go PLAID or Ctrl+C to cancel...{Colors.ENDC}")
            # No countdown - INSTANT PLAID!
            print(f"{Colors.OKGREEN}🏁 ENGAGING PLAID DRIVE NOW! 🏁{Colors.ENDC}")
            
            start_total = time.time()
            success = automate_synchro_process(folder_path, num_scenarios)
            total_elapsed = time.time() - start_total
            
            if success:
                # PLAID success message
                scenarios_per_second = num_scenarios / total_elapsed
                print(f"\n{Colors.OKGREEN}╔════════════════════════════════════════════════════════════╗")
                print(f"║  {Colors.BOLD}🏁 PLAID MISSION ACCOMPLISHED - MAXIMUM WARP 🏁{Colors.ENDC}{Colors.OKGREEN}           ║")
                print(f"║    Generated {num_scenarios} report(s) in {total_elapsed:.1f} seconds                     ║")
                print(f"║    Average: {total_elapsed/num_scenarios:.1f}s per scenario                            ║")
                print(f"║    PLAID Speed: {scenarios_per_second:.1f} scenarios/second                      ║")
                if total_elapsed/num_scenarios < 2.0:
                    print(f"║    🏆 SUB-2-SECOND ACHIEVEMENT UNLOCKED! 🏆              ║")
                print(f"║    Output: {folder_path[:35]:<35}             ║")
                print(f"╚════════════════════════════════════════════════════════════╝{Colors.ENDC}")
                
                # Open folder if requested
                if open_folder_after:
                    print(f"\n{Colors.OKBLUE}Opening output folder at light speed...{Colors.ENDC}")
                    if open_folder(folder_path):
                        print(f"{Colors.OKGREEN}✓ Folder opened successfully{Colors.ENDC}")
                    
        except KeyboardInterrupt:
            print(f"\n{Colors.FAIL}╔══════════════════════════════════════╗")
            print(f"║  {Colors.BOLD}✗ PLAID CANCELLED{Colors.ENDC}{Colors.FAIL}                     ║")
            print(f"║    User aborted PLAID sequence       ║")
            print(f"╚══════════════════════════════════════╝{Colors.ENDC}")
            sys.exit(0)
        
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}PLAID disengaged! 🏁{Colors.ENDC}")
        sys.exit(0)

if __name__ == "__main__":
    main()
