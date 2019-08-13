from http.server import BaseHTTPRequestHandler,HTTPServer
import cgi
import urllib
import json
import cv2
import time
import os
import base64
from io import BytesIO
from base64 import b64encode
from json import dumps

PORT = 3000



    
class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello')
        print('hey get!')
        
    def do_POST(self):
        
        #s = str(self.rfile.readline(),'UTF-8')
        #print(urllib.parse_qs(urllib.parse.unquote(s)))
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        #print(body)
        body_data = str(body,encoding = 'utf-8')
        post_data = json.loads(body_data)
        image_base64_1 = post_data['photo_base64_1']
        image_base64_2 = post_data['photo_base64_2']
        image_base64_3 = post_data['photo_base64_3']
        
        image_data_1 = base64.b64decode(image_base64_1)
        image_data_2 = base64.b64decode(image_base64_2)
        image_data_3 = base64.b64decode(image_base64_3)
        
        with open('imagedecode1.jpg','wb') as jpg_file:
            jpg_file.write(image_data_1)
        
        '''
        p=os.popen('sudo /home/pi/weight')
        x = p.read()
        p.close()
        
        newPath = "/home/pi/merchandise/"+str(body,encoding = 'utf-8')
        if(not(os.path.exists(newPath))):
            os.mkdir(newPath)
        
        f = open(newPath+'/list.txt','a')
        f.write(x)
        f.write(str(body,encoding = 'utf-8'))
        f.close()
        raw_data = {}
        raw_data['code'] = str(body,encoding = 'utf-8')
        raw_data['weight'] = x
        
        ENCODING = 'utf-8'
        cap = cv2.VideoCapture(0)
        for i in range(1,4):
            ret,frame = cap.read()
            if(ret):
                
                cv2.imshow("cap",frame)
                cv2.imwrite(newPath+'/'+str(i)+'.jpg',frame)
                cv2.waitKey(1)
                with open(newPath+'/'+str(i)+'.jpg','rb') as jpgfile:
                    byte_content = jpgfile.read()
                    base64_bytes= b64encode(byte_content)
                    base64_str = base64_bytes.decode(ENCODING)
                    raw_data['photo_base64'+str(i)] = base64_str
            
        cap.release()
        json_data = dumps(raw_data,indent =2)
        with open(newPath+'/info.json','a') as json_file:
            json_file.write(json_data)
        #data = body.encode('utf-8')
        #strbody = str(body,encoding= 'utf-8')
        #code = strbody.split('=')
        #print(code[1])
        #print(jsonstr)
        #print(json_dict)
        '''
        self.send_response(200)
        self.end_headers()
        
        response = BytesIO()
        response.write(b'hey!')
        response.write(b'received:')
        #response.write(body)
        
        self.wfile.write(response.getvalue())
        

httpd = HTTPServer(('localhost',PORT),myHandler)
httpd.serve_forever()