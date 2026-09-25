"""
================================================================
  APURBO OB55 ULTIMATE SECURE ENGINE v3.0
  Channel: https://t.me/apurbo_world
  Owner: @ufbapurboyt730
  PROTECTED AGAINST UNAUTHORIZED MODIFICATION & TAMPERING
================================================================
"""

import os
import sys
import json
import glob
import time
import hashlib
import threading
import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init

# ---------- strict tamper-evident credit protection ----------
_OWNER_TAG = "@ufbapurboyt730"
_CHANNEL_TAG = "https://t.me/apurbo_world"

def _enforce_security():
    if _OWNER_TAG != "@ufbapurboyt730" or _CHANNEL_TAG != "https://t.me/apurbo_world":
        sys.stderr.write("\n[CRITICAL ERROR] Unauthorized code modification detected! Execution terminated.\n")
        sys.exit(403)

_enforce_security()

# ---------- initialize color scheme ----------
init(autoreset=False)
R = Style.RESET_ALL
B = Style.BRIGHT

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PRINT_LOCK = threading.Lock()
STATS_LOCK = threading.Lock()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_banner():
    print(f"║ {Fore.CYAN}{B} █████╗░{Fore.MAGENTA}██████╗░{Fore.YELLOW}██╗░░░██╗{Fore.GREEN}██████╗░{Fore.MAGENTA}██████╗░{Fore.YELLOW}░█████╗░  {Fore.CYAN}║")
    print(f"║ {Fore.CYAN}██╔══██╗{Fore.MAGENTA}██╔══██╗{Fore.YELLOW}██║░░░██║{Fore.GREEN}██╔══██╗{Fore.MAGENTA}██╔══██╗{Fore.YELLOW}██╔══██╗  {Fore.CYAN}║")
    print(f"║ {Fore.CYAN}███████║{Fore.MAGENTA}██████╔╝{Fore.YELLOW}██║░░░██║{Fore.GREEN}██████╔╝{Fore.MAGENTA}██████╦╝{Fore.YELLOW}██║░░██║  {Fore.CYAN}║")
    print(f"║ {Fore.CYAN}██╔══██║{Fore.MAGENTA}██╔═══╝░{Fore.YELLOW}██║░░░██║{Fore.GREEN}██╔══██╗{Fore.MAGENTA}██╔══██╗{Fore.YELLOW}██║░░██║  {Fore.CYAN}║")
    print(f"║ {Fore.CYAN}██║░░██║{Fore.MAGENTA}██║░░░░░{Fore.YELLOW}╚██████╔╝{Fore.GREEN}██║░░██║{Fore.MAGENTA}██████╦╝{Fore.YELLOW}╚█████╔╝  {Fore.CYAN}║")
    print(f"║ {Fore.CYAN}{B}╚═╝░░╚═╝{Fore.MAGENTA}╚═╝░░░░░{Fore.YELLOW}░╚═════╝░{Fore.GREEN}╚═╝░░╚═╝{Fore.MAGENTA}╚═════╝░{Fore.YELLOW}░╚════╝   {Fore.CYAN}║")
    
def live_loading_animation(duration=2.0):
    steps = [
        "VERIFYING LDR SECURITY SIGNATURES",
        "ESTABLISHING ENCRYPTED VERCEL TUNNEL",
        "ALLOCATING HIGH-SPEED WORKER THREADS",
        "SYNCING DATABASE AUTHENTICATION NODES"
    ]
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    width = 30
    start_time = time.time()
    print(f"\n{Fore.MAGENTA}{B}╔══════════════════ APURBO SYSTEM INITIALIZATION ══════════════════╗{R}")
    idx = 0
    while True:
        elapsed = time.time() - start_time
        percent = min(elapsed / duration, 1.0)
        step_idx = min(int(percent * len(steps)), len(steps) - 1)
        current_step = steps[step_idx]
        filled = int(width * percent)
        bar = "█" * filled + "░" * (width - filled)
        sym = spinner[idx % len(spinner)]
        idx += 1
        line = f" {sym} {Fore.CYAN}{current_step:<33} {Fore.YELLOW}{int(percent * 100):3}% {Fore.CYAN}{bar}{R}"
        sys.stdout.write(f"\r{Fore.MAGENTA}║{R}{line:<57}{Fore.MAGENTA}║{R}")
        sys.stdout.flush()
        if percent >= 1.0:
            break
        time.sleep(0.06)
    print(f"\n{Fore.MAGENTA}{B}╚═════════════════════════════════════════════════════════╝{R}\n")
    time.sleep(0.15)

def print_result_box(task_id, uid, success, execution_time, region="N/A", msg=""):
    status_color = Fore.GREEN if success else Fore.RED
    status_text = " [ SUCCESSFUL ] " if success else " [   FAILED   ] "
    icon = "★" if success else "✕"
    
    # Dynamic RGB Border styling per box render
    border_col = Fore.CYAN if success else Fore.YELLOW
    
    lines = [
        f"{CYAN}{B}╔═════════════════════════════════════════════════════════╗",
        f"│ {Fore.WHITE}TASK ID   │ {Fore.YELLOW}{str(task_id):<43} {border_col}│",
        f"│ {Fore.WHITE}UID TARGET│ {Fore.CYAN}{str(uid)[:43]:<43} {border_col}│",
        f"│ {Fore.WHITE}REGION    │ {Fore.MAGENTA}{str(region):<43} {border_col}│",
        f"│ {Fore.WHITE}STATUS    │ {status_color}{icon}{status_text:<42} {border_col}│",
        f"│ {Fore.WHITE}LATENCY   │ {Fore.GREEN}{execution_time:.2f}s{R:<43} {CYAN}│",
        f"╚═════════════════════════════════════════════════════════╝{R}"
    ]
    output = "\n".join(lines) + "\n"
    with PRINT_LOCK:
        sys.stdout.write(output)
        sys.stdout.flush()

class LDROB55Activator:
    def __init__(self, max_workers=64):
        _enforce_security()
        self.api_base = "https://jxe-guest-act-ob55.vercel.app/jxe/act"
        self.max_workers = max_workers
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=200, pool_maxsize=200, max_retries=1)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.session.verify = False
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Linux; Android 12; Mobile) AppleWebKit/537.36'})
        self.successful = 0
        self.failed = 0
        self.successful_accounts = []
        self.stats_lock = threading.Lock()

    def activate_single_account(self, acc, task_id):
        start = time.time()
        uid = acc['uid']
        pwd = acc['password']
        
        target_url = f"{self.api_base}?uid={uid}&password={pwd}"
        
        try:
            resp = self.session.get(target_url, timeout=10)
            elapsed = time.time() - start
            
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    if data.get("status") == "success" or data.get("activated") is True:
                        region = data.get("region", "BD")
                        print_result_box(task_id, uid, True, elapsed, region)
                        with self.stats_lock:
                            self.successful += 1
                            self.successful_accounts.append({
                                'uid': uid, 
                                'password': pwd, 
                                'region': region,
                                'account_name': data.get("account_name", "Unknown"),
                                'account_id': data.get("account_id", "N/A")
                            })
                        return True
                except json.JSONDecodeError:
                    pass
            
            print_result_box(task_id, uid, False, elapsed)
            with self.stats_lock:
                self.failed += 1
            return False

        except Exception:
            elapsed = time.time() - start
            print_result_box(task_id, uid, False, elapsed)
            with self.stats_lock:
                self.failed += 1
            return False

    def select_source_path(self):
        print(f"{Fore.MAGENTA}{B}╔═════════════════════════════════════════════════════════╗")
        print(f"│               {Fore.WHITE}LDR STORAGE CONFIGURATION ROUTER         {Fore.MAGENTA}║")
        print(f"╠═════════════════════════════════════════════════════════╣")
        print(f"│  {Fore.YELLOW}1. Auto-Scan Current Working Directory{Fore.CYAN}                 │")
        print(f"│  {Fore.YELLOW}2. Specify Custom System Path Location{Fore.CYAN}               │")
        print(f"╚═════════════════════════════════════════════════════════╝{R}")
        choice = input(f"{Fore.MAGENTA}{B}⚡ Select Option Mode (1/2): {R}").strip()
        if choice == '2':
            print(f"\n{Fore.DIM}{Fore.WHITE}Example Path: /sdcard/Download/database.json{R}")
            path = input(f"{Fore.CYAN}📂 Enter Directory/File Path: {R}").strip()
            path = path.replace('"', '').replace("'", "")
            if not os.path.exists(path):
                print(f"{Fore.RED}❌ Specified file or directory does not exist.{R}")
                return None
            return path
        else:
            return os.getcwd()

    def load_accounts_from_path(self, path):
        accounts = []
        files = []
        if os.path.isfile(path):
            files = [path]
        elif os.path.isdir(path):
            files = glob.glob(os.path.join(path, '*.json')) + glob.glob(os.path.join(path, '*.txt'))
        else:
            return accounts

        if not files:
            print(f"{Fore.RED}❌ No valid data files detected in path: {path}{R}")
            return accounts

        print(f"{Fore.GREEN}🔍 Found {len(files)} target database file(s).{R}")
        for filepath in files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                if not content:
                    continue
                if filepath.endswith('.json'):
                    try:
                        data = json.loads(content)
                        if isinstance(data, list):
                            for item in data:
                                acc = self._extract_account(item)
                                if acc:
                                    accounts.append(acc)
                        elif isinstance(data, dict):
                            for key, val in data.items():
                                if isinstance(val, dict):
                                    acc = self._extract_account(val)
                                    if acc:
                                        accounts.append(acc)
                    except:
                        pass
                else:
                    lines = content.splitlines()
                    for line in lines:
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue
                        sep = ':' if ':' in line else ' ' if ' ' in line else None
                        if sep:
                            parts = line.split(sep, 1)
                            if len(parts) == 2:
                                uid = parts[0].strip()
                                pwd = parts[1].strip()
                                if uid and pwd:
                                    accounts.append({'uid': uid, 'password': pwd})
            except Exception as e:
                print(f"{Fore.YELLOW}⚠ Warning parsing file {filepath}: {e}{R}")

        unique = []
        seen = set()
        for acc in accounts:
            key = (acc['uid'], acc['password'])
            if key not in seen:
                seen.add(key)
                unique.append(acc)
        print(f"{Fore.GREEN}✨ Successfully verified {len(unique)} unique user accounts.{R}\n")
        return unique

    def _extract_account(self, obj):
        if not isinstance(obj, dict):
            return None
        uid = obj.get('uid') or obj.get('user') or obj.get('username')
        pwd = obj.get('password') or obj.get('pass')
        if uid and pwd:
            return {'uid': str(uid), 'password': str(pwd)}
        return None

    def save_results(self):
        filename = 'ldr-activated-success.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.successful_accounts, f, indent=2)
        print(f"\n{Fore.CYAN}💾 Exported {len(self.successful_accounts)} active accounts to {filename}{R}")

    def run(self, accounts):
        total = len(accounts)
        if total == 0:
            print(f"{Fore.RED}❌ No accounts available for pipeline execution.{R}")
            return
            
        live_loading_animation(duration=1.5)
        print(f"{Fore.CYAN}🚀 Launching LDR high-speed parallel engine ({self.max_workers} Workers)...{R}\n")
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.activate_single_account, acc, i+1): acc for i, acc in enumerate(accounts)}
            for _ in as_completed(futures):
                pass

        total_time = time.time() - start_time
        self.save_results()

        success_rate = (self.successful / total * 100) if total > 0 else 0
        speed = (total / total_time) if total_time > 0 else 0
        
        summary_lines = [
            f" {Fore.WHITE}Total Processed  │ {Fore.YELLOW}{total}{R}",
            f" {Fore.GREEN}Successful       │ {Fore.GREEN}{self.successful}{R}",
            f" {Fore.RED}Failed           │ {Fore.RED}{self.failed}{R}",
            f" {Fore.WHITE}Total Time       │ {Fore.YELLOW}{total_time:.2f}s{R}",
            f" {Fore.CYAN}Engine Speed     │ {Fore.MAGENTA}{speed:.1f} acc/s{R}",
            f" {Fore.CYAN}Success Rate     │ {Fore.MAGENTA}{success_rate:.1f}%{R}"
        ]
        
        print(f"\n{Fore.MAGENTA}{B}╔══════════════════ EXECUTION REPORT ═══════════════╗")
        for line in summary_lines:
            print(f"║{R}{line:<58}║")
        print(f"╚═══════════════════════════════════════════════════╝{R}")
        print(f"\n{Fore.GREEN}⚡ Owner: @ufbapurboyt730 | Channel: https://t.me/apurbo_world{R}")

def main():
    clear_screen()
    render_banner()
    activator = LDROB55Activator(max_workers=64)
    source_path = activator.select_source_path()
    if source_path is None:
        print(f"{Fore.RED}❌ Setup aborted. No source specified.{R}")
        return
    accounts = activator.load_accounts_from_path(source_path)
    if accounts:
        activator.run(accounts)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}👋 Script safely terminated by user.{R}")
        sys.exit(0)
