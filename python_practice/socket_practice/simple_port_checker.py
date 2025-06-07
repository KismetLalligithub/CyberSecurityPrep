import socket

def check_port(host, port, timeout=1): 

    try: 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        result = sock.connect_ex((host, port))

        if result == 0 and port == 21 or port == 22 or port == 80:
            sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock2.connect((host, port))
            print(f"[*] Successfully connected to {host} on port {port}")

            if port == 80:
                request = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
                sock2.send(request.encode('utf-8'))
                print(f"[*] Sent HTTP GET request")

                response_bytes = sock2.recv(1024)
                response_string = response_bytes.decode('utf-8', errors='ignore')
                print(f"[*] Received Response (first 4096 bytes):\n")
                print(response_string[:100])
            
            sock2.close()

            return True
        elif result == 0: 
            return True
        else: 
            return False 
    except socket.gaierror: 
        return False
    except socket.error as e: 
        return False
    finally: 
        if 'sock' in locals(): 
            sock.close()

def port_check(target_ip, common_ports, timeout=1):
    print(f"\n[*] Checking common ports on {target_ip} ...")
    for p in common_ports: 
        if check_port(target_ip, p, timeout): 
            print(f"  Port {p}: Open")
        else: 
            print(f"  Port {p}: Closed/Filtered/Unresolved")
