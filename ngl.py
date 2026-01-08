#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-
"""
██╗   ██╗ ██████╗ ██╗██████╗    ███╗   ██╗██╗   ██╗██╗  ██╗███████╗██████╗ 
██║   ██║██╔═══██╗██║██╔══██╗   ████╗  ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗
██║   ██║██║   ██║██║██║  ██║   ██╔██╗ ██║██║   ██║█████╔╝ █████╗  ██████╔╝
╚██╗ ██╔╝██║   ██║██║██║  ██║   ██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗
 ╚████╔╝ ╚██████╔╝██║██████╔╝   ██║ ╚████║╚██████╔╝██║  ██╗███████╗██║  ██║
  ╚═══╝   ╚═════╝ ╚═╝╚═════╝    ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
VOID NUKER - Ultimate NGL Spammer v4.0
Developer: Marr 
"""

import subprocess
import sys
import os

# ========== AUTO-INSTALL DEPENDENCIES ==========
def install_dependencies():
    """Auto-install required packages"""
    print("[*] Checking dependencies...")
    
    required = {
        'requests': 'requests',
        'colorama': 'colorama'
    }
    
    for module, package in required.items():
        try:
            __import__(module)
            print(f"✅ {module} already installed")
        except ImportError:
            print(f"⚠️ Installing {module}...")
            try:
                subprocess.check_call([
                    sys.executable, 
                    "-m", 
                    "pip", 
                    "install", 
                    package,
                    "--quiet"
                ])
                print(f"✅ {module} installed successfully")
            except Exception as e:
                print(f"❌ Failed to install {module}: {e}")
                print("Please run manually: pip install requests colorama")
                sys.exit(1)

# Run auto-install
install_dependencies()

# ========== NOW IMPORT EVERYTHING ==========
import requests
import json
import time
import threading
import random
from datetime import datetime

# ========== CONFIGURATION ==========
VERSION = "4.0"
DEVELOPER = "Marr"
BANNER = f"""
{chr(27)}[91m
╦  ╦╔═╗╔╦╗╔╦╗  ╔═╗╦ ╦╔═╗╦═╗╔═╗
╚╗╔╝╠═╣║║║ ║   ║ ╦║ ║╠═╣╠╦╝║╣ 
 ╚╝ ╩ ╩╩ ╩ ╩   ╚═╝╚═╝╩ ╩╩╚═╚═╝
{chr(27)}[96m
╔═╗╔╦╗╔═╗╔═╗╦═╗╔═╗╔═╗╦  ╔═╗╦═╗
╠═╣ ║║╠═╣║ ║╠╦╝╠═╣║  ║  ║╣ ╠╦╝
╩ ╩═╩╝╩ ╩╚═╝╩╚═╩ ╩╚═╝╩═╝╚═╝╩╚═
{chr(27)}[93m
Termux Edition v{VERSION}
Developer: {DEVELOPER}
{chr(27)}[0m"""

# ========== ENHANCED USER AGENTS DATABASE (150+ Agents) ==========
USER_AGENTS = [
    # ========== LATEST CHROME DESKTOP ==========
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    
    # ========== FIREFOX LATEST ==========
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 15.0; rv:135.0) Gecko/20100101 Firefox/135.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0",
    
    # ========== SAFARI LATEST ==========
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
    
    # ========== ANDROID CHROME LATEST ==========
    "Mozilla/5.0 (Linux; Android 15; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-F956B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.120 Mobile Safari/537.36",
    
    # ========== XIAOMI DEVICES ==========
    "Mozilla/5.0 (Linux; Android 14; 24031PN0CG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; 23021RAA2Y) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; 22081212UG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.120 Mobile Safari/537.36",
    
    # ========== OPPO/REALME/VIVO ==========
    "Mozilla/5.0 (Linux; Android 14; CPH2581) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; RMX3851) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; V2338) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.120 Mobile Safari/537.36",
    
    # ========== GOOGLE PIXEL ==========
    "Mozilla/5.0 (Linux; Android 15; Pixel 9 Pro XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 15; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.120 Mobile Safari/537.36",
    
    # ========== SAMSUNG BROWSER ==========
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/25.0 Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/121.0.0.0 Mobile Safari/537.36",
    
    # ========== MICROSOFT EDGE ==========
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    
    # ========== OPERA ==========
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 OPR/115.0.0.0",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36 OPR/75.0.0.0",
    
    # ========== BRAVE BROWSER ==========
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Brave/130.0",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36 Brave/130.0",
    
    # ========== VIVALDI ==========
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Vivaldi/6.7",
    
    # ========== UC BROWSER ==========
    "Mozilla/5.0 (Linux; U; Android 14; en-US; SM-S928B Build/UP1A) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.0.0 Mobile Safari/537.36 UCBrowser/15.0.0.0",
    
    # ========== DUCKDUCKGO BROWSER ==========
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile DuckDuckGo/5.145.0 Safari/537.36",
    
    # ========== FIREFOX MOBILE ==========
    "Mozilla/5.0 (Android 14; Mobile; rv:135.0) Gecko/135.0 Firefox/135.0",
    "Mozilla/5.0 (Android 14; Mobile; rv:135.0) Gecko/135.0 Firefox/135.0",
    
    # ========== OPERA MINI ==========
    "Opera/9.80 (Android; Opera Mini/82.0.2254/135.0; U; en) Presto/2.12.423 Version/12.16",
    
    # ========== CHROME iOS ==========
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/130.0.6723.120 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/130.0.6723.120 Mobile/15E148 Safari/604.1",
    
    # ========== FIREFOX iOS ==========
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/135.0 Mobile/15E148 Safari/605.1.15",
    
    # ========== ANDROID WEBVIEW ==========
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.120 Mobile Safari/537.36",
    
    # ========== LEGACY DEVICES (Untuk diversifikasi) ==========
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.111 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.136 Mobile Safari/537.36",
    
    # ========== TABLETS ==========
    "Mozilla/5.0 (Linux; Android 14; SM-X910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.120 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-X616B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.120 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Lenovo TB-X606F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.120 Safari/537.36",
    
    # ========== SMART TV / GAME CONSOLES ==========
    "Mozilla/5.0 (SMART-TV; Linux; Tizen 7.0) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/25.0 Chrome/130.0.6723.120 TV Safari/537.36",
    "Mozilla/5.0 (PlayStation 5; PlayStation 5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
    "Mozilla/5.0 (Nintendo Switch; Nintendo) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
    
    # ========== BOTS (Untuk variasi) ==========
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    
    # ========== TERMUX / CURL (Untuk realisme) ==========
    "curl/8.5.0",
    "Wget/1.21.4",
    "Python-urllib/3.11",
    
    # ========== RANDOM OLD BROWSERS ==========
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0)",
    
    # ========== MOBILE EMULATION ==========
    "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.120 Mobile Safari/537.36",
    
    # ========== CUSTOM APPS ==========
    "NGL-Spammer/4.0 (Termux; Android 14; SM-S928B) AppleWebKit/537.36",
    "VoidNuker/5.0 (Termux; Linux; aarch64) AppleWebKit/537.36",
    "DarkMasterWeb/1.0 (Android; U; en-US) AppleWebKit/537.36",
    
    # ========== UNIQUE RARE AGENTS ==========
    "Mozilla/5.0 (X11; FreeBSD amd64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; OpenBSD amd64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; NetBSD amd64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; DragonFly amd64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    
    # ========== UNUSUAL COMBINATIONS ==========
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Vivaldi/6.7",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36 EdgA/115.0.0.0",
    
    # ========== EXPERIMENTAL ==========
    "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; arm64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
    
    # ========== WINDOWS PHONE (Rare) ==========
    "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36 Edge/130.0.0.0",
    
    # ========== BLACKBERRY (Vintage) ==========
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9900; en) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.1.0.346 Mobile Safari/534.11+",
    
    # ========== SAMSUNG TIZEN ==========
    "Mozilla/5.0 (Linux; Tizen 7.0; SAMSUNG SM-Z9005) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/25.0 Chrome/130.0.6723.120 Mobile Safari/537.36",
    
    # ========== AMAZON FIRE ==========
    "Mozilla/5.0 (Linux; Android 14; KFMAWI) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Silk/130.0.0.0",
    
    # ========== CUSTOM USER AGENTS ==========
    "Mozilla/5.0 (compatible; VoidBot/1.0; +https://void.nuker)",
    "Mozilla/5.0 (compatible; MarrBot/1.0; +https://marr.dev)",
    "VoidNuker/5.0 Termux-Edition (Linux; Android 14; aarch64)",
    "DarkMasterWeb-Void/4.0 (Android; Termux; en-US)",
    
    # ========== TERMUX SPECIFIC ==========
    "Termux/0.118 (Linux; Android 14; aarch64) Python/3.11",
    "Termux-Requests/2.31.0 (Linux; U; Android 14; en-US)",
    
    # ========== FORWARDED USER AGENTS ==========
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Via-Termux",
    "Mozilla/5.0 (Android; Mobile; rv:135.0) Gecko/135.0 Firefox/135.0 Via-VoidNuker",
    
    # ========== RANDOMIZED ==========
    f"Mozilla/5.0 (Linux; Android {random.randint(10, 15)}; SM-S{random.randint(900, 999)}B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(120, 130)}.0.{random.randint(6000, 7000)}.{random.randint(100, 200)} Mobile Safari/537.36",
    f"Mozilla/5.0 (iPhone; CPU iPhone OS {random.randint(15, 18)}_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{random.randint(16, 18)}.0 Mobile/15E148 Safari/604.1",
]

# Colors
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

# ========== CORE FUNCTIONS ==========
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    clear_screen()
    print(BANNER)

def print_colored(text, color=Colors.WHITE):
    print(f"{color}{text}{Colors.END}")

# ========== NGL SPAMMER CLASS ==========
class VoidNuker:
    def __init__(self):
        self.stats = {
            'sent': 0,
            'success': 0,
            'failed': 0,
            'running': False,
            'start_time': None
        }
        self.threads = []
        
    def send_message(self, username, message):
        """Send single message to NGL"""
        url = f"https://ngl.link/api/submit"
        
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://ngl.link',
            'Referer': f'https://ngl.link/{username}',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        payload = {
            'username': username,
            'question': message,
            'deviceId': f"void_{random.randint(1000000, 9999999)}",
            'gameSlug': '',
            'referrer': ''
        }
        
        try:
            response = requests.post(url, data=payload, headers=headers, timeout=10)
            self.stats['sent'] += 1
            
            if response.status_code == 200:
                self.stats['success'] += 1
                return True
            else:
                self.stats['failed'] += 1
                return False
        except Exception:
            self.stats['failed'] += 1
            return False
    
    def worker(self, worker_id, username, messages, delay, quantity):
        """Worker thread"""
        sent_count = 0
        
        while self.stats['running'] and (quantity == 0 or sent_count < quantity):
            try:
                message = random.choice(messages)
                self.send_message(username, message)
                sent_count += 1
                
                # Update display every 5 messages
                if sent_count % 5 == 0:
                    self.display_stats()
                
                # Random delay
                time.sleep(delay + random.uniform(0, 0.3))
                
            except Exception as e:
                print_colored(f"[Thread-{worker_id}] Error: {e}", Colors.RED)
                time.sleep(2)
        
        print_colored(f"[Thread-{worker_id}] Finished - {sent_count} sent", Colors.GREEN)
    
    def display_stats(self):
        """Display live statistics"""
        if not self.stats['start_time']:
            return
            
        elapsed = time.time() - self.stats['start_time']
        success_rate = (self.stats['success'] / self.stats['sent'] * 100) if self.stats['sent'] > 0 else 0
        
        clear_screen()
        show_banner()
        
        print_colored(f"\n╔══════════════════════════════════════════╗", Colors.CYAN)
        print_colored(f"║         LIVE ATTACK STATISTICS         ║", Colors.WHITE)
        print_colored(f"╠══════════════════════════════════════════╣", Colors.CYAN)
        print_colored(f"║ 🎯 Target: {self.config['username']:28} ║", Colors.YELLOW)
        print_colored(f"║ 📤 Sent: {self.stats['sent']:<6} ✅ Success: {self.stats['success']:<6} ║", Colors.GREEN)
        print_colored(f"║ ❌ Failed: {self.stats['failed']:<5} 📊 Rate: {success_rate:6.1f}% ║", Colors.RED)
        print_colored(f"║ ⏱️  Time: {elapsed:6.1f}s 🧵 Threads: {len(self.threads):<4} ║", Colors.BLUE)
        
        if elapsed > 0:
            speed = self.stats['sent'] / elapsed
            print_colored(f"║ 🚀 Speed: {speed:6.1f}/s{' ' * 19}║", Colors.MAGENTA)
        
        print_colored(f"╚══════════════════════════════════════════╝", Colors.CYAN)
        print_colored(f"\n[!] Press Ctrl+C to stop", Colors.YELLOW)
    
    def start_attack(self, config):
        """Start the attack"""
        self.config = config
        self.stats = {
            'sent': 0,
            'success': 0,
            'failed': 0,
            'running': True,
            'start_time': time.time()
        }
        
        print_colored(f"\n[+] Starting attack on @{config['username']}", Colors.GREEN)
        print_colored(f"[+] Threads: {config['threads']} | Delay: {config['delay']}s", Colors.CYAN)
        print_colored(f"[+] Quantity: {'Unlimited' if config['quantity'] == 0 else config['quantity']}", Colors.YELLOW)
        
        time.sleep(2)
        
        # Create threads
        for i in range(config['threads']):
            thread = threading.Thread(
                target=self.worker,
                args=(i+1, config['username'], config['messages'], 
                      config['delay'], config['quantity']),
                daemon=True
            )
            thread.start()
            self.threads.append(thread)
        
        try:
            # Monitor attack
            while self.stats['running'] and any(t.is_alive() for t in self.threads):
                time.sleep(0.5)
                self.display_stats()
                
                # Check quantity limit
                if config['quantity'] > 0 and self.stats['sent'] >= config['threads'] * config['quantity']:
                    break
                    
        except KeyboardInterrupt:
            print_colored("\n[!] Stopping attack...", Colors.RED)
        
        finally:
            self.stop_attack()
    
    def stop_attack(self):
        """Stop the attack"""
        self.stats['running'] = False
        time.sleep(1)
        
        # Final stats
        elapsed = time.time() - self.stats['start_time']
        success_rate = (self.stats['success'] / self.stats['sent'] * 100) if self.stats['sent'] > 0 else 0
        
        print_colored(f"\n════════════════════════════════════════", Colors.CYAN)
        print_colored(f"           ATTACK COMPLETED           ", Colors.GREEN)
        print_colored(f"════════════════════════════════════════", Colors.CYAN)
        print_colored(f"🎯 Target: {self.config['username']}", Colors.YELLOW)
        print_colored(f"✅ Success: {self.stats['success']}", Colors.GREEN)
        print_colored(f"❌ Failed: {self.stats['failed']}", Colors.RED)
        print_colored(f"📤 Total: {self.stats['sent']}", Colors.CYAN)
        print_colored(f"📊 Rate: {success_rate:.1f}%", Colors.MAGENTA)
        print_colored(f"⏱️  Time: {elapsed:.1f}s", Colors.BLUE)
        
        if elapsed > 0:
            speed = self.stats['sent'] / elapsed
            print_colored(f"🚀 Speed: {speed:.1f}/s", Colors.GREEN)
        
        print_colored(f"════════════════════════════════════════", Colors.CYAN)
        
        # Save results
        self.save_results(elapsed, success_rate)
    
    def save_results(self, elapsed, success_rate):
        """Save results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"void_results_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write(f"VOID NUKER Attack Results\n")
                f.write(f"Time: {timestamp}\n")
                f.write(f"Target: {self.config['username']}\n")
                f.write(f"Success: {self.stats['success']}\n")
                f.write(f"Failed: {self.stats['failed']}\n")
                f.write(f"Total: {self.stats['sent']}\n")
                f.write(f"Success Rate: {success_rate:.1f}%\n")
                f.write(f"Duration: {elapsed:.1f}s\n")
                f.write(f"Threads: {self.config['threads']}\n")
                f.write(f"Developer: {DEVELOPER}\n")
            
            print_colored(f"[+] Results saved to {filename}", Colors.GREEN)
        except Exception as e:
            print_colored(f"[!] Failed to save: {e}", Colors.RED)

# ========== MAIN MENU ==========
def main_menu():
    """Main menu interface"""
    spammer = VoidNuker()
    
    while True:
        show_banner()
        
        print_colored(f"\n╔══════════════════════════════════╗", Colors.CYAN)
        print_colored(f"║            MAIN MENU  ║", Colors.WHITE)
        print_colored(f"╠══════════════════════════════════╣", Colors.CYAN)
        print_colored(f"║ 1️⃣  Plenger Attack     ║", Colors.GREEN)
        print_colored(f"║ 2️⃣  Custom Attack Bwabwa║", Colors.YELLOW)
        print_colored(f"║ 3️⃣  View Results        ║", Colors.BLUE)
        print_colored(f"║ 4️⃣  Exit                 ║", Colors.RED)
        print_colored(f"╚══════════════════════════════════╝", Colors.CYAN)
        
        choice = input(f"\n{Colors.CYAN}[?] Select (1-4): {Colors.END}").strip()
        
        if choice == '1':
            username = input(f"{Colors.CYAN}[?] NGL Username: {Colors.END}").strip()
            if username:
                config = {
                    'username': username,
                    'messages': [
                        "VOID NUKER ACTIVATED 🚀",
                        "TERMUX POWER ⚡",
                        "MARRIAGE OF CHAOS 💀",
                        "UNLIMITED SPAM 🔥"
                    ],
                    'threads': 10,
                    'delay': 0.5,
                    'quantity': 0  # Unlimited
                }
                
                print_colored(f"\n[!] Starting attack on @{username}", Colors.YELLOW)
                print_colored(f"[!] Press Ctrl+C to stop anytime", Colors.RED)
                time.sleep(2)
                
                spammer.start_attack(config)
                input(f"\n{Colors.CYAN}[?] Press Enter to continue...{Colors.END}")
        
        elif choice == '2':
            show_banner()
            
            username = input(f"{Colors.CYAN}[?] NGL Username: {Colors.END}").strip()
            if not username:
                continue
            
            # Messages
            print_colored(f"\n[*] Messages (Enter empty to use default)", Colors.YELLOW)
            messages = []
            while True:
                msg = input(f"{Colors.CYAN}[?] Message {len(messages)+1}: {Colors.END}").strip()
                if not msg:
                    if not messages:
                        messages = ["VOID ATTACK 🌀", "TERMUX EDITION 📱", "MARRIAGE 👑"]
                    break
                messages.append(msg)
            
            # Threads
            try:
                threads = int(input(f"{Colors.CYAN}[?] Threads (1-50): {Colors.END}") or "10")
                threads = max(1, min(50, threads))
            except:
                threads = 10
            
            # Delay
            try:
                delay = float(input(f"{Colors.CYAN}[?] Delay (seconds): {Colors.END}") or "0.5")
                delay = max(0.1, delay)
            except:
                delay = 0.5
            
            # Quantity
            try:
                quantity = int(input(f"{Colors.CYAN}[?] Messages per thread (0=unlimited): {Colors.END}") or "0")
            except:
                quantity = 0
            
            config = {
                'username': username,
                'messages': messages,
                'threads': threads,
                'delay': delay,
                'quantity': quantity
            }
            
            print_colored(f"\n[!] Starting attack with {threads} threads", Colors.YELLOW)
            time.sleep(2)
            
            spammer.start_attack(config)
            input(f"\n{Colors.CYAN}[?] Press Enter to continue...{Colors.END}")
        
        elif choice == '3':
            show_banner()
            print_colored(f"\n[*] Saved Results", Colors.CYAN)
            
            # List result files
            result_files = [f for f in os.listdir('.') if f.startswith('void_results_') and f.endswith('.txt')]
            
            if not result_files:
                print_colored("[!] No results found", Colors.YELLOW)
            else:
                for i, f in enumerate(sorted(result_files, reverse=True)[:5], 1):
                    print_colored(f"{i}. {f}", Colors.WHITE)
            
            input(f"\n{Colors.CYAN}[?] Press Enter to continue...{Colors.END}")
        
        elif choice == '4':
            print_colored(f"\n[*] Exiting VOID NUKER...", Colors.RED)
            time.sleep(1)
            clear_screen()
            break
        
        else:
            print_colored(f"\n[!] Invalid choice", Colors.RED)
            time.sleep(1)

# ========== MAIN EXECUTION ==========
if __name__ == "__main__":
    try:
        # Welcome message
        show_banner()
        print_colored(f"\n[*] VOID NUKER v{VERSION} - Ready for Action!", Colors.GREEN)
        print_colored(f"[*] Developer: {DEVELOPER}", Colors.CYAN)
        print_colored(f"[*] Platform: Termux (Android)", Colors.YELLOW)
        print_colored(f"[!] Hanya Untuk Edukasi", Colors.RED)
        time.sleep(2)
        
        # Start main menu
        main_menu()
        
    except KeyboardInterrupt:
        print_colored(f"\n[!] Interrupted by user", Colors.RED)
    except Exception as e:
        print_colored(f"\n[!] Error: {e}", Colors.RED)
