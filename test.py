import cv2
import numpy as np

cap = cv2.VideoCapture('test.mp4')

while True:
    ret, frame = cap.read()

    cv2.imshow("Window", frame)

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()