import cv2
from camera import check_camera, get_camFrameData
from landmarks import get_landmarks
from eyeboxes import drawBoxes
def main():
#////////////////////////////////////////////////////////////////////////////////
# Opening and showing the camera
#////////////////////////////////////////////////////////////////////////////////
    camera = check_camera()
    CamReadingInProgress = True
    while (CamReadingInProgress == True):
        arrFrames = get_camFrameData(camera)
        if arrFrames is not None:
            cv2.imshow('Live CAM', arrFrames)
            # IF 'c' is pressed the cam will stop reading
            if cv2.waitKey(1) & 0xFF == ord('c'):
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