import requests
import evdev
import signal,sys
import cgi
import urllib
import json
import cv2
import time
import os
from io import BytesIO
from base64 import b64encode
from json import dumps

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
scancodes = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
}
device = None
barcodeScannerName = "HID 0581:020c Keyboard"
for dev in devices:
    if dev.name == barcodeScannerName:
        device = evdev.InputDevice(dev.fn)
        
url = 'http://127.0.0.1:3000'

#device.grab()
barcode = ""

def acquisition():
	if(device):
		for event in device.read_loop():
			if event.type == evdev.ecodes.EV_KEY:
				data = evdev.categorize(event)
				if data.keystate == 1 and data.scancode!=42:
					if data.scancode == 28:
						#create a folder to save the infos
						newPath = "../merchandise/"+barcode
						if(not(os.path.exists(newPath))):
							os.mkdir(newPath)
						f = open(newPath+'/list.txt','a')
						
						#get the barcode
						print('barcode:'+barcode)
						post_data = {}
						post_data['code'] = barcode
						
						#get the weight measurement
						p=os.popen('sudo /home/pi/weight')
						x = p.read()
						p.close()
						post_data['weight'] = x
						print('the weight:'+x)
						
						#a transcript for the data info of the merchandise
						f = open(newPath+'/list.txt','a')
						f.write(x+'\n')
						f.write("barcode=" + barcode)
						f.close()
						
						#take photoshots of the merchandise
						ENCODING = 'utf-8'
						cap = cv2.VideoCapture(0)
						cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
						cap.set(cv2.CAP_PROP_FRAME_HEIGHT,960)
						for i in range(1,4):
							ret,frame = cap.read()
							if(ret):
								cv2.imshow("cap",frame)
								cv2.imwrite(newPath+'/photo'+str(i)+'.jpg',frame)
								cv2.waitKey(1)
								with open(newPath+'/photo'+str(i)+'.jpg','rb') as jpgfile:
									byte_content = jpgfile.read()
									base64_bytes= b64encode(byte_content)
									base64_str = base64_bytes.decode(ENCODING)
									post_data['photo_base64_'+str(i)] = base64_str
						cap.release()
						cv2.destroyAllWindows()
						#transfer to json data and post to the server
						json_data = dumps(post_data,indent =2)
						with open(newPath+'/info.json','a') as json_file:
							json_file.write(json_data)
						r = requests.post(url,data = json_data)
						
						barcode = ""
					else:
						barcode += scancodes[data.scancode]
	else:
		print('no printer founded...')


