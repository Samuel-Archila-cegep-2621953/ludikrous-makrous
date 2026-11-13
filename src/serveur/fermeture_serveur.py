import sys
import socket
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((sys.argv[1], int(sys.argv[2])))
        s.sendall('fermer'.encode())
        recu = s.recv(1024)
    s.close()
except:
    exit(0)