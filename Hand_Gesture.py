# "convex Hull is a technique which will connect the
# outer most pixel in image in our case it is the outer
# most pixel of our finger"

"""for this example image has been used """

import cv2
import numpy as np

hand = cv2.imread("hand.png",0)

#thresholding
ret, the = cv2.threshold(hand, 70, 255, cv2.THRESH_BINARY)

#finding countours
# to find  the connected pixel

countours,Herraacy = cv2.findContours(the.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

hull = [cv2.convexHull(c) for c in countours ]

#drawing countours

final =cv2.drawContours(hand, hull, -1, (255, 0, 0), 3) 

cv2.imshow("orignalImage", hand)

cv2.imshow("threshold imgae", the)

cv2.imshow("Convexhull", final)
cv2.waitKey(0)
