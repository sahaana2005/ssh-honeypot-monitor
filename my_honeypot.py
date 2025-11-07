#!/usr/bin/env python3
import socket
import threading
import time
from datetime import datetime

print("🐢 Starting Simple SSH Honeypot...")
print("📡 Listening on port 2222")
print("💾 Logging to honeypot_log.txt")

def handle_connection(client_socket, address):
    print(f"🚨 Connection from {address[0]}:{address[1]}")
    try:
        # Send SSH banner
        client_socket.send(b"SSH-2.0-OpenSSH_7.4\r\n")
        
        # Receive client data
        data = client_socket.recv(1024)
        print(f"📨 Received: {data.decode('utf-8', errors='ignore')}")
        
        # Log the attempt
        log_entry = f"{datetime.now()} - {address[0]}:{address[1]} - {data}\n"
        with open("honeypot_log.txt", "a") as f:
            f.write(log_entry)
            
        print(f"✅ Logged connection from {address[0]}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client_socket.close()

def start_honeypot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 2222))
    server.listen(5)
    
    print("🎯 Honeypot is LIVE! Waiting for connections...")
    print("Press Ctrl+C to stop\n")
    
    while True:
        client, addr = server.accept()
        client_handler = threading.Thread(target=handle_connection, args=(client, addr))
        client_handler.start()

if __name__ == "__main__":
    start_honeypot()
