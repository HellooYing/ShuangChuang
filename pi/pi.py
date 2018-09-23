import sys
sys.path.append(r"./color")
sys.path.append(r"./kind")
import cv2
import color.testColor,color.colorDictionary
import kind.getkind
a=kind.getkind.car_type("./img/2.png")
print(a)
frame = cv2.imread('./img/2.png') #filename
print(color.testColor.getColorOfFrame(frame))
