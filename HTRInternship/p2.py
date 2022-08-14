import cv2
import pickle
import numpy as np

def checkParkSpace(img1):
    spaceCounter=0
    for pos in posList:
        x,y = pos
        img_crop=img1[y:y+height,x:x+width]
        count=cv2.countNonZero(img_crop)
        print("count",count)

        if count < 20:
            color=(0,255,0)
            spaceCounter +=1
        else:
            color=(0,0,255)

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, 2)
width=100
height=40

capture= cv2.VideoCapture("carPark.mp4")

with open("CarParkPos","rb") as f:
    posList = pickle.load(f)

while True:
    success,img=capture.read()

    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur=cv2.GaussianBlur(imgGray,(3,3),1)
    imgThreshold=cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    imgMedianBlur=cv2.medianBlur(imgThreshold,(5))
    imgDilate=cv2.dilate(imgMedianBlur,np.ones((3,3)),iterations=1)
    checkParkSpace(imgDilate)
    cv2.imshow("img",img)
    cv2.waitKey(25)