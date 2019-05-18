# "convex Hull is a technique which will connect the
# outer most pixel in image in our case it is the outer
# most pixel of our finger"

import cv2
import numpy as np

hand = cv2.imread("handPic.jpg",0)

#thresholding
ret, the = cv2.threshold(hand, 70, 255, cv2.THRESH_BINARY)

#finding countours
# to find  the connected pixel

__, countours, __ = cv2.findContours(the.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

hull = [cv2.convexHull(c) for c in countours ]


cv2.imshow("hanndpic",hand)

cv2.waitKey(0)
