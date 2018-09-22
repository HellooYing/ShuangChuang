import numpy as np
import collections

def colorDictionary():
    
    dist = collections.defaultdict(list)

    #黑色
    black_lower = np.array([0, 0, 0])
    black_upper = np.array([180, 255, 46])
    colorList = []
    colorList.append(black_lower)
    colorList.append(black_upper)
    dist['black'] = colorList
    #灰色
    gray_lower = np.array([0, 0, 46])
    gray_upper = np.array([180, 43, 220])
    colorList = []
    colorList.append(gray_lower)
    colorList.append(gray_upper)
    dist['gray'] = colorList
    #白色
    white_lower = np.array([0, 0, 221])
    white_upper = np.array([180, 30, 255])
    colorList = []
    colorList.append(white_lower)
    colorList.append(white_upper)
    dist['white'] = colorList
    #红色1
    red_lower = np.array([0, 43, 46])
    red_upper = np.array([10, 255, 255])
    colorList = []
    colorList.append(red_lower)
    colorList.append(red_upper)
    dist['red'] = colorList
    #红色2
    red_lower = np.array([156, 43, 46])
    red_upper = np.array([180, 255, 255])
    colorList = []
    colorList.append(red_lower)
    colorList.append(red_upper)
    dist['red'] = colorList
    #橙色
    orange_lower = np.array([11, 43, 46])
    orange_upper = np.array([25, 255, 255])
    colorList = []
    colorList.append(orange_lower)
    colorList.append(orange_upper)
    dist['orange'] = colorList
    #黄色
    yellow_lower = np.array([26, 43, 46])
    yellow_upper = np.array([34, 255, 255])
    colorList = []
    colorList.append(yellow_lower)
    colorList.append(yellow_upper)
    dist['yellow'] = colorList
    #绿色
    green_lower = np.array([35, 43, 46])
    green_upper = np.array([77, 255, 255])
    colorList = []
    colorList.append(green_lower)
    colorList.append(green_upper)
    dist['green'] = colorList
    #青色
    navy_lower = np.array([78, 43, 46])
    navy_upper = np.array([99, 255, 255])
    colorList = []
    colorList.append(navy_lower)
    colorList.append(navy_upper)
    dist['navy'] = colorList
    #蓝色
    blue_lower = np.array([100, 43, 46])
    blue_upper = np.array([124, 255, 255])
    colorList = []
    colorList.append(blue_lower)
    colorList.append(blue_upper)
    dist['blue'] = colorList
    #紫色
    purple_lower = np.array([125, 43, 46])
    purple_upper = np.array([155, 255, 255])
    colorList = []
    colorList.append(purple_lower)
    colorList.append(purple_upper)
    dist['purple'] = colorList

    return dist
