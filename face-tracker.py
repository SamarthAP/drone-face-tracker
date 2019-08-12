from djitellopy import Tello
import numpy as np 
import cv2

# speed of drone 
speed = 25

# init Tello
tello = Tello()

# Tello velocities
velocity_fb = 0    # forward/back
velocity_lr = 0    # left/right
velocity_ud = 0    # up/down
velocity_yaw = 0   # yaw

# load cascade classifier 
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Tello setup
tello.connect()
tello.set_speed(speed)
tello.streamon()
tello.takeoff()

# init object to read video frames from Tello
frame_read = tello.get_frame_read() 

# tello staying still or moving to find target
hold_position = False

running = True

# main loop
while running:

    key = cv2.waitKey(1)

    if key == ord('q'):
        cv2.destroyAllWindows()
        break

    if frame_read.stopped:
        break
    
    # frame = cv2.cvtColor(frame_read.frame, cv2.COLOR_BGR2RGB)
    frame = np.fliplr(frame_read.frame)
    frame_shape = frame.shape

    # need a dst object to add shapes/lines on top of the frame, and
    # cv2.cvtColor() returns a dst
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # detect faces
    faces = face_cascade.detectMultiScale(frame, 1.5, 2)

    # if no faces dont move 
    if len(faces) == 0:
        velocity_fb = 0
        velocity_lr = 0
        velocity_ud = 0
        velocity_yaw = 0

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2) # face outline rectaangle
        cv2.circle(frame, (x + w//2 , y + h//2), 5, (0, 0, 255)) # middle of face outline

        face_middle = (x + w // 2, y + h // 2) # middle of face coordinate
        frame_middle = (frame_shape[1] // 2, frame_shape[0] // 2) # middle of frame coordinate

        # want face to be around 200x200 pixels 
        # if face is larger, then both dimensions of z_axis_displacement 
        # are negative, so we can tell the drone to move backwards because it
        # is too close to the face
        z_axis_displacement = (200 - w, 200 - h)

        # displacement of face from middle of frame; yaw is 0; NOTE: using only width of face for z axis displacement
        displacement_vector = np.array([frame_middle[0] - face_middle[0], z_axis_displacement[0], frame_middle[1] - face_middle[1], 0])

        # threshold circle 
        cv2.circle(frame, (face_middle[0], face_middle[1]), 200, (255, 255, 255), 5)

        # vector line 
        cv2.line(frame, (x + w//2 , y + h//2), (x + w//2 + displacement_vector[0] , y + h//2 + displacement_vector[2]), (255, 255, 255), 2)

        if not abs(displacement_vector[0]) < 200:
            velocity_lr = speed * int(displacement_vector[0]/abs(displacement_vector[0]))
        else:
            velocity_lr = 0
        
        if not abs(displacement_vector[1]) < 40:
            velocity_fb = speed * int(displacement_vector[1]/abs(displacement_vector[1]))
        else:
            velocity_fb = 0

        if not abs(displacement_vector[2]) < 200:
            velocity_ud = speed * int(displacement_vector[2]/abs(displacement_vector[2]))
        else:
            velocity_ud = 0
        
        # break for loop because we only want to move to the first face detected
        break
    
    tello.send_rc_control(velocity_lr, velocity_fb, velocity_ud, velocity_yaw)

    # middle of frame 
    cv2.circle(frame, (frame.shape[1] // 2, frame.shape[0] // 2), 5, (0, 255, 0))
    cv2.imshow('Tello Video', frame)

tello.land()
tello.end()