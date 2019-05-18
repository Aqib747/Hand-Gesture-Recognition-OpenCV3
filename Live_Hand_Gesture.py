import cv2
import numpy as np
import math

#Open Camera

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow("frame", frame)

    cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 0)
    crop_image= frame[100:300, 100:300]

    #apply blur
    blur = cv2.GaussianBlur(crop_image, (3, 3), 0 )

    #BGR To HSV

    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # mask where white will be skin color and rest is black

    mask2 = cv2.inRange(hsv, np.array([2, 0, 0]), np.array([20, 225, 255]))

    #morpholigical transformation

    kernal = np.ones((5, 5))

    dilation = cv2.dilate(mask2, kernal , iterations= 1)
    erosion = cv2.erode(dilation, kernal, iterations= 1)

    #again gausian blur

    filtered = cv2.GaussianBlur(erosion, (3, 3), 0 )
    ret ,thresh = 