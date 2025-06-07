import socket 

target_host = "scanme.nmap.org"

target_port = 80

try: 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[*] Socket created for {target_host}")
except socket.error as err: 
    print(f"[!] Socket creation failed: {err}")
    exit()

try: 
    client.connect((target_host, target_port))
    print(f"[*] Successfully connected to {target_host} on port {target_port}")

    request = f"GET / HTTP/1.1\r\nHost: {target_host}\r\nConnection: close\r\n\r\n"
    client.send(request.encode('utf-8'))
    print(f"[*] Sent HTTP GET request")

    response_bytes = client.recv(4096)
    response_string = response_bytes.decode('utf-8', errors='ignore')

    print(f"\n[*] Received Response (first 4096 bytes):\n")
    print(response_string)

except socket.gaierror as err: 
    print(f"[!] Address-related error connecting to server: {err}")
except socket.error as err: 
    print(f"[!] Connection error: {err}")
finally: 
    print("[*] Closing socket.")
    client.close()
