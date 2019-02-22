import socket

sock = socket.socket()
sock.connect(('192.168.1.37', 9090))
sock.send("c"+chr(7));

data=sock.recv(1024)
sock.close()

print(data);
