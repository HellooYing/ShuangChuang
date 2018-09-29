import cv2
import os
def SearchVehical(VideoPath):
    cap=cv2.VideoCapture(VideoPath)
    capture=r".\capture"
    classIdentify_car=".\cars.xml"
    classfier = cv2.CascadeClassifier(classIdentify_car)
    value,frame=cap.read()
    if not os.path.exists(capture):
        os.makedirs(capture)
    FrameCount=0
    while True:
        FrameCount =FrameCount+1
        value,frame=cap.read()
        if not value:
            break
        grey=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        carRects=classfier.detectMultiScale(grey,scaleFactor=1.2,minNeighbors=3,minSize=(64,64))
        i=0
        if len(carRects)>0:
            for carRect in carRects:  # 单独框出每一张车辆
                x, y, w, h = carRect
                i=i+1
                fragment = frame[x:x + w, y:y + h]
                #cv2.rectangle(frame, (x, y), (x + w, y + h),(0,255,0), 2)
                cv2.imwrite(r".\capture\Vehical{}_{}.jpg".format(FrameCount,i),fragment)
                print("成功捕捉   .\capture\Vehical{}_{}.jpg".format(FrameCount,i))
    return capture
if __name__=="__main__":
    SearchVehical(r"../video/test1.mp4")
