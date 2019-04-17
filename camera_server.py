import socket
import sys
import cv2
import pickle
import numpy as np
import struct

HOST = ''
PORT = 6666   #porta aperta al mio asus

serversocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

serversocket.bind((HOST, PORT))
print('Socket bind complete')
serversocket.listen(10)
print('Socket now listening')
conn, addr = serversocket.accept()

cap=cv2.VideoCapture('http://192.168.1.176:7777/video')
while True:
    ret,frame=cap.read()
    data = pickle.dumps(frame) ### new code
    conn.sendall(struct.pack("L", len(data))+data) ### new code

	
