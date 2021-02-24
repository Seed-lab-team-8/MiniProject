import time
import numpy as np
import cv2
import cv2.aruco as aruco
import math

from picamera import PiCamera
from time import sleep
from picamera.array import PiRGBArray
import os
from PIL import Image


def findCenter(corners): # Get the center of the aruco image in x,y pixel coordinates by taking half the difference between the top left and bottom right pixel of the marker and adding that to the top left coordinate (bottom corner (lowest) with respect to (x,y) coordinates starting from top left of image at (0,0))
    return( (abs(((corners[0][0][2][0] - corners[0][0][0][0]))/2) + corners[0][0][0][0]),
            (abs(((corners[0][0][2][1] - corners[0][0][0][1]))/2) + corners[0][0][0][1]) )

#def writeNumber(value):
#    bus.write_byte(address, value)
#    return -1
#
#def readNumber():
#    number = bus.read_byte(address)
#    return number


print ("Use aruco to get wheel to move. Position 0 is angle 0, position 1 is angle pi/2, position 2 is angle pi, position 3 is angle 3*pi/4. Put the aruco in quadrant 1 (+x,+y) for position 0, quadrant 2 for position 1, quadrant 3 for position 2 and quadrant 4 for position 3 respectively. Press a key to continue.")
cv2.waitKey(0)

cap = cv2.VideoCapture(0)
i=0
while(i<50):
    _, frame = cap.read()
    #h,w,c = frame.shape
    #cv2.imshow('frame',frame)
    i=i+1
    
    h, w, c = frame.shape
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    if corners:
        try:
            center = findCenter(corners)
            print(center)
            if(center[0] > w/2 and center[1] < h/2): loc, pos = "Position 0: 0", 0
            if(center[0] < w/2 and center[1] < h/2): loc, pos = "Position 1: pi/2", 1
            if(center[0] < w/2 and center[1] > h/2): loc, pos = "Position 2: pi", 2
            if(center[0] > w/2 and center[1] > h/2): loc, pos = "Position 3: 3pi/4", 3
            cv2.putText(frame, loc, org = (0, 400), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color = (0, 0, 0))
            
            
            #writeNumber(pos)
                #print ("RPI: Hi Arduino, I sent you ", pos)

                #number = readNumber()
                #print ("Arduino: Hey RPI, I received ", number)

                #if prevPos != pos:  
                #    lcd.clear()
                #    lcd.message = "Sent: " + str(pos) + "\nGot:  " + str(number)
                #    prevPos = pos
                
            
            cv2.imshow('frame',frame)
            cv2.waitKey(0)
            
        except: pass
                
    #rvec, tvec,_ = aruco.estimatePoseSingleMarkers(corners, 0.05, camera_matrix, dist_co)

    # Status Handling
    if(not corners):status = "No marker found"
    else:status = "Found a marker!"
    cv2.putText(frame, status, org = (0, 300), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color = (0, 0, 0))
    frame = aruco.drawDetectedMarkers(frame, corners, ids)
    cv2.imshow('frame',frame)


    k = cv2.waitKey(1)
    if k == 27: break
    #print(h,w)
    
#print(frame)
cv2.imshow('frame',frame)

cv2.waitKey(0)
cv2.destroyAllWindows()   

cap.release()
cv2.destroyAllWindows()