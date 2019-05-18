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
    ret ,thresh =  cv2.threshold(filtered, 127, 255, 0)

    # threshold image
    cv2.imshow("Thresholded Image", thresh)

    #Getting Countours

    image,contour,herrachy =    cv2.findContours(thresh, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)

    try:
        # find contour with maximum area
        MaxContour =  max(contour, key=lambda x: cv2.contourArea(x))

        #Create Bounding Rectangle around Contour
        x, y, w, h = cv2.boundingRect(MaxContour)
        cv2.rectangle(crop_image, (x, y), (x + w, y +h) (0, 0 ,255), 0)

        #Applying Convex Hull

        hull= cv2.convexHull(MaxContour)

        #draw Countour
        drawing = np.zeros(crop_image , dtype="uint8")
        cv2.drawContours(drawing, [MaxContour], -1, (0, 255, 0),0 )
        cv2.drawContours(drawing, [hull], -1, (0, 255, 0), 0)

        #find convexity defect
        hull = cv2.convexHull(MaxContour, returnPoints= False)
        defects = cv2.convexityDefects(MaxContour, hull)

        #useing cosine rule to find the far point from the start and end point

        count_defect = 0

        for i in range(defects.shape[0]):
            s, e, f, d = defects[i ,0]
            start = tuple(MaxContour[s][0])
            end = tuple(MaxContour[e][0])
            far = tuple(MaxContour[f][0])

            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
            angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14

            # if angle > 90 draw a circle at the far point
            if angle <= 90:
                count_defect += 1
                cv2.circle(crop_image, far, 1, [0, 0, 255], -1)

            cv2.line(crop_image, start, end, [0, 255, 0], 2)

        if count_defects == 0:
            cv2.putText(frame, "AK UNGLI", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
        elif count_defects == 1:
            cv2.putText(frame, "DO UNGLI ", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
        elif count_defects == 2:
            cv2.putText(frame, "TEEN UNGLI", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
        elif count_defects == 3:
            cv2.putText(frame, "CHAAR UNGLI", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
        elif count_defects == 4:
            cv2.putText(frame, "PANCH UNGLI", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
        else:
            pass
    except:
        pass
