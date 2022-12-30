import numpy as np
import cv2
import time
import datetime
from collections import deque
import telegram


def is_person_present(frame, thresh=1100):
    global foog
    fgmask = foog.apply(frame)
    ret, fgmask = cv2.threshold(fgmask, 250, 255, cv2.THRESH_BINARY)
    fgmask = cv2.dilate(fgmask, None, iterations=4)
    contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours and cv2.contourArea(max(contours, key=cv2.contourArea)) > thresh:
        cnt = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, 'Person Detected', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1, cv2.LINE_AA)

        return True, frame

    else:
        return False, frame


def sendMessage(body):
    my_token = "5722526497:AAEI_FoFddGf55OJZlDtZgtsC3GaJn0SkNM"
    bot = telegram.Bot(token=my_token)
    bot.sendVideo(chat_id="5408192472", text= body)

# 'http://192.168.1.6:8080/video'
cv2.namedWindow('frame', cv2.WINDOW_KEEPRATIO)
cap = cv2.VideoCapture("test.mp4")
width = int(cap.get(3))
height = int(cap.get(4))

foog = cv2.createBackgroundSubtractorMOG2(detectShadows=True, varThreshold=100, history=2000)

status = False

patience = 7

detection_thresh = 15

initial_time = None

de = deque([False] * detection_thresh, maxlen=detection_thresh)

# Initialize these variables for calculating FPS
fps = 0
frame_counter = 0
start_time = time.time()

while (True):

    ret, frame = cap.read()
    if not ret:
        break

    detected, annotated_image = is_person_present(frame)
    de.appendleft(detected)

    if sum(de) == detection_thresh and not status:
        status = True
        entry_time = datetime.datetime.now().strftime("%A, %I-%M-%S %p %d %B %Y")
        out = cv2.VideoWriter('outputs/{}.avi'.format(entry_time), cv2.VideoWriter_fourcc(*'XVID'), 15.0,
                              (width, height))

    if status and not detected:

        if sum(de) > (detection_thresh / 2):
            if initial_time is None:
                initial_time = time.time()

        elif initial_time is not None:
            if time.time() - initial_time >= patience:
                status = False
                exit_time = datetime.datetime.now().strftime("%A, %I:%M:%S %p %d %B %Y")
                out.release()
                initial_time = None

                # img_name = "arlet.png".format(img_counter)
                # cv2.imwrite(img_name, frame)
                body = "Alert: \n A Person Entered the Room at {} \n Left the room at {}".format(entry_time, exit_time)
                sendMessage(body)

    elif status and sum(de) > (detection_thresh / 2):
        initial_time = None

    # Get the current time in the required format
    current_time = datetime.datetime.now().strftime("%A, %I:%M:%S %p %d %B %Y")

    cv2.putText(annotated_image, 'FPS: {:.2f}'.format(fps), (1500, 20), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 40, 155),
                2)
    cv2.putText(annotated_image, current_time, (310, 20), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 255), 2)
    cv2.putText(annotated_image, 'Room Occupied: {}'.format(str(status)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (200, 10, 150), 2)

    if initial_time is None:
        text = 'Patience: {}'.format(patience)
    else:
        text = 'Patience: {:.2f}'.format(max(0, patience - (time.time() - initial_time)))

    cv2.putText(annotated_image, text, (1000, 20), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 40, 155), 2)

    if status:
        out.write(annotated_image)

    cv2.imshow('frame', frame)
    frame_counter += 1
    fps = (frame_counter / (time.time() - start_time))
    if cv2.waitKey(30) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()