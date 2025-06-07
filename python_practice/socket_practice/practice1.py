import socket

try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket succcessfully created")
except socket.error as err: 
    print(f"Socket creation failed with error: {err}")
s.close()
