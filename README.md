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

Next I set an arbitrary threshold such that if the drone's displacement was within said threshold, it wouldn't need to move. This is so that the drone doesn't constantly try to 'fix' it's position even if is just a few pixels off of the center of the face. Now we have all of the information needed, and all that was left to do was send movement commands to the drone, based on the vector and the threshold.

Note: I am currently using this interface for interacting with the drone: https://github.com/damiafuentes/DJITelloPy. However, I am writing my own interface for the drone and will be switching to it once it is ready: https://github.com/SamarthAP/TelloWrapper.