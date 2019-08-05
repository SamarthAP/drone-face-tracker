from djitellopy import Tello
import numpy as np 
import cv2

# speed of drone 
speed = 60

# init Tello
tello = Tello()

# Tello velocities
velocity_fb = 0
velocity_lr = 0
velocity_ud = 0
velocity_yaw = 0

# load cascade classifier 
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Tello setup
tello.connect()
tello.set_speed(speed)
tello.streamon()

# init object to read video frames from Tello
frame_read = tello.get_frame_read() 

running = True

# main loop
while running:

    if frame_read.stopped:
        break
    
    # frame = cv2.cvtColor(frame_read.frame, cv2.COLOR_BGR2RGB)
    frame = np.fliplr(frame_read.frame)

    faces = face_cascade.detectMultiScale(frame, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.circle(frame, (x + w//2 , y + h//2), 5, (0, 0, 255))

    cv2.imshow('Tello Video', frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        cv2.destroyAllWindows()
        break

tello.end()