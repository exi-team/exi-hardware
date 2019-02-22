import socket
from socket import error as SocketError
import RPi.GPIO as GPIO

sock = socket.socket()
sock.bind(('192.168.1.37', 9090))
sock.listen(1)
GPIO.setmode(GPIO.BOARD)
curState1 = False
curState2 = False

def cmdTurnOn(led):
	GPIO.setup(led, GPIO.OUT)
	GPIO.output(led, True)

def cmdTurnOff(led):
	GPIO.setup(led, GPIO.OUT)
	GPIO.output(led, False)	

while True:
	conn, addr = sock.accept()

	print("Connected: ", addr);

	while True:
		try:
			data=conn.recv(2)
		except SocketError as e:
			break
		if not data:
			break

		if data[0]=="o":
			print("Turning led "+str(ord(data[1]))+" on")
			conn.send("Turning on "+str(ord(data[1]))+" led")
			cmdTurnOn(ord(data[1]));
			if ord(data[1])==3:
				curState1 = True;
			elif ord(data[1])==7:
				curState2 = True;
		elif data[0]=="f":
			print("Turning led "+str(ord(data[1]))+" off")
			conn.send("Turning off "+str(ord(data[1]))+" led")
			cmdTurnOff(ord(data[1]));
			if ord(data[1])==3:
				curState1 = False;
			elif ord(data[1])==7:
				curState2 = False;
		elif data[0]=="c":
			print("Checking socket #"+str(ord(data[1]))+".");
			if ord(data[1])==3:
				conn.send(str(curState1)+"\r\n");
			elif ord(data[1])==7:
				conn.send(str(curState2)+"\r\n");
			else:
				conn.send("no");
		else:
			conn.send("Unknown cmd '"+data[0]+"'")

GPIO.cleanup()
conn.close()
