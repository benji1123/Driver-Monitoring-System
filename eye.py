
# Face Recognition

import cv2;         #openCV
import argparse;


# Arguments Stuffs .........................................
parser = argparse.ArgumentParser(description = 'python main.py [opaque][1]')
parser.add_argument("bgrnd",help="0 => clear bgrnd | 1=>opaque bgrnd", type=int)     # backcground type 
parser.add_argument("cam",help="0 for webcam | 1 for external cam", type=int)       # webcam to use
parser.add_argument("arduino",help="0 for no arduino | 1 for arduino", type=int)
args = parser.parse_args()


# arduino stuffs ........................................
import serial   
import time

# toggle arduino connection
if(args.arduino):
    PORT = "COM4"
    RATE = 9600
    arduino= serial.Serial('/dev/cu.usbmodem14411',9600, timeout = 0)
    # arduino outputs user's level of distraction in terms of steering-wheel sesors
    if (arduino.inWaiting()>0):
        wheel_score = arduino.readline().decode('ascii')


# Computer Vision ..........................................

eye_score = 0;
in_count = 0                                            # eye-motion counter (frame #)
origin_x, origin_y = None, None;                        # Origin Coordinate
size_confirm, width_box, height_box = 0, 100, 100       # Safety-Zone size attributes
safe_x, safe_y = 180,200;

# Loading Haar Classifiers 
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml'); #global referential
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml'); #face referential

# Detection Algorithm............
def detect(gray, frame):  

    global wheel_score, eye_score
    global width_box, height_box, size_confirm, safe_x, safe_y;


    # ..DEFINE DANGER-ZONE..
    cv2.rectangle(frame, (safe_x, safe_y), (safe_x+width_box, safe_y+height_box), (255, 0, 0), 4); 

    # set size of safe-
    if(size_confirm == 0):
        while(True):

            # alter size of box
            if(cv2.waitKey(3) & 0xFF == ord('s')):
                height_box += 5;
                break;
            elif(cv2.waitKey(3) & 0xFF == ord('w')):
                height_box -= 5;
                break;
            elif(cv2.waitKey(3) & 0xFF == ord('d')):
                width_box -= 5;
                break;
            elif(cv2.waitKey(3) & 0xFF == ord('a')):
                width_box += 5;
                break;

            # altering position of box
            elif(cv2.waitKey(3) & 0xFF == ord('k')):
                safe_y += 5;
                break;
            elif(cv2.waitKey(3) & 0xFF == ord('i')):
                safe_y -= 5;
                break;
            elif(cv2.waitKey(3) & 0xFF == ord('l')):
                safe_x -= 5;
                break;
            elif(cv2.waitKey(3) & 0xFF == ord('j')):
                safe_x += 5;
                break;

            # set configuration
            elif(cv2.waitKey(3) & 0xFF == ord('b')):
                pos_confirm = 1;
                break;
            break;

            
    global args;

    # Detect face & get bound-coordinates 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5); #got {x,y,w,h}
    
    # set background UPAQUE
    if(args.bgrnd==1):
        cv2.rectangle(frame, (0, 0), (1000, 1000), (0, 0, 0), 10000); 
    
    
    # Draw Face-Bounds on Frame

    for(face_x,face_y, _w, _h) in faces: 

        #enclose face in rect
        cv2.rectangle(frame,(face_x,face_y),(face_x + _w + 25, face_y + _h + 25), (255,105,180), 5); 
        roi_gray = gray[face_y : face_y + _h, face_x : face_x + int(_w/2)];
        roi_color = frame[face_y:face_y + _h, face_x:face_x + _w]; #store face-coordinates (color)

        # Draw Line down Origin
        #if(not(origin_x == None)):
            #cv2.line(frame,(origin_x, 0), (origin_x, 800), (255, 255, 255), 3)
        

        # Detect Eyes & get bound-coordinates 
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3);


        #SET ORIGIN POSITION of EyE
        global origin_x, origin_y, in_count;

        if(origin_x == None):

            for(eye_x, eye_y, ew, eh) in eyes[:1]:
                
                # Draw eye-enclosure
                cv2.rectangle(roi_color, (eye_x, eye_y), (eye_x +ew, eye_y + eh), (0, 255, 0), 3) 
            
                # Draw midpoint of Eye-ROI
                mex, mey = int(eye_x + ew/2), int(eye_y + eh/2);
                cv2.circle(roi_color,(mex,mey),3,(0,255,0),5)

                # set Origin @ present coordinate
                if(cv2.waitKey(1) & 0xFF == ord('s')):
                    origin_x, origin_y = mex+face_x, mey
                    print ("\n\nOrigin Position: ", origin_x," , ",origin_y, "\n")
                    break;
                    

        # Measure DISPLACEMENT from ORIGIN
        if(not(origin_x==None)):

            for(eye_x,eye_y,ew,eh) in eyes[:1]:     # track RIGHT eye only 
            
            # Draw EyeBox
                
                mex, mey = int(eye_x+ew/2), int(eye_y + eh/2);           # Compute MIDPOINT of Eye
                b,g,r = 0,255,0

                # EYE IS IN DISTRACTED ZONE
                if(mex < safe_x-face_x or mex > safe_x-face_x +width_box or mey < safe_y-face_y or mey > safe_y-face_y+height_box):
                    b,g,r = 0,0,255

                cv2.circle(roi_color,(mex,mey),3,(b,g,r),3)              #draw eye-center

                cv2.rectangle(roi_color, (eye_x, eye_y), 
                             (eye_x+ew, eye_y+eh), (b,g,r), 3)           # Draw outer eyes-bound 
                in_count+=1;
    return frame;




# Implementing Continuous Detection with Webcam..........................

video_capture = cv2.VideoCapture(args.cam);    #"0" => object of live webcam video
while True:

    
    # process (detection) frame 
    _, frame = video_capture.read();   
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY); # cascade operates on grayscale
    canvas = detect(gray,frame); 


    # un-invert camera-feed
    canvas = cv2.flip(canvas, 1)


    # resizing webcam window
    cv2.namedWindow('Press Q to Quit',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Press Q to Quit',800,620)
    cv2.imshow('Press Q to Quit',canvas);
    
    if cv2.waitKey(1) & 0xFF == ord('q'):   #quit on "q" press
        break;


# Quit Webcam & Close Elements
video_capture.release()
cv2.destroyAllWindows()     