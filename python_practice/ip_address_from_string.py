import re 

ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
found_ips = re.findall(ip_pattern, text)


