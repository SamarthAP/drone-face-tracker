# drone-face-tracker
Facial Recognition + DJI Tello Drone

### Demo
Here is a little video of the drone in action, it follows people around using facial recognition! https://youtu.be/djg_Msd-Yks

### How it works 
Essentially there are two parts to this project:
1. Connecting to the drone and sending commands to it
2. Performing facial recognition and calculating where the drone needs to go

#### Part 1:
Connecting to the drone is pretty simple. The drone transmits its own wifi, so you can just connect to that, and communicate with the drone through a UDP websocket and multithreading. I created a python interface for this part and got the drone moving with my laptop's keyboard, however I wasn't able to solve the problem of receiving the video data from the drone in time. I was too eager to get the drone up and running, so instead I used [this](https://github.com/damiafuentes/DJITelloPy) interface I found on GitHub. Now that we had access to the drone's video, we can finally perform some calculations!

#### Part 2:
I took the video frames from the drone and used OpenCV, numpy and a Haar Cascade classifier for facial recognition. A face is recognized and bound by a rectangle. We are given the top-left corner of the rectangle, and its width and height. With that I found the middle of the face, and calculated the 2D vector from the middle of the video frame to the middle of the face. 

We basically want the drone to move so it's centered on a face, so the the middle of the frame has to be around the middle of the face. The 2D vector can help in moving the drone up, down, left and right, but not in a third dimension (forward/backward). To find the third dimension, I used the size of the face and compared it with an arbitrary face size. For example, let's say a 'normal' face size is 150x150 pixels. If the current face found is larger than 150x150, we know that the drone is too close, and vice versa. So with all of that we get a 3D vector representing the displacement of the drone. 

Next I set an arbitrary threshold such that if the drone's displacement was within said threshold, it wouldn't need to move. This is so that the drone doesn't constantly try to 'fix' it's position even if is just a few pixels off of the center of the face. Now we have all of the information needed, all that's left to do is to send movement commands to the drone, based on the vector and the threshold.

### Possible Improvements
- Use a combination of yaw and left/right movement to handle a left/right displacement of the face. Currently yaw is not used, only left/right movement is.
- Use the magnitude of the 3D displacement vector to determine the speed at which the drone should move. If the drone is very far from the face, it could move at a higher speed, and if the drone is closer, a slower speed. Currently, the drone moves at a constant speed.

### Limiting Factors
- Framerate is a big one. We want to make the displacement vector to be as accurate and as recent as possible. A lower framerate would mean that if the person moves abruptly between two frames, the most recent displacement vector would be 'outdated' and wouldn't represent the right direction that the drone needs to move.
- Drone response time is a huge factor as well. The DJI Tello doesn't move instantly when a command is sent, there is a tiny delay, which could be caused by many factors. However, this limits the drone from moving accurately, because there could be instances where the drone is moving in a direction and needs to suddenly change directions, but the delay means the drone can't reflect the updated information in its movement. Also, the DJI Tello can't handle consecutive commands well. Sometimes, if two commands are sent back-to-back, the second command will not register. Again, this adds to the problem of not having the most recent information.

Note: I am currently using this interface for interacting with the drone: https://github.com/damiafuentes/DJITelloPy. However, I am writing my own interface for the drone and will be switching to it once it is ready: https://github.com/SamarthAP/TelloWrapper.