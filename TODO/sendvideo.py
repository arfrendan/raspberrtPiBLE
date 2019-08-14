import socket
import threading
import struct
import time
import cv2
import picamera
import io

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(('192.168.0.93',8080))
connection = client_socket.makefile('wb')
try:
    with picamera.PiCamera() as camera:
        camera.resolution=(640,320)
        camera.framerate = 15
        time.sleep(1)
        start = time.time()
        stream = io.BytesIO()
        
        for foo in camera.capture_continuous(stream,'jpeg',use_video_port = True):
            connection.write(struct.pack('<L',stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            if time.time() - start >600:
                break
            stream.seek(0)
            stream.truncate()
    connection.write(struct.pack('<L',0))
finally:
    connection.close()
    client_socket.close()
    