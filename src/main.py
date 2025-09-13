import cv2
from camera import check_camera, get_camFrameData
from landmarks import get_landmarks
from eyeboxes import drawBoxes
from ear_detector import calculateEAR, isDrowsy
def main():
#////////////////////////////////////////////////////////////////////////////////
# Opening and showing the camera
#////////////////////////////////////////////////////////////////////////////////
    camera = check_camera()
    CamReadingInProgress = True
    while (CamReadingInProgress == True):
        arrFrames = get_camFrameData(camera)
        if arrFrames is not None:
            landmarks = get_landmarks(arrFrames)
            if landmarks == None:
                continue
            avgEAR = calculateEAR(landmarks[0], landmarks[1])
            eyesClosed = isDrowsy(avgEAR, 5)
            if eyesClosed:
                arrFrames = drawBoxes(arrFrames, landmarks, eyesClosed)
            else:
                arrFrames = drawBoxes(arrFrames, landmarks, eyesClosed)
            cv2.imshow('Live CAM', arrFrames)
            # IF 'c' is pressed the cam will stop reading
            if cv2.waitKey(1) & 0xFF == ord('c') or cv2.getWindowProperty('Live CAM', cv2.WND_PROP_VISIBLE) < 1:
                CamReadingInProgress = False
        
        else:
            print("Error: Cant read the frame")
            CamReadingInProgress = False
            break
            


    #Close the cam window
    camera.release()
    cv2.destroyAllWindows()
#////////////////////////////////////////////////////////////////////////////////
if __name__ == "__main__":
    main()