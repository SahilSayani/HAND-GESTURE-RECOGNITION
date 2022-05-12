import cv2
import numpy as np
import mediapipe as mp
import time
import pyautogui as py
from scipy.spatial import distance
import threading
import os, urllib.request
# from django.conf import settings

class VideoCamera(object):

    def __init__(self):
        self.vid = cv2.VideoCapture(0)

    def __del__(self):
        self.vid.release()



    def get_frame(self):
        success, image = self.vid.read()

        tipIds = [4, 8, 12, 16, 20]

        mpHands = mp.solutions.hands
        mpDraw  = mp.solutions.drawing_utils
        hands   = mpHands.Hands(static_image_mode=False,
                                            max_num_hands=1,
                                            model_complexity=1,
                                            min_detection_confidence=0.8,
                                            min_tracking_confidence=0.5)



        if success == True:
            img = cv2.flip(image, 1)

            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    mpDraw.draw_landmarks(imgRGB, handLms, mpHands.HAND_CONNECTIONS)

            img = cv2.cvtColor(imgRGB, cv2.COLOR_BGR2RGB)
            if results.multi_hand_landmarks != None:
                normalizedLandmark = results.multi_hand_landmarks[0].landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
                print(normalizedLandmark)

            # t1 = threading.Thread(target=move_cursor, args=(results, mpHands))
            # t2 = threading.Thread(target=click, args=(results, mpHands))
            
            #             # starting thread 1
            # t1.start()
            #             # starting thread 2
            # t2.start()
            
            #             # wait until thread 1 is completely executed
            # t1.join()
            #             # wait until thread 2 is completely executed
            # t2.join()

        ret, jpg = cv2.imencode('.jpg',img)
        return jpg.tobytes()
# comment below code to get website
    def move_cursor(results, mpHands):
            if results.multi_hand_landmarks != None:
                normalizedLandmark = results.multi_hand_landmarks[0].landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    
                rel_x = normalizedLandmark.x * (1919)
                rel_y = normalizedLandmark.y * (1079)
                py.moveTo(rel_x, rel_y)
    
    
    def click(results, mpHands):
            if results.multi_hand_landmarks != None:
                middle_tip = results.multi_hand_landmarks[0].landmark[mpHands.HandLandmark.MIDDLE_FINGER_TIP]
                thumb_tip = results.multi_hand_landmarks[0].landmark[mpHands.HandLandmark.THUMB_TIP]
    
                middle_tip_x = middle_tip.x
                middle_tip_y = middle_tip.y
                thumb_tip_x = thumb_tip.x
                thumb_tip_y = thumb_tip.y
                a = (middle_tip_x, middle_tip_y)
                b = (thumb_tip_x, thumb_tip_y)
                if (distance.euclidean(a, b) < 0.06):
                    py.click()


def main1():
    # Main video capture as webcamera
    vid = cv2.VideoCapture(0)
    py.FAILSAFE = False
    frameWidth = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    frameHeight = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    tipIds = [4, 8, 12, 16, 20]

    mpHands = mp.solutions.hands
    mpDraw  = mp.solutions.drawing_utils
    hands   = mpHands.Hands(static_image_mode=False,
                                    max_num_hands=1,
                                    model_complexity=1,
                                    min_detection_confidence=0.8,
                                    min_tracking_confidence=0.5)
    pTime = 0
    checker=1
    while checker==1:
        # Video read
        var, img = vid.read()

        if var == True:
            img = cv2.flip(img, 1)

            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    mpDraw.draw_landmarks(imgRGB, handLms, mpHands.HAND_CONNECTIONS)

            t1 = threading.Thread(target=move_cursor, args=(results, mpHands))
            t2 = threading.Thread(target=click, args=(results, mpHands))

            # starting thread 1
            t1.start()
            # starting thread 2
            t2.start()

            # wait until thread 1 is completely executed
            t1.join()
            # wait until thread 2 is completely executed
            t2.join()

            img = cv2.cvtColor(imgRGB, cv2.COLOR_BGR2RGB)


            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 255), 3)

            cv2.imshow("video", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                checker=0
                break


def move_cursor(results, mpHands):
        if results.multi_hand_landmarks != None:
            normalizedLandmark = results.multi_hand_landmarks[0].landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]

            rel_x = normalizedLandmark.x * (1919)
            rel_y = normalizedLandmark.y * (1079)
            py.moveTo(rel_x, rel_y)


def click(results, mpHands):
        if results.multi_hand_landmarks != None:
            middle_tip = results.multi_hand_landmarks[0].landmark[mpHands.HandLandmark.MIDDLE_FINGER_TIP]
            thumb_tip = results.multi_hand_landmarks[0].landmark[mpHands.HandLandmark.THUMB_TIP]

            middle_tip_x = middle_tip.x
            middle_tip_y = middle_tip.y
            thumb_tip_x = thumb_tip.x
            thumb_tip_y = thumb_tip.y
            a = (middle_tip_x, middle_tip_y)
            b = (thumb_tip_x, thumb_tip_y)
            if (distance.euclidean(a, b) < 0.06):
                py.click()

main1()
