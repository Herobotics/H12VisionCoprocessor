import cv2
import numpy as np
import grip
    
vc = cv2.VideoCapture(1)
imagePipeline = grip.GripPipeline()

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

#prosses image
while rval:
    
    cv2.imshow("image", frame)
    cv2.imshow("hull", imagePipeline.process(frame))
    
    #Get next image
    rval, frame = vc.read()

    #break on ESC
    key = cv2.waitKey(20)
    if key == 27:
        break
    
cv2.destroyWindow("image")
cv2.destroyWindow("color")
cv2.destroyWindow("hull")
