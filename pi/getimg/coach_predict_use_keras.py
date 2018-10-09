# -*- coding: utf-8 -*-
import cv2
from car_train_use_keras import Model
video_path= 'C:\\worksapce\\videoCapture\\111.mp4'
picture_path1= 'C:\\worksapce\\videoCapture\\object\\coach-predict-object\\car3.jpg'
picture_path2='C:\\worksapce\\videoCapture\\object\\coach-predict-object\\coach5.jpg'
path=[picture_path1,picture_path2]
def video_coach_predict(video_path):
    # 加载模型
    model = Model()
    model.load_model(file_path='./car'
                               '.model.h5')
    # 框住车辆的边框颜色
    color = (0, 255, 0)
    # 捕获指定摄像头的实时视频流
    cap = cv2.VideoCapture(video_path)
    # 人脸识别分类器本地存储路径
    cascade_path = "C:\\worksapce\\videoCapture\\cars.xml"
    # 循环检测识别客车
    while True:
        _, frame = cap.read()  # 读取一帧视频
        # 图像灰化，降低计算复杂度
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 使用车辆识别分类器，读入分类器
        cascade = cv2.CascadeClassifier(cascade_path)
        # 利用分类器识别出哪个区域为车辆
        carRects = cascade.detectMultiScale(frame_gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        if len(carRects) > 0:
            for carRect in carRects:
                x, y, w, h = carRect
                # 截取车辆图像提交给模型识别这是什么车
                image = frame[y - 10: y + h + 10, x - 10: x + w + 10]
                carID = model.car_predict(image)
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, thickness=2)
                # 如果是“car”
                if carID == 0:
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, thickness=2)
                    # 文字提示是什么车
                    cv2.putText(frame, 'car',
                                (x + 30, y + 30),  # 坐标
                                cv2.FONT_HERSHEY_SIMPLEX,  # 字体
                                1,  # 字号
                                (255, 0, 255),  # 颜色
                                1)  # 字的线宽
                else:

                    pass
        cv2.imshow("predict coach", frame)
        # 等待10毫秒看是否有按键输入
        k = cv2.waitKey(2)
        # 退出循环
        if k ==27 &0xFF:
            break
    # 释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows()
def picture_coach_predict(picture_path):
    model = Model()
    model.load_model(file_path='./car.model.h5')
    # 框住车辆的边框颜色
    # 用cv2中读取图片
    img = cv2.imread(picture_path)
    color=(0,255,0)
    # 车 辆 识别分类器本地存储路径
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cascade_path= "C:\\worksapce\\videoCapture\\cars.xml"
    cascade=cv2.CascadeClassifier(cascade_path)
    # 利用分类器识别出哪个区域为车辆
    carRects = cascade.detectMultiScale(img_gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
    if len(carRects) > 0:
        print("yes for xml")
        for carRect in carRects:
            x, y, w, h = carRect
            # 截取车辆图像提交给模型识别这是什么车
            image = img[y - 10: y + h + 10, x - 10: x + w + 10]
            cv2.rectangle(img, (x - 10, y - 10), (x + w + 10, y + h + 10), color, thickness=2)
            carID = model.car_predict(image)
            if carID == 0:
               print("yes for corret coach")
               cv2.rectangle(img, (x - 10, y - 10), (x + w + 10, y + h + 10), color, thickness=2)
               # 文字提示是什么车
               cv2.putText(img, 'coach',
                           (x + 30, y + 30),          # 坐标
                           cv2.FONT_HERSHEY_SIMPLEX,  # 字体
                           1,                         # 字号
                           (255, 0, 255),             # 颜色
                           2)                         # 字的线宽
            else:
                pass
    cv2.imshow('model',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def picture_dicture(picture_path):
    img=cv2.imread(picture_path)
    model=Model()
    model.load_model(file_path='./car.model.h5')
    carID=model.car_predict(img)
    if carID==0:
        print("{}:yes for coach".format(picture_path))
    else:
        print("{}:no for coach".format(picture_path))
if __name__ == '__main__':
    #picture_coach_predict(picture_path)
    #video_coach_predict(video_path)
    for picture_path in path:
        picture_dicture(picture_path)

