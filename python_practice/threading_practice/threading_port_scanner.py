import socket
import threading
import queue 
import time


target_host = "scanme.nmap.org"

ports_to_scan_list = [21, 22, 23, 25, 53, 80, 110, 111, 135, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
NUMBER_OF_THREADS = 20

port_queue = queue.Queue()
for port in ports_to_scan_list: 
    port_queue.put(port)

open_ports_list = []
list_lock = threading.Lock()

def port_scanner_worker(target_ip): 

    while not port_queue.empty(): 
        try: 
            port = port_queue.get_nowait()
        except queue.Empty: 
            break 
        
        try: 
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)

            if s.connect_ex((target_ip, port)) == 0: 
                with list_lock: 
                    open_ports_list.append(port)
            
            else: 
                print(f"Port {port} on {target_ip} is CLOSED/FILTERED")

        except socket.gaierror: 
            break
        except socket.error as e: 
            pass
        finally: 
            if 's' in locals(): 
                s.close()

        port_queue.task_done()

if __name__ == "__main__":
    print(f"[*] Starting scan on {target_host} with {NUMBER_OF_THREADS} threads...")
    start_time = time.time()

    try: 
        resolved_target_ip = socket.gethostbyname(target_host)
        print(f"[*] Resolved {target_host} to {resolved_target_ip}")

    except socket.gaierror: 
        print(f"[*] Error: Hostname {target_host} could not be resolved. Exiting.")
        exit()
    
    threads = []

    for _ in range(NUMBER_OF_THREADS):
        thread = threading.Thread(target=port_scanner_worker, args=(resolved_target_ip,))
        thread.daemon = True
        threads.append(thread)
        thread.start()

    port_queue.join()

    end_time = time.time()

    scan_duration = end_time - start_time

    print(f"\n[*] Scan Complete in {scan_duration:.2f} seconds.")
    if open_ports_list: 
        open_ports_list.sort()
        print(f"[*] Open ports found: {open_ports_list}")
    else: 
        print("[*] No open ports found in the scanned range.")

