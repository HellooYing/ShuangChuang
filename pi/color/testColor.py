import cv2
import numpy as np
import colorDictionary

def getColorOfFrame(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    maxsum = -100
    color = None
    color_dict = colorDictionary.colorDictionary()
    for d in color_dict:
        #color_dict[d][0] -- lower color; color_dict[d][1] -- upper color.
        mask = cv2.inRange(hsv,color_dict[d][0],color_dict[d][1])  #利用函数设阈值，去除背景部分，选定区域为白，其他为黑
        #cv2.inRange(img,lowerColor,upperColor)取lowerColor和upperColor范围内的颜色
        #cv2.threshold()和cv2.inRange()在此处意义相同？作用均为将图像二值化
        #binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]#二值化
        binary = cv2.erode(mask, None, iterations = 2)#腐蚀,将图像的边缘腐蚀掉。作用就是将目标的边缘的“毛刺”踢除掉
        binary = cv2.dilate(binary, None, iterations = 2)#膨胀，将图像的边缘扩大些。作用就是将目标的边缘或者是内部的坑填掉。（去除噪点）
        #使用相同次数的腐蚀与膨胀，可以使目标表面更平滑！！
        img, cnts, hiera = cv2.findContours(binary.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#检查轮廓
        sum = 0
        for c in cnts:
            sum += cv2.contourArea(c)
        if sum > maxsum :
            maxsum = sum
            color = d
    return color
    
if __name__ == '__main__':
    frame = cv2.imread('timg.jpg') #filename
    print(getColorOfFrame(frame))

