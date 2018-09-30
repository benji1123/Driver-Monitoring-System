
''' 
McMaster University | EcoCar4 ADAS Challenge | Sept - Oct 2018  
    
    [1]      Patrick Pan         TRON        Background Research, Presentation, Advisor  
    [2]      Jarvis Wang         CE          Arduino Steering Wheel Module, PySerial Interfacing
    [3]      Ben Li              CE          Computer Vision Program (this)
'''


import cv2;         
import argparse;

# Arguments Stuffs .............................................................................................

parser = argparse.ArgumentParser(description = 'python main.py [opaque][1]')
parser.add_argument("bgrnd",help="0 => clear bgrnd | 1=>opaque bgrnd", type=int)     # backcground type 
parser.add_argument("cam",help="0 for webcam | 1 for external cam", type=int)       # webcam to use
parser.add_argument("arduino",help="0 for no arduino | 1 for arduino", type=int)
args = parser.parse_args()


# arduino stuffs .............................................................................................

import serial   
import time

# toggle arduino connection
if(args.arduino == 1):
    arduino= serial.Serial('COM4', 9600, timeout = 0)


# Computer Vision .............................................................................................

in_count = 0                                            # count the frame-#
size_confirm, width_box, height_box = 0, 80, 80       # Safety-Zone size attributes
safe_x, safe_y = 180,200;

# Loading Haar-Cascades 
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml'); #global referential
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml'); #face referential

# Setting the Safe-Zone
def setSafeZone():
    global size_confirm, height_box, width_box, safe_y, safe_x
    while(True):
        # altering size of box
        c1 = cv2.waitKey(3)
        if(c1 & 0xFF == ord('s')):
            height_box += 5; break
        elif(c1 & 0xFF == ord('w')):
            height_box -= 5; break
        elif(c1 & 0xFF == ord('d')):
            width_box -= 5; break
        elif(c1 & 0xFF == ord('a')):
            width_box += 5; break
        # altering position of box
        elif(c1 & 0xFF == ord('k')):
            safe_y += 5;    break
        elif(c1 & 0xFF == ord('i')):
            safe_y -= 5;    break
        elif(c1 & 0xFF == ord('l')):
            safe_x -= 5;    break
        elif(c1 & 0xFF == ord('j')):
            safe_x += 5;    break
        # set curr. configuration (this function will no longer be called)
        elif(c1 & 0xFF == ord('b')):
            size_confirm = 1; break
        break

# Running the Detection Algorithm
def detect(gray, frame):  
    global wheel_score, args, width_box, height_box, size_confirm, safe_x, safe_y, in_count
    wheel_score = None

    cv2.rectangle(frame, (safe_x, safe_y), (safe_x+width_box, safe_y+height_box), (255, 0, 0), 4);  # draw safe-zone on frame

    # configure background
    if(args.bgrnd==1):
        cv2.rectangle(frame, (0, 0), (1000, 1000), (0, 0, 0), 10000); 
        
    # recieve data from steering-wheel
    if (args.arduino == 1 and arduino.inWaiting()>0):
        wheel_score = arduino.readline().decode('ascii')

    # DEFINE SAFE-ZONE
    if(size_confirm == 0):
        setSafeZone()

    # Detect Face Position
    faces = face_cascade.detectMultiScale(gray, 1.3, 5); 
    for(face_x, face_y, _w, _h) in faces: 
        
        #enclose face in rect
        cv2.rectangle(frame,(face_x,face_y),(face_x + _w + 25, face_y + _h + 25), (255,105,180), 5); 
        roi_gray = gray[face_y : face_y + _h, face_x : face_x + int(_w/2)];
        roi_color = frame[face_y:face_y + _h, face_x:face_x + _w];              #storing face-position data for future processing
        
        #Detect Right-Eye
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3);
        for(eye_x,eye_y,ew,eh) in eyes[:1]:    
            
            # Initialize Eye Positional Data
            mex, mey = int(eye_x+ew/2), int(eye_y + eh/2);  # midpoint     
            distracted = 0;                                 # state of distraction : 0 by default
            b,g,r = 0,255,0                                 # color-code : RED-Distracted | GREEN-Safe

            # Define Areas where User is considered Distracted
            c1 = mex<safe_x-face_x      
            c2 = mex>safe_x-face_x+width_box
            c3 = mey<safe_y-face_y 
            c4 = mey>safe_y-face_y+height_box    

            # Detect if User is Distracted
            if(c1 or c2  or c3  or c4):
                distracted = 1
                print("eyes: distracted | wheel-score: ", wheel_score)
                b,g,r = 0,0,255
            else:
                print("eyes: OKAY | wheel-score: ", wheel_score)

            # Draw Rect around the detected Eye on Frame
            cv2.circle(roi_color,(mex,mey),3,(b,g,r),3)              
            cv2.rectangle(roi_color, (eye_x, eye_y), (eye_x+ew, eye_y+eh), (b,g,r), 3)           

            # # Tell Arduino the User's Distracted-State
            # if(args.arduino == 1):
            #     in_count+=1
    return frame;


# Implementing Continuous Detection .............................................................................................

video_capture = cv2.VideoCapture(args.cam);    #"0" => object of live webcam video

while True:

    # process (detection) frame 
    _, frame = video_capture.read()   
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # cascade operates on grayscale
    canvas = detect(gray,frame) 

    # un-invert camera-feed
    canvas = cv2.flip(canvas, 1)

    # resizing webcam window
    cv2.namedWindow('Press Q to Quit',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Press Q to Quit',800,620)
    cv2.imshow('Press Q to Quit',canvas)
    
    # Program Exit Sequence
    if cv2.waitKey(1) & 0xFF == ord('q'):   
        break

video_capture.release()
cv2.destroyAllWindows()     