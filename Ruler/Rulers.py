# -*- coding: utf-8 -*-
import cv2
from Ruler import Get_ruler
from Ruler import Find_num,Find_num
import numpy as np
import math
from functools import reduce
import pdb
from Datastruct import Data_struct
import copy


def getRuler(ori_image,image):

    img_height, img_width = image.shape
    image_biaochi=copy.copy(image)
    
    enlarge = 20
    thre1=0.95
    Ruler=Data_struct.Ruler()


    topRuler_y,downRuler_y=Get_ruler.get_top_down_y(image)
    #leftRuler_x,rightRuler_x=Get_ruler.get_left_right_x(image)
    
    # pdb.set_trace()
    top_pointlist,top_pointlist_y=Get_ruler.get_top_Point(image,topRuler_y,thre1)
    
    # print(top_pointlist)
    up_diff=top_pointlist[len(top_pointlist)-1]-top_pointlist[0]
    
    for i in range(len(top_pointlist)):
        cv2.rectangle(image_biaochi,(top_pointlist[i]-10,top_pointlist_y[i]-10),(top_pointlist[i]+10,top_pointlist_y[i]+10),(50,40,10),3)
     
    #cv2.imwrite('img_biaochi.jpg', image_biaochi)
    result_v, result, up_num = Find_num.get_prop2(ori_image,image, topRuler_y, top_pointlist, topRuler_y[0], thre1)

# =============================================================================
#     if len(top_pointlist) == 2:     # 只有两个端点，那是最长的标尺
#         result_v, result, up_num = Find_num.get_prop2(ori_image,image, topRuler_y, top_pointlist, topRuler_y[0], thre1)
#     else:
#         result_v, result, up_num = Find_num.get_prop1(ori_image,image,top_pointlist_y, enlarge, top_pointlist)
#         #print('改后')
# =============================================================================
        #result_v, result, up_num = Find_num.get_prop1(image,top_pointlist_y, enlarge, top_pointlist)
    Ruler.proportion(result_v)
 
    Ruler.scale(result) 
    print("scale: ", end='')
    print(Ruler.out_scale())

    return Ruler,up_num,up_diff,image_biaochi
    #return topRuler, downRuler, leftRuler, rightRuler

def changeRuler(Ruler,up_diff,new_num):
    Ruler.proportion(up_diff/new_num) 
    Ruler.scale(new_num/up_diff) 
    print("new: ", end='')
    print(Ruler.out_scale())
    return Ruler
       
if __name__ == '__main__':
    filename = "E:/AIJIA/dataset/11.png"
    image=cv2.imread(filename,0) 
    # ret,image = cv2.threshold(image,thre,255,cv2.THRESH_BINARY)
    thre = yuzhi.find_binary(image)
    print("二值化阈值为: ", end='')
    print(thre)
    image = yuzhi.gray2binary(image.copy(),thre)
    RulerList = getRuler(filename, image)
    print(RulerList.data_dic['right_ruler'].out_proportion())