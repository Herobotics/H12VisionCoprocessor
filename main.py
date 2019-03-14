import threading
from networktables import NetworkTables

import cv2
import numpy as np

import ballPipeLine
import retroPipeLine

cond = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

NetworkTables.initialize(server='10.25.00.2')
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

with cond:
    print("Waiting")
    if not notified[0]:
        cond.wait()


# Insert your processing code here
print("Connected!")


# ballTarget - The ball that we want to go to if we want to get balls
#   x - Center of the ball on the X plane
#   y - Center of the ball on the Y plane
#   radius - Radius of the ball
# retroTarget - The pair of retro reflective tape that we want to go to
#   x - Center of the target on the X plane
#   y - Center of the target on the Y plane
#   angle - Angle that the target is at. Average from the botom to right and left to top slope
#   height - height from the bottom to the top of the target
# cameraIndex - Index of what camera to show. 0 - No camera, 1 - camera 1, 2 - camera 2, 3 - camera 1,2
# cameraStream - Cammer video that is being outputed by the pi

def getBallTargets(camera):
    cameraConnected, frame = camera.read()
    if not cameraConnected:
        return []
    return ballPipeLine.process(frame)

def getRetroTargets(camera):
    cameraConnected, frame = camera.read()
    if not cameraConnected:
        return []
    return retroPipeLine.process(frame)

frountCamera = cv2.VideoCapture(0)
backCamera = cv2.VideoCapture(1)

while True:
    putValue('ballTarget',getBallTargets(frountCamera))
    putValue('retroTarget',getRetroTargets(frountCamera))  
