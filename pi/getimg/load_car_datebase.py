# -*- coding: utf-8 -*-
import os
import numpy as np
import cv2
IMAGE_SIZE = 64
# 按照指定图像大小调整尺寸
def resize_image(image, height=IMAGE_SIZE, width=IMAGE_SIZE):
    top, bottom, left, right = (0, 0, 0, 0)
    # 获取图像尺寸
    shape = image.shape
    h=shape[0]
    w=shape[1]
    # 对于长宽不相等的图片，找到最长的一边
    longest_edge = max(h, w)
    # 计算短边需要增加多上像素宽度使其与长边等长
    if h < longest_edge:
        dh = longest_edge - h
        top = dh // 2
        bottom = dh - top
    elif w < longest_edge:
        dw = longest_edge - w
        left = dw // 2
        right = dw - left
    else:
        pass
        # RGB颜色
    BLACK = [0, 0, 0]
    # 给图像增加边界，是图片长、宽等长，cv2.BORDER_CONSTANT指定边界颜色由value指定
    constant = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=BLACK)
    # 调整图像大小并返回
    return cv2.resize(constant, (height, width))
# 读取训练数据
images = []
labels = []
def read_path(path_name):
    for dir_item in os.listdir(path_name):
        # 从初始路径开始叠加，合并成可识别的操作路径
        full_path = os.path.abspath(os.path.join(path_name, dir_item))
        if os.path.isdir(full_path):  # 如果是文件夹，继续递归调用
            read_path(full_path)
        else:  # 文件
            if dir_item.endswith('.jpg'):
                print(full_path)
                image = cv2.imread(full_path)
                image = resize_image(image, IMAGE_SIZE, IMAGE_SIZE)
                # 放开这个代码，可以看到resize_image()函数的实际调用效果
                images.append(image)
                labels.append(os.path.dirname(full_path))
    print("labels:")
    print(labels)
    return images, labels
# 从指定路径读取训练数据
def load_dataset(path_name):
    images, labels = read_path(path_name)
    # 将输入的所有图片转成四维数组，尺寸为(图片数量*IMAGE_SIZE*IMAGE_SIZE*3)
    # 图片为64 * 64像素,一个像素3个颜色值(RGB)
    images = np.array(images)
    print(images.shape)
    # 标注数据，其他车辆全部指定为0
    labels = np.array([0 if label.endswith('non_vehicle') else 1 for label in labels])
    return images, labels
if __name__=='__main__':
    path_name=r"D:\DaChuangworkspace\capture"
    read_path(path_name)
