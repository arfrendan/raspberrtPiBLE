import cv2
import time
import os
import multiprocessing as mp

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
def shoot():
	while(1):
		ret,frame = cap.read()
		cv2.imshow("cap",frame)
		if cv2.waitKey(1) & 0xFF == ord('p'):
			for i in range(0,150):
				ret,frame = cap.read()
				cv2.imwrite("./Pictures/pos/"+str(i)+".jpg",frame)
				cv2.imshow("cap",frame)
				cv2.waitKey(100)
		elif cv2.waitKey(1) & 0xFF == ord('n'):
			for i in range(0,300):
				ret,frame = cap.read()
				cv2.imwrite("./Pictures/neg/"+str(i)+".jpg",frame)
				cv2.imshow("cap",frame)
				cv2.waitKey(50)
		elif cv2.waitKey(1) & 0xFF == ord('q'):
			break
		elif cv2.waitKey(1) & 0xFF == ord('s'):
			p=os.popen('sudo weight')
			x = p.read()
			print(x)
			f = open('../merchandise/test.txt','a')
			f.write(x)
			f.close()
	cap.release()
	cv2.destroyAllWindows()

