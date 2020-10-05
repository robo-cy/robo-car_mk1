# robo-car_mk1
This is a simple project to learn about robotics and python3

So I've finally got my little robot to the point where I can drive it around remotely using the camera to see where I'm going. Now I can start working on the robotic arm.

The robot is based off of the Drogerdy 2.0 and has been redesigned to allow the use of much larger motors. Included in the redesign is a track tensioning mechanism to overcome the problem of the main drive cogs slipping inside the tracks due to increased torque.

The entire system is powered by a 20v De Walt battery pack. This was the cheapest way I could find to power everything since I already have quite a few of these batteries. I have several voltage converters on board since my system uses 4 different voltages (5v for the raspberry pi, 12v for the drive system, 3.3v for the LED lights, and 24v for the steppers to control the robotic arm).

All of the code is written in python 3 and while some of it initially was borrowed from forums and such, almost all of it is heavily modified, or rewritten altogether. 
