import pyautogui
import time
import sys
from datetime import datetime

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
    """Display a cool banner"""
    banner = f"""
{Colors.OKCYAN}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║  {Colors.BOLD}███████╗██╗   ██╗███╗   ██╗ ██████╗██╗  ██╗██████╗  ██████╗{Colors.ENDC}{Colors.OKCYAN}  ║
║  {Colors.BOLD}██╔════╝╚██╗ ██╔╝████╗  ██║██╔════╝██║  ██║██╔══██╗██╔═══██╗{Colors.ENDC}{Colors.OKCYAN} ║
║  {Colors.BOLD}███████╗ ╚████╔╝ ██╔██╗ ██║██║     ███████║██████╔╝██║   ██║{Colors.ENDC}{Colors.OKCYAN} ║
║  {Colors.BOLD}╚════██║  ╚██╔╝  ██║╚██╗██║██║     ██╔══██║██╔══██╗██║   ██║{Colors.ENDC}{Colors.OKCYAN} ║
║  {Colors.BOLD}███████║   ██║   ██║ ╚████║╚██████╗██║  ██║██║  ██║╚██████╔╝{Colors.ENDC}{Colors.OKCYAN} ║
║  {Colors.BOLD}╚══════╝   ╚═╝   ╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝{Colors.ENDC}{Colors.OKCYAN}  ║
║                                                               ║
║                    {Colors.BOLD}Automated Workflow Tool{Colors.ENDC}{Colors.OKCYAN}                    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
    print(banner)

def print_status(step, message, status="info"):
    """Print formatted status messages"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if status == "info":
        color = Colors.OKBLUE
        icon = "ℹ"
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
    """Display a progress bar"""
    progress = int((current / total) * width)
    bar = "█" * progress + "░" * (width - progress)
    percentage = int((current / total) * 100)
    print(f"\r{Colors.OKCYAN}Progress: [{bar}] {percentage}%{Colors.ENDC}", end="", flush=True)

def countdown(seconds, message="Starting"):
    """Animated countdown"""
    for i in range(seconds, 0, -1):
        print(f"\r{Colors.WARNING}{message} in {i} seconds...{Colors.ENDC}", end="", flush=True)
        time.sleep(1)
    print(f"\r{Colors.OKGREEN}{message} now!{Colors.ENDC}" + " " * 20)

def automate_synchro_process():
    """Enhanced Synchro automation with progress tracking"""
    pyautogui.PAUSE = 0.5
    pyautogui.FAILSAFE = True
    
    total_steps = 8
    
    try:
        print_status(1, "Targeting Synchro window...", "info")
        pyautogui.click(-1200, 700)
        time.sleep(1)
        print_progress_bar(1, total_steps)
        time.sleep(0.5)
        
        print_status(2, "Executing Ctrl+R command...", "info")
        pyautogui.hotkey('ctrl', 'r')
        time.sleep(1)
        print_progress_bar(2, total_steps)
        time.sleep(0.5)
        
        print_status(3, "Navigating interface (6x TAB)...", "info")
        for i in range(6):
            pyautogui.press('tab')
            time.sleep(0.3)
        print_progress_bar(3, total_steps)
        time.sleep(0.5)
        
        print_status(4, "Opening save dialog...", "info")
        pyautogui.press('enter')
        time.sleep(3)
        print_progress_bar(4, total_steps)
        time.sleep(0.5)
        
        print_status(5, "Navigating to target directory...", "info")
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.5)
        pyautogui.write(r"C:\Users\DrewCobean\OneDrive - Paradigm\Desktop\Synchro")
        pyautogui.press('enter')
        time.sleep(2)
        print_progress_bar(5, total_steps)
        time.sleep(0.5)
        
        print_status(6, "Locating target file (4x TAB)...", "info")
        for i in range(4):
            pyautogui.press('tab')
            time.sleep(0.3)
        print_progress_bar(6, total_steps)
        time.sleep(0.5)
        
        print_status(7, "Confirming file selection...", "info")
        pyautogui.press('down')
        time.sleep(0.5)
        pyautogui.press('up')
        time.sleep(0.5)
        print_progress_bar(7, total_steps)
        time.sleep(0.5)
        
        print_status(8, "Finalizing operation...", "info")
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(2)
        print_progress_bar(8, total_steps)
        
        print(f"\n\n{Colors.OKGREEN}╔════════════════════════════════════════╗")
        print(f"║  {Colors.BOLD}✓ OPERATION COMPLETED SUCCESSFULLY{Colors.ENDC}{Colors.OKGREEN}    ║")
        print(f"╚════════════════════════════════════════╝{Colors.ENDC}")
        
    except pyautogui.FailSafeException:
        print(f"\n\n{Colors.WARNING}╔══════════════════════════════════════╗")
        print(f"║  {Colors.BOLD}⚠ OPERATION CANCELLED BY USER{Colors.ENDC}{Colors.WARNING}       ║")
        print(f"║    Mouse moved to corner (failsafe)    ║")
        print(f"╚══════════════════════════════════════╝{Colors.ENDC}")
    except Exception as e:
        print(f"\n\n{Colors.FAIL}╔══════════════════════════════════════╗")
        print(f"║  {Colors.BOLD}✗ OPERATION FAILED{Colors.ENDC}{Colors.FAIL}                   ║")
        print(f"║    Error: {str(e)[:25]:<25} ║")
        print(f"╚══════════════════════════════════════╝{Colors.ENDC}")

def main():
    """Main CLI interface"""
    print_banner()
    
    print(f"{Colors.BOLD}Configuration:{Colors.ENDC}")
    print(f"  • Target Window: {Colors.OKCYAN}Synchro Application{Colors.ENDC}")
    print(f"  • Output Directory: {Colors.OKCYAN}OneDrive\\Desktop\\Synchro{Colors.ENDC}")
    print(f"  • Safety: {Colors.OKGREEN}Failsafe Enabled{Colors.ENDC} (move mouse to corner to stop)")
    
    print(f"\n{Colors.BOLD}Ready to execute automated workflow.{Colors.ENDC}")
    print(f"{Colors.WARNING}Ensure Synchro application is visible and accessible.{Colors.ENDC}")
    
    try:
        input(f"\n{Colors.BOLD}Press ENTER to continue or Ctrl+C to cancel...{Colors.ENDC}")
        countdown(3, "Initializing automation")
        print()
        automate_synchro_process()
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.FAIL}╔══════════════════════════════════════╗")
        print(f"║  {Colors.BOLD}✗ OPERATION CANCELLED{Colors.ENDC}{Colors.FAIL}                ║")
        print(f"║    User interrupted execution        ║")
        print(f"╚══════════════════════════════════════╝{Colors.ENDC}")
        sys.exit(0)

if __name__ == "__main__":
    main()