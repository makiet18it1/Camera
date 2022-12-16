# Import the required libraries
import numpy as np

import time
import argparse
import datetime
import cv2
import imutils
from collections import deque

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="Nguồn video mặc định 0 là sử dụng webcam", default='0', type=str)
ap.add_argument("-a", "--min-area", type=int, default=300, help="Kích thước nhỏ nhất của đối tượng")
ap.add_argument("-b", "--background", type=str, default=None, help="Ảnh background")
args = vars(ap.parse_args())

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

start_time = time.time()

fps = 0
frame_counter = 0

if args['video'] == '0':
    cap = cv2.VideoCapture('http://192.168.1.9:8080/video')
else:
    cap = cv2.VideoCapture(args['video'])

first_frame = None
if args['background'] is not None:
    first_frame = cv2.imread(args['background'])

    first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

    first_gray = cv2.GaussianBlur(first_gray, (21, 21), 0)

idx = 0

top_left, bottom_right = (100, 700), (500, 100)

# img_counter = 0

while (True):

    ret, frame = cap.read()
    if frame is None:
        break
    text = "An toan"
    # Resize ảnh về kích thước cố định
    frame = imutils.resize(frame, width=1500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # cv2.imshow("Current frame", frame)

    if first_frame is None:
        first_frame = frame
        first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
        first_gray = cv2.GaussianBlur(first_gray, (21, 21), 0)

    frameDelta = cv2.absdiff(first_gray, gray)

    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
    cv2.putText(frame, "Tinh trang: {}".format(text), (00, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    frame_counter += 1
    fps = (frame_counter / (time.time() - start_time))

    # Display the FPS
    cv2.putText(frame, 'FPS: {:.2f}'.format(fps), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

    for c in cnts:

        if cv2.contourArea(c) < args["min_area"]:
            continue

        (x, y, w, h) = cv2.boundingRect(c)

        center_x = x + w / 2
        center_y = y + h / 2

        logic = top_left[0] < center_x < bottom_right[0] and top_left[1] < center_y < bottom_right[1]

        if logic:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            text = "Co xam nhap"

    cv2.imshow('Camera An Ninh', frame)
    # cv2.imshow("Thresh", thresh)
    cv2.imwrite('/images/{}_result.png'.format(idx), frame)
    cv2.imwrite('../images/{}_delta.jpg'.format(idx), frameDelta)
    # cv2.imshow("Frame Delta", frameDelta)
    idx += 1



    # Exit if q is pressed.
    if cv2.waitKey(1) == ord('q'):
        break

# Release Capture and destroy windows
cap.release()
cv2.destroyAllWindows()
