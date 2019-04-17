import socket
import sys
import cv2
import pickle
import numpy as np
import struct
import sys
import multiprocessing as mp
from multiprocessing import Process, Queue
import imutils


def Left():
    HOST = ''
    PORT = 6666  #porta aperta al mio asus

    serversocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    serversocket.bind((HOST, PORT))
    print('Socket bind complete')
    serversocket.listen(5)
    print('Socket now listening')
    conn, addr = serversocket.accept()
    cap=cv2.VideoCapture(0)
    
    while True:
        try:    
                ret,frame=cap.read()
                cv2.waitKey(10)
                frame = imutils.resize(frame, width=480)
                data = pickle.dumps(frame) ### new code
                conn.sendall(struct.pack("L", len(data))+data) ### new code
        except KeyboardInterrupt:
                serversocket.close()
        


def Right():
    HOST = ''
    PORT = 6667   #porta aperta al mio asus

    serversocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    serversocket.bind((HOST, PORT))
    print('Socket bind complete')
    serversocket.listen(5)
    print('Socket now listening')
    conn, addr = serversocket.accept()

    cap=cv2.VideoCapture('http://192.168.43.230:7777/video')
    while True:
        try:
                ret,frame=cap.read()
                cv2.waitKey(10)
                frame = imutils.resize(frame, width=480)
                data = pickle.dumps(frame) ### new code
                conn.sendall(struct.pack("L", len(data))+data) ### new code
        except KeyboardInterrupt:
                serversocket.close()
                break


p_left =mp.Process(target=Left)
p_right =mp.Process(target=Right)
processes =[p_left,p_right]
# print('Processes started')
# Run processes
for p in processes:
    p.start()
# Exit the completed processes
#print('Processes joined')
for p in processes:
    p.join()

        
