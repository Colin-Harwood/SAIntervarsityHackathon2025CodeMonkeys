import os
import cv2
import pygame
#loading the siren sound into pygame
pygame.mixer.init()
siren_path = "assets/siren.wav"
siren = pygame.mixer.Sound(siren_path)
def drawBoxes(frame , landmarks, eyesOpen):
    #getting eye cords and store them
    leftEYE, rightEYE = landmarks
    if (leftEYE is None or rightEYE is None):
        print ("Error: Cant see eyes")
        return None
    #getting dimentions for the left eye box
    lx_min, lx_max = float("inf"), float("-inf")
    ly_min, ly_max = float("inf"), float("-inf")
    for (x, y) in leftEYE:
        if x < lx_min:
            lx_min = x
        if x > lx_max:
            lx_max = x
        if y < ly_min:
            ly_min = y
        if y > ly_max:
            ly_max = y
    
    #getting dimentions for the right eye box
    rx_min, rx_max = float("inf"), float("-inf")
    ry_min, ry_max = float("inf"), float("-inf")
    for (x, y) in rightEYE:
        if x < rx_min:
            rx_min = x
        if x > rx_max:
            rx_max = x
        if y < ry_min:
            ry_min = y
        if y > ry_max:
            ry_max = y
    #drawing the boxes
    if (eyesOpen == False):
        cv2.rectangle(frame,(int(lx_min), int(ly_min)), (int(lx_max), int(ly_max)),(0, 255, 0), 2)
        cv2.rectangle(frame,(int(rx_min), int(ry_min)), (int(rx_max), int(ry_max)), (0, 255, 0), 2)
        cv2.putText(frame,"Driver Awake",(10, 30),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),2,cv2.LINE_AA)
        #stop the sound if it is playing
        if pygame.mixer.get_busy():
            siren.stop()
    else:
        cv2.rectangle(frame, (int(lx_min), int(ly_min)), (int(lx_max), int(ly_max)),(0, 0, 255), 2)
        cv2.rectangle(frame,(int(rx_min), int(ry_min)), (int(rx_max), int(ry_max)), (0, 0, 255), 2)
        cv2.putText(frame,"Driver Sleeping!",(10, 30),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 0, 255),2,cv2.LINE_AA)
        #Make a loud noise to alert the driver
        pygame.mixer.init()
        pygame.mixer.music.load(siren_path)
        pygame.mixer.music.play(loops=0)
        #play the sound if it is not already playing
        if not pygame.mixer.get_busy():
            siren.play()
        
    return frame
