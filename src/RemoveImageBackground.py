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


#Convert to and apply gray scale
gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
binary = cv2.bitwise_not(gray_scale)

#Get contours from gray scale
contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#Get rectangle coordinates from around contours
rect = (0,0,0,0)

areas = [cv2.contourArea(c) for c in contours]
max_index = np.argmax(areas)
contour = contours[max_index]

x,y,w,h = cv2.boundingRect(contour)

#If rectangle isn't properly drawn, use up to total size of image
if x==0:
    x+=img.shape[1]-1
if y==0:
    y+=img.shape[0]-1
rect = (x,y,x+w,y+h)


#Grab foreground from rectangle
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
cut_mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*cut_mask[:,:,np.newaxis]

#Output image
cv2.imwrite('../output/black_bkg.jpg', img)


