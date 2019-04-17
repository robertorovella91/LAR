import cv2
import numpy as np
import socket
import sys
import pickle
import struct ### new code
import multiprocessing as mp
from multiprocessing import Process

IP_ROBOT = '192.168.1.131'
PORT_ROBOT_LEFT = 9999
PORT_ROBOT_RIGHT = 8888

def Cam_Stream(_IP_ROBOT,_PORT_ROBOT):

	#IP_ROBOT = 'X.X.X.X' #locale
	#PORT_ROBOT = 8888 #locale

	clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	clientsocket.connect((_IP_ROBOT,_PORT_ROBOT))


	data = b''
	payload_size = struct.calcsize("L")

	while True:
	    while len(data) < payload_size:
		    data += clientsocket.recv(4096)
	    packed_msg_size = data[:payload_size]

	    data = data[payload_size:]
	    msg_size = struct.unpack("L", packed_msg_size)[0]
	
	    while len(data) < msg_size:
		    data += clientsocket.recv(4096)
	    frame_data = data[:msg_size]
	    data = data[msg_size:]

	    frame=pickle.loads(frame_data)
	    #print(frame.size)
	    cv2.imshow('frame', frame)
	    cv2.waitKey(10)


pleft = mp.Process(target = Cam_Stream, args =(IP_ROBOT,PORT_ROBOT_LEFT) ) 
pright = mp.Process(target = Cam_Stream, args =(IP_ROBOT,PORT_ROBOT_RIGHT) ) 

pleft.start() 
pright.start() 
pleft.join() 
pright.join() 





