import cv2
try:
    cap = cv2.VideoCapture(0)
    ret,frame = cap.read()
    cv2.imshow('frame',frame)
    cap.release()
    cv2.destroyAllWindows()
    print(0,end = '')
except:
    print(-1,end = '')