import os
import glob
import cv2
from Similar import pHash,hammingDist
from car_train_use_keras import Model
def DelRePic():
    model=Model()
    model.load_model(file_path=r'./vehicle.model.h5')
    piclist=glob.glob(r".\capture\*.jpg")
    pHashDict={}
    DelPicList=[]
    for pic_index in piclist:
        pHashDict[pic_index]=pHash(pic_index)
    index=0
    while True:
        if index>=len(pHashDict):
            break
        indexx=0
        while True:
            indexx=indexx+1
            if indexx>=len(pHashDict):
                break
            if index==indexx:
                continue
            try:
                Dist=hammingDist(pHashDict[piclist[index]],pHashDict[piclist[indexx]])
            except IndexError:
                pass
            if Dist<=20:
                pHashDict.pop(piclist[indexx])
                print("remove "+piclist[indexx])
                os.remove(piclist[indexx])
                piclist.pop(indexx)
        index=index+1
    for pic in piclist:
        img=cv2.imread(pic)
        carID = model.car_predict(img)
        if carID==0:  #识别出非车辆
            os.remove(pic)
            print("remove"+pic)
if __name__=="__main__":
    DelRePic()