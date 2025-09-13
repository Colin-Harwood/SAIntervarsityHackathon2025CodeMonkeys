# ear_detector
import numpy as np
import math
import time

# passed in 6 landmarks


# 1.calculate the Eye aspect ratio form the landMark.py module 
# 2.check whether the eyes are open by comparing the current EAR to the present threshold
# 3.count the number of consecutive frames that eyes have been open or closed for 
# 4. trigger drowsiness if eyes are closed for to many frames

    ## passed in an 2 arrays of 6 tuples (each eye is calculated individually return the ratio ##
def calculateEAR(leftEye, rightEye):
    if leftEye is None or rightEye is None:
        print("Error: Cant see eyes")
        return None
    
    leftPoint_1, leftPoint_2, leftPoint_3, leftPoint_4, leftPoint_5, leftPoint_6 = leftEye
    rightPoint_1, rightPoint_2, rightPoint_3, rightPoint_4, rightPoint_5, rightPoint_6 = rightEye


    leftVerticalDistance1 = math.dist(leftPoint_2, leftPoint_6)
    leftVerticalDistance2 = math.dist(leftPoint_3, leftPoint_5)
    leftHorizontalDistance = math.dist(leftPoint_1, leftPoint_4)

    LHS = ( leftVerticalDistance1 + leftVerticalDistance2) / (2 * leftHorizontalDistance)

    rightVerticalDistance1 = math.dist(rightPoint_2, rightPoint_6)
    rightVerticalDistance2 = math.dist(rightPoint_3, rightPoint_5)
    rightHorizontalDistance = math.dist(rightPoint_1, rightPoint_4)

    RHS = (abs(rightVerticalDistance1) + abs(rightVerticalDistance2)) / (2 * rightHorizontalDistance)

    return (LHS + RHS) / 2.0


def isDrowsy( avgEAR, drowsyTime = 1.0, threshHold = 0.15 ):
    if avgEAR is None :
        print("average is empty")
        return None
    
    global drowsy_start_time   ### GLOBAL counter

    if avgEAR < threshHold:
        # if first time dipping below threshold, start timer
        if drowsy_start_time is None:
            drowsy_start_time = time.time()
        
        # check how long it has stayed below
        elapsed = time.time() - drowsy_start_time
        if elapsed >= drowsyTime:
            return True
        else:
            return False
    else:
        # reset when eyes open again
        drowsy_start_time = None
        return False
        