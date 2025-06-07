my_ports = [21, 22, 80, 443, 8080]
target_host = ["10.0.0.1", "server.local", "192.168.1.254"]
mixed_list = [1, "test", True, 3.14]

def load_targets(filename="targets.txt"): 
    targets = []
    try: 
       with open(filename, "r") as f: 
            for line in f: 
                clean_line = line.strip()
                if clean_line and not clean_line.startswith("#"):
                    targets.append(clean_line)
       print(f"Loaded targets: {targets}")
       return targets
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return []

with open("targets.txt", "w") as temp_target_file: 
    temp_target_file.write("10,0,0,1\n")
    temp_target_file.write("10.0.0.2\n")
    temp_target_file.write("# This is a comment\n")
    temp_target_file.write("10.0.0.5\n")

loaded_ips = load_targets()
if loaded_ips: 
    print("Simulating scan for loaded IPS...")
    for ip in loaded_ips: 
        print(f"  -> Scanning {ip}...")

