from socket_practice.simple_port_checker import check_port, port_check
host_name = input("Please enter the ip addres or domain of host: ")
ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389]
port_check(host_name, ports, 2)
 


