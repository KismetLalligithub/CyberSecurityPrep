import socket
import threading
import queue
import time
import sys

open_ports_list = []
list_lock = threading.Lock()
port_queue = queue.Queue()

def parse_ports(port_spec):
    ports = set()
    try:
        if ',' in port_spec:
            parts = port_spec.split(',')
            for part in parts:
                part = part.strip()
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    if start > end:
                        raise ValueError(f"Invalid range: {part}")
                    ports.update(range(start, end + 1))
                else:
                    ports.add(int(part))
        elif '-' in port_spec:
            start, end = map(int, port_spec.split('-'))
            if start > end:
                raise ValueError(f"Invalid range: {port_spec}")
            ports.update(range(start, end + 1))
        else:
            ports.add(int(port_spec))

        for port in ports:
            if not 1 <= port <= 65535:
                raise ValueError(f"Port number {port} is out of valid range (1-65535).")
        
        return sorted(list(ports))

    except ValueError as e:
        print(f"[!] Invalid port specification: {e}")
        return None

def port_scanner_worker(target_ip, verbose):
    while not port_queue.empty():
        try:
            port = port_queue.get_nowait()
        except queue.Empty:
            break

        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)

            if s.connect_ex((target_ip, port)) == 0:
                if verbose:
                    print(f"Port {port} on {target_ip} is OPEN")
                with list_lock:
                    open_ports_list.append(port)
            else:
                if verbose:
                    print(f"Port {port} on {target_ip} is CLOSED/FILTERED")

        except socket.gaierror:
            if verbose:
                print(f"Error: Hostname {target_ip} could not be resolved. Thread exiting.")
            break
        except socket.error as e:
            if verbose:
                print(f"Socket error on port {port}: {e}")
            pass
        finally:
            if s:
                s.close()
        
        port_queue.task_done()

if __name__ == "__main__":
    is_verbose = False
    if '-v' in sys.argv or '--verbose' in sys.argv:
        is_verbose = True
        if '-v' in sys.argv: sys.argv.remove('-v')
        if '--verbose' in sys.argv: sys.argv.remove('--verbose')

    if len(sys.argv) == 4:
        target_host = sys.argv[1]
        port_spec = sys.argv[2]
        try:
            num_threads = int(sys.argv[3])
            if num_threads <= 0:
                raise ValueError
        except ValueError:
            print("[!] Error: Number of threads must be a positive integer.")
            exit()
    else:
        print("[*] No command-line arguments provided. Switching to interactive mode.")
        print("    Usage: python your_script_name.py <target_host> <ports> <threads> [-v|--verbose]")
        target_host = input("[?] Enter the target host (e.g., scanme.nmap.org): ")
        if not target_host:
            print("[!] Error: Target host cannot be empty.")
            exit()
        port_spec = input("[?] Enter ports to scan (e.g., '1-1024' or '80,443,8080'): ")
        while True:
            try:
                num_threads_str = input("[?] Enter the number of threads (e.g., 20): ")
                num_threads = int(num_threads_str)
                if num_threads > 0:
                    break
                else:
                    print("[!] Please enter a positive number.")
            except ValueError:
                print("[!] Invalid input. Please enter an integer.")

    ports_to_scan_list = parse_ports(port_spec)
    if not ports_to_scan_list:
        exit()

    for port in ports_to_scan_list:
        port_queue.put(port)

    print(f"\n[*] Starting scan on {target_host} with {num_threads} threads...")
    start_time = time.time()

    try:
        resolved_target_ip = socket.gethostbyname(target_host)
        print(f"[*] Resolved {target_host} to {resolved_target_ip}")
    except socket.gaierror:
        print(f"[!] Error: Hostname {target_host} could not be resolved. Exiting.")
        exit()

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=port_scanner_worker, args=(resolved_target_ip, is_verbose))
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