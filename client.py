import cv2
import pickle
import socket
import struct

TCP_IP = '127.0.0.1'
TCP_PORT = 9501
server_address = (TCP_IP, TCP_PORT)


streamer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
streamer.connect((TCP_IP,TCP_PORT))


while True:
    cap = cv2.VideoCapture(0)
    pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    while True:
        flag, frame = cap.read()
        if flag:
            frame = pickle.dumps(frame)
            size = len(frame)
            p = struct.pack('I', size)
            frame = p + frame
            streamer.sendall(frame)
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, pos_frame-1)
      
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            size = 10
            p = struct.pack("I", size)
            streamer.send(p)
            streamer.send('')
            break
    streamer.close()