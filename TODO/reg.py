from picamera.array import PiRGBArray
from picamera import PiCamera
from functools import partial

import multiprocessing as mp
import cv2
import os
import time
import numpy as np

os.putenv('SDL_FBDEV','/dev/fb0') 

resX =  320
resY = 240

cx = resX/2
cy = resY/2

xdeg = 150 
ydeg = 150

camera = PiCamera()
camera.resolution = (resX,resY)
camera.framerate = 60

rawCapture = PiRGBArray(camera,size = (resX,resY))

face_cascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
banana_cascade = cv2.CascadeClassifier('/home/pi/banana_classifier.xml')
sunflower_cascade = cv2.CascadeClassifier('/home/pi/sunflower.xml')
soccer_cascade = cv2.CascadeClassifier('/home/pi/football.xml')
piano_cascade = cv2.CascadeClassifier('/home/pi/piano.xml')
coca_cascade = cv2.CascadeClassifier('/home/pi/coca.xml')



t_start = time.time()
fps = 0

def get_faces(img):
    image =img
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = coca_cascade.detectMultiScale(gray,minNeighbors = 20 , minSize = (50,50))
    return faces,img

def get_color(colorHSV):
    
    if colorHSV[2]<=46:
        return 0
    elif colorHSV[2]<=220 and colorHSV[1]<=43:
        return 1
    elif colorHSV[2]>=221 and colorHSV[1]<=30:
        return 2
    elif ((colorHSV[0]<=10)or(colorHSV[0]>=156)) and colorHSV[1]>=43 :
        return 3
    elif colorHSV[0]>=11 and colorHSV[0]<=25 and colorHSV[1]>=43 :
        return 4
    elif colorHSV[0]>=26 and colorHSV[0]<=34 and colorHSV[1]>=43 :
        return 5
    elif colorHSV[0]>=35 and colorHSV[0]<=77 and colorHSV[1]>=43 :
        return 6
    elif colorHSV[0]>=78 and colorHSV[0]<=99 and colorHSV[1]>=43 :
        return 7
    elif colorHSV[0]>=100 and colorHSV[0]<=124 and colorHSV[1]>=43 :
        return 8
    elif colorHSV[0]>=125 and colorHSV[0]<=155 and colorHSV[1]>=43 :
        return 9
    else:
        return -1
    
def img_color(imgHsv):
    
    color = {
    'bla':0,
    'whi':0,
    'gra':0,
    'red':0,
    'ora':0,
    'yel':0,
    'lig':0,
    'deg':0,
    'blu':0,
    'pur':0,
    'unk':0
    }
    
    width = imgHsv.shape[0]
    height = imgHsv.shape[1]
    for i in range(5):
        for j in range(5):
            ri = int(np.random.random()*width*0.5+width*0.25)
            rj = int(np.random.random()*height*0.5+height*0.25)
            pixel = imgHsv[ri][rj]
            if(get_color(pixel) == 0):
                color['bla'] += 1
            elif(get_color(pixel) == 1):
                color['whi'] += 1
            elif(get_color(pixel) == 2):
                color['gra'] += 1
            elif(get_color(pixel) == 3):
                color['red'] += 1
            elif(get_color(pixel) == 4):
                color['ora'] += 1
            elif(get_color(pixel) == 5):
                color['yel'] += 1
            elif(get_color(pixel) == 6):
                color['lig'] += 1
            elif(get_color(pixel) == 7):
                color['deg'] += 1
            elif(get_color(pixel) == 8):
                color['blu'] += 1
            elif(get_color(pixel) == 9):
                color['pur'] += 1
            elif(get_color(pixel) == -1):
                color['unk'] += 1
    max_color = max(zip(color.values(),color.keys()))
    return max_color[1]
    
    
def draw_frame(img,faces):
    global xdeg
    global ydeg
    global fps
    global time_t
    r = 0
    b = 0
    g = 0
    for(x,y,w,h) in faces:
        cut = img[y:y+h,x:x+w]
        hsv = cv2.cvtColor(cut,cv2.COLOR_BGR2HSV)
        print(img_color(hsv))
                
        cv2.rectangle(img,(x,y),(x+w,y+h),(200,255,0),2)
        #cv2.putText(img,"face No."+str(len(faces)),(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
        #'''
        if(img_color(hsv)=='red'):
            cv2.putText(img,"coca No."+str(len(faces)),(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
        if(img_color(hsv)=='blu'):
            cv2.putText(img,"sprite No."+str(len(faces)),(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
        if(img_color(hsv)=='ora'):
            cv2.putText(img,"fanta No."+str(len(faces)),(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
        if(img_color(hsv)=='deg' or img_color(hsv)=='lig'):
            cv2.putText(img,"7up No."+str(len(faces)),(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
        #'''
        '''
        tx = x+w/2
        ty = y+h/2
        
        if (cx-tx >15 and xdeg <= 190):
            xdeg += 1
            os.system("sudo echo 0="+str(xdeg)+"> /dev/servoblaster" )
        elif(cx-tx <-15 and xdeg >= 110):
            xdeg -= 1
            os.system("sudo echo 0="+str(xdeg)+"> /dev/servoblaster" )
            
        if (cy-ty >15 and ydeg >= 110):
            ydeg -= 1
            os.system("sudo echo 1="+str(xdeg)+"> /dev/servoblaster" )
        elif(cy-ty <-15 and xdeg <=190):
            ydeg += 1
            os.system("sudo echo 1="+str(xdeg)+"> /dev/servoblaster" )
        ''' 
    fps = fps + 1
    sfps = fps/ (time.time() - t_start)
    cv2.putText(img,"FPS:" + str(int(sfps)),(10,10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
        
    cv2.imshow("frame",img)
    cv2.waitKey(1)

def main():
    pool = mp.Pool(processes = 4)
    fcount = 0
    
    camera.capture(rawCapture,format = "bgr")
    
    r1 = pool.apply_async(get_faces,[rawCapture.array])
    r2 = pool.apply_async(get_faces,[rawCapture.array])
    r3 = pool.apply_async(get_faces,[rawCapture.array])
    r4 = pool.apply_async(get_faces,[rawCapture.array])
    
    f1,i1 = r1.get()
    f2,i2 = r2.get()
    f3,i3 = r3.get()
    f4,i4 = r4.get()
    
    rawCapture.truncate(0)
    
    for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
        image = frame.array
        
        if fcount == 1:
            r1 = pool.apply_async(get_faces,[image])
            f2,i2 = r2.get()
            draw_frame(i2,f2)
        elif fcount == 2:
            r2 = pool.apply_async(get_faces,[image])
            f3,i3 = r3.get()
            draw_frame(i3,f3)
        if fcount == 3:
            r3 = pool.apply_async(get_faces,[image])
            f4,i4 = r4.get()
            draw_frame(i4,f4)
        if fcount == 4:
            r4 = pool.apply_async(get_faces,[image])
            f1,i1 = r1.get()
            draw_frame(i1,f1)
            
            fcount = 0
        fcount += 1
        rawCapture.truncate(0)
            
if __name__ == '__main__':
    main()
            
            