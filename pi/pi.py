import sys
sys.path.append(r"./color")
sys.path.append(r"./kind")
import cv2
import color.testColor,color.colorDictionary
import kind.getkind
a=kind.getkind.car_type("./img/6.jpg")
frame = cv2.imread('./img/6.jpg')
b=color.testColor.getColorOfFrame(frame)
print(a,b)
