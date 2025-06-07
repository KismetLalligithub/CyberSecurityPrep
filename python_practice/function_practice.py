def function_name(parameter1, parameter2, ...): 
	return some_value


def is_well_known_port(port_number): 
	if 0 <= port_number <= 1023: 
		return True
	return False

def simulate_port_scan(target_ip, port_number): 
	if port_number in [21, 22, 25, 80, 443]: 
		return "Open (Simulated)"
	else: 
		return "Closed/Filtered (Simulated)"
def get_common_port(service_name):
	serivce_map = {
		"http": 80, 
		"https": 443, 
		"ftp": 21, 
		"ssh": 22, 
		"dns": 53,
		"smtp": 25
	}
	return service_map.get(service_name.lower())

# exercises
def display_tool_banner(tool_name, version): 
	print(f"--- {tool_name} v{version} ---")

def check_service_keywords(service_name, keywords_list): 
	print(f"[+] Analayzing keywords for service: {service_name}")
	for keyword in keywords_list: 
		print(f"Looking for potential issue: {keyword} in {service_name}")
	