import cv2
import glob
import numpy as np

#Find image
img_path = [glob.glob('../data/'+e) for e in ['*.jpg', '*.jpeg', '*.png']][0][0]

#Load image
img = cv2.imread(img_path)

#Create mask and models for foreground and background
mask = np.zeros(img.shape[:2], np.uint8)
bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

img_copy = img.copy()

#Convert to and apply gray scale
gray_scale = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
binary = cv2.bitwise_not(gray_scale)

#Get contours from gray scale
contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#Get rectangle coordinates from around contours
rect = (0,0,0,0)
for contour in contours:
    (x,y,w,h) = cv2.boundingRect(contour)
    rect = (x,y,w,h)
    cv2.rectangle(img_copy, (x,y), (x+w,y+h), (0,255,0), 2)

#Grab foreground from rectangle
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)+(mask==0),255,0).astype('uint8')
img = img*mask2[:,:,np.newaxis]

#Output image
cv2.imwrite('../output/black_bkg.jpg', img)


