import numpy as np
import cv2
import imutils
from pyzbar import pyzbar
import time
import sys
import re

def decode(image):
    barcodes = pyzbar.decode(image)
    for barcode in barcodes:
        (x,y,w,h) = barcode.rect
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),5)
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        text = "{}({})".format(barcodeData,barcodeType)
        cv2.putText(image,text,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
        return [barcodeData,barcodeType]
        
def detect_barcode(image):
		
		image = image.copy()
		gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

		gradX = cv2.Sobel(gray,ddepth = cv2.CV_32F,dx = 1, dy = 0,ksize = -1)
		gradY = cv2.Sobel(gray,ddepth = cv2.CV_32F,dx = 0, dy = 1,ksize = -1)
		gradient = cv2.subtract(gradX,gradY)
		gradient = cv2.convertScaleAbs(gradient)

		blurred = cv2.blur(gradient,(9,9))
		(_,thresh) = cv2.threshold(blurred,225,255,cv2.THRESH_BINARY)

		kernel = cv2.getStructuringElement(cv2.MORPH_RECT , (21,7))
		closed = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel)

		closed = cv2.erode(closed, None , iterations= 4)
		closed = cv2.dilate(closed, None , iterations= 4)
		
		cv2.imshow('black',closed)
		cnts = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		if len(cnts):
			c=sorted(cnts, key = cv2.contourArea , reverse = True)[0]
			rect = cv2.minAreaRect(c)
			box = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
			box = np.int0(box)			
			if len(box) :
				Xs = [i[0] for i in box]
				Ys = [i[1] for i in box]
				x1 = min(Xs)
				x2 = max(Xs)
				y1 = min(Ys)
				y2 = max(Ys)
				
				height = y2-y1
				width = x2-x1
				if (y1-20>0 and x1-20>0 and y1+height+20>0 and x1+width+20>0):
					cropImg = frame[y1-20:y1+height+20,x1-20:x1+width+20]
					barcode = decode(cropImg)
					if(barcode != None ):
						if(re.match('^69\d{11}',barcode[0])):
							cv2.imshow("cutted image",cropImg)
							print(barcode[0],barcode[1])
							sys.stdout.flush()
	

