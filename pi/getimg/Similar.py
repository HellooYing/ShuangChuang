import cv2
import numpy as np
import sys
def pHash(imgfile):
    """get image pHash value"""
    #加载并调整图片为32x32灰度图片
    img=cv2.imread(imgfile, 0)
    #print(img.shape)
    if img is not None:
        img=cv2.resize(img,(64,64),interpolation=cv2.INTER_CUBIC)
                    #创建二维列表
        h, w = img.shape[:2]
        vis0 = np.zeros((h,w), np.float32)
        vis0[:h,:w] = img       #填充数据

    #二维Dct变换
        vis1 = cv2.dct(cv2.dct(vis0))
    #cv.SaveImage('a.jpg',cv.fromarray(vis0)) #保存图片
        vis1.resize(16,16)

    #把二维list变成一维list
        img_list=vis1.flatten()

    #计算均值
        avg = sum(img_list)*1./len(img_list)
        avg_list = ['0' if i<avg else '1' for i in img_list]
    #return avg_list
    #得到哈希值转换成16进制
        return ''.join(['%x' % int(''.join(avg_list[x:x+4]),2) for x in range(0,16*16,4)])
    else:
            print("image not loaded")
def cmpHash(hash1,hash2):
    n=0
    #hash长度不同则返回-1代表传参出错
    if len(hash1)!=len(hash2):
        return -1
    #遍历判断
    for i in range(len(hash1)):
        #不相等则n计数+1，n最终为相似度
        if hash1[i]!=hash2[i]:
            n=n+1
    return n
def hammingDist(s1, s2):
    """
    这等同于”汉明距离”(Hamming distance,在信息论中，
    两个等长字符串之间的汉明距离是两个字符串对应位置的不同字符的个数)。
    如果不相同的数据位数不超过5，就说明两张图像很相似；
    如果大于10，就说明这是两张不同的图像。
    :param s1:
    :param s2:
    :return:
    """
    # assert len(s1) == len(s2)
    # return sum([ch1 != ch2 for ch1, ch2 in zip(s1, s2)])
    try:
        assert len(s1) == len(s2)
    except TypeError:
        return 0
    else:
        return sum([ch1 != ch2 for ch1, ch2 in zip(s1, s2)])

def similar_path(img1,img2):
    Hashlist2=pHash(img1)
    Hashlist1=pHash(img2)
    #print(Hashlist1)
    #print(Hashlist2)
    #similar=cmpHash(Hashlist1,Hashlist2)
    #print(similar)
    out_score = 1 - hammingDist(Hashlist1, Hashlist2) * 1. / (32 * 32 / 4)
    return out_score
def similar(Hashlist1,Hashlist2):
    out_score = 1 - hammingDist(Hashlist1, Hashlist2) * 1. / (32 * 32 / 4)
    return out_score