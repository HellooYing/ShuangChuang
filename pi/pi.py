import sys
sys.path.append(r"./color")
sys.path.append(r"./kind")
import cv2
import color.testColor,color.colorDictionary
import kind.getkind
# a=kind.getkind.car_type("./kind/data/car_photos/jc/jc1.jpg")
# print(a)
frame = cv2.imread('./kind/data/car_photos/jc/jc1.jpg') #filename
print(frame)
# print(color.testColor.getColorOfFrame(frame))
# 假设现在已经有了图片
