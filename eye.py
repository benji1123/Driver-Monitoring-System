
# Face Recognition

import cv2;         #openCV
import argparse;


# Arguments Stuffs .........................................
parser = argparse.ArgumentParser(description = 'python main.py [opaque][1]')
parser.add_argument("bgrnd",help="0=>clear bgrnd, 1=>opaque bgrnd",type=int)
args = parser.parse_args()



in_count = 0                                # eye-motion counter (frame #)
origin_x, origin_y = None, None;            # Origin Coordinate


# Computer Vision ..........................................
# Loading Haar Classifiers 
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml'); #global referential
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml'); #face referential




# Detecting Face - Eyes
def detect(gray, frame):  

    cv2.rectangle(frame,(0,0),(0,5),(255,0,0),5);


    global args;
    # Detect face & get bound-coordinates 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5); #got {x,y,w,h}
    
    if(args.bgrnd==1):
        cv2.rectangle(frame, (0, 0), (1000, 1000), (255, 105, 180), 10000); 
    
    
    # Draw Face-Bounds on Frame

    for(face_x,face_y, _w, _h) in faces: 

        #enclose face in rect
        cv2.rectangle(frame,(face_x,face_y),(face_x + _w + 25, face_y + _h + 25), (255,105,180), 5); 
        roi_gray = gray[face_y : face_y + _h, face_x : face_x + int(_w/2)];
        roi_color = frame[face_y:face_y + _h, face_x:face_x + _w]; #store face-coordinates (color)

        # Draw Line down Origin
        if(not(origin_x == None)):
            cv2.line(frame,(origin_x, 0), (origin_x, 800), (255, 255, 255), 3)
        

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

            for(eye_x,eye_y,ew,eh) in eyes[:1]:
            
            # Draw Origin for Visual Refernece 
                cv2.rectangle(roi_color, (eye_x, eye_y), 
                             (eye_x+ew, eye_y+eh), (0, 255, 0), 3)      # Draw outer eyes-bound 
                mex, mey = int(eye_x+ew/2), int(eye_y + eh/2);           # Compute MIDPOINT of Eye
                cv2.circle(roi_color,(mex,mey),3,(0,0,255),3)     # Draw Midpoint


                # INTERFACE with SERVOMOTOR

                if(in_count % 5 == 0):       
                    
                    # move L 
                    if(mex > origin_x - face_x):
                        print("\nmoving left\nmex-:  ",mex,
                            "\origin_x: ",origin_x)
                    
                    # move R 
                    elif(mex < origin_x - 0):
                        print("\nmoving right\nmex:  ", mex,
                            "\origin_x: ",origin_x)
                
                in_count+=1;
    
    return frame;




# Implementing Continuous Detection with Webcam..........................

video_capture = cv2.VideoCapture(0);    #"0" => object of live webcam video
while True:

    
    # sending latest frame from cam => detect()
    _, frame = video_capture.read();   
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY); #cascade operates on grayscale
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