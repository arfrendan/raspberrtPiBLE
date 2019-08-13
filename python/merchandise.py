import sys
import json
import cv2
import time
import requests
import os
import pymysql
import pygame
from io import BytesIO
from base64 import b64encode
from json import dumps
from country_check import check_country,check_country_ch

url = 'http://192.168.0.171:3000'
barcode = sys.argv[1]

#create a folder to save the infos
newPath = "/home/pi/merchandise/"+barcode
if(not(os.path.exists(newPath))):
    os.mkdir(newPath)
    
#create a json to post to the server
post_data = {}

#get the barcode
print('barcode:'+barcode)
post_data['code'] = barcode
                    
#date & time logger
now_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
post_data['log_time'] = now_time

#get the weight measurement
p=os.popen('sudo /home/pi/weight')
x = p.read()
p.close()
post_data['weight'] = x
print('the weight:'+x)
       
#get the country of the merchandise
country = check_country_ch(barcode)
print(country)


#a transcript for the datainfo of the merchandise
f = open(newPath+'/list.txt','w')
f.write('weight='+x+'\n')
f.write("barcode=" + barcode+'\n')
f.write('logging time:'+now_time)
f.write('country:'+country)
f.close()

#save to database
conn = pymysql.connect(host = 'localhost',user='root',passwd = 'root',db = 'test')
cursor = conn.cursor()
insert = "INSERT INTO MERCHANDISE(M_CODE, M_TIME,M_WEIGHT) VALUES('%s','%s',%f)" %(barcode,now_time,float(x))
truncate = "ON DUPLICATE KEY UPDATE M_TIME = '%s', M_WEIGHT = %f" %(now_time,float(x))     
try:
    cursor.execute(insert+truncate)
    conn.commit()
    print('result')
except:
    print('err')
    conn.rollback()
    
#take photoshots of the merchandise
ENCODING = 'utf-8'
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,800)
for i in range(1,2):
    ret,frame = cap.read()
    if(ret):
        cv2.imshow("cap",frame)
        cv2.imwrite(newPath+'/photo'+str(i)+'.jpg',frame)
        cv2.waitKey(1)
        with open(newPath+'/photo'+str(i)+'.jpg','rb') as jpgfile:
            byte_content = jpgfile.read()
            base64_bytes= b64encode(byte_content)
            base64_str = base64_bytes.decode(ENCODING)
            photo_insert = "UPDATE MERCHANDISE SET M_PHOTO_%d='%s' WHERE M_CODE = '%s'"%(i,base64_str,barcode)
                                
            cursor.execute(photo_insert)
            conn.commit()
            post_data['photo_base64_'+str(i)] = base64_str
cap.release()
cv2.destroyAllWindows()
                    
#close the database
conn.close()

#transfer to json data and post to the server
json_data = dumps(post_data,indent =2)
with open(newPath+'/info.json','a') as json_file:
    json_file.write(json_data)
#r = requests.post(url,data = json_data

#play a notifying sound
pygame.mixer.init()
pygame.mixer.music.load('/home/pi/ok.mp3')
pygame.mixer.music.play()
time.sleep(4)
pygame.mixer.music.stop()