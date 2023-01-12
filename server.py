import cv2
import pickle
import socket
import struct

TCP_IP = '127.0.0.1'
TCP_PORT = 9501

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(5)
print("server is listening")

payload_size = struct.calcsize("I")
client_socket, client_address = sock.accept()
print('connection established with ' ,client_address)

data = b''
while True:
    while len(data) < payload_size:
        data += client_socket.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("I", packed_msg_size)[0]
    while len(data) < msg_size:
        data += client_socket.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    if frame_data=='':
        break
    frame=pickle.loads(frame_data)
    ret2, frame2 = cv2.imencode(".jpg", frame)
    print(frame2)
    
    cv2.imshow("window", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
socket.close()
