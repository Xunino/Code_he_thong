import cv2
import numpy as np
import time
import imutils

cap = cv2.VideoCapture('./data/videos/test1.mp4')
if cap.isOpened():
    print("Video Ok...!")
else:
    print("Fail")

count = 0
success = True
while success:
    
    success, frame = cap.read()

    time.sleep(5)

    cv2.imwrite("./data/images/output_{}.jpg".format(count), frame)    
    
    count +=1
    print("Successes")