import mediapipe as mp
import cv2

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, #one face
    refine_landmarks=True, #using irises
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

def get_landmarks(frame):
    #get the shape: width, height, type(3)
    h, w, _ = frame.shape
    #cv2 takes the format from BGR to RGB as face_mesh expects RGB format
    results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if not results.multi_face_landmarks:
        return None
    
    lm = results.multi_face_landmarks[0].landmark  #get landmarks for the first face(0) 

    landmarks_pixels = []
    for l in lm:
        #landmark_pixels is a list of all 468 landmarks(positions on face)
        landmarks_pixels.append((int(l.x*w), int(l.y*h))) #landmarks give as a proportion so 0->1. normalise to fit according to height and width of screen

    LEFT_EYE = [33, 160, 158, 133, 153, 144] #only 6 of these positions are relevant to the left eye
    RIGHT_EYE = [263, 387, 385, 362, 380, 373] #only 6 relevant to right eye

    left_eye = [landmarks_pixels[i] for i in LEFT_EYE]
    right_eye = [landmarks_pixels[i] for i in RIGHT_EYE]

    #being returned as ([lefteye], [righteye])
    return (left_eye, right_eye)