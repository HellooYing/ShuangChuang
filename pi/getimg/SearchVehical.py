from pipeline import search_car
import cv2
import os
def SaveVehical(VideoPath=r'../video/test.mp4'):
    #读取视频
    cap=cv2.VideoCapture(VideoPath)
    frameCount=0
    while True:
        frameCount=frameCount+1
        ret,frame =cap.read()
        if not ret:
            break
        #return 窗口，和车辆存储路径
        CapturePath =search_car(frame,frameCount)
    return CapturePath

if __name__=="__main__":
    SaveVehical()