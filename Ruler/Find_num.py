# -*- coding: utf-8 -*-

import numpy as np
import cv2
#import pytesseract  
from PIL import Image 
from functools import reduce
import pdb
from aip import AipOcr  
import base64
from Settings import Settings

#from goto import with_goto

# 删除端点附近的垂直线，便于后面数字识别
def delete_vertical(img, height, i_index, j_index):
    add = 1
    while i_index-add >= 0 and i_index-add < height:
        if img[i_index-add, j_index] == 0:
            if img[i_index-add, j_index+1] == 0 and img[i_index-add, j_index-1] == 0:
                pass
            else:
                img[i_index-add, j_index] = 255
            add = add + 1
        else:
            break
    add = 0
    while i_index+add < height:
        if img[i_index+add, j_index] == 0:
            if img[i_index+add, j_index+1] == 0 and img[i_index+add, j_index-1] == 0:
                pass
            else:
                img[i_index+add, j_index] = 255
            add = add + 1
        else:
            break



def get_int(num):
    list1=['a','c','d','e','f','k','m','n','p','q','r','t','u','v','w','x','y','A','C','E','F','G','H','K','M','N','P','R','T','W','X','Y']
    num_list=['0','1','2','3','4','5','6','7','8','9']
    for i in range(len(num)):
        if (num[i]=='o'or num[i]=='O'or num[i]=='Q'or num[i]=='D'or num[i]=='U'or num[i]=='V'):
            if(i==0):
                num='0'+num[i+1:]
            else:
                num=num[0:i]+'0'+num[i+1:]
        elif (num[i]=='b'or num[i]=='h'):
            if(i==0):
                num='6'+num[i+1:]
            else:
                num=num[0:i]+'6'+num[i+1:]
        elif (num[i]=='z'or num[i]=='Z'):
            if(i==0):
                num='2'+num[i+1:]
            else:
                num=num[0:i]+'2'+num[i+1:]
        elif (num[i]=='B'or num[i]=='g'):
            if(i==0):
                num='8'+num[i+1:]
            else:
                num=num[0:i]+'8'+num[i+1:]
        elif (num[i]=='s'or num[i]=='S'):
            if(i==0):
                num='5'+num[i+1:]
            else:
                num=num[0:i]+'5'+num[i+1:]
        elif (num[i]=='l' or num[i]=='L' or num[i]=='i' or num[i]=='I' or num[i]=='j' or num[i]=='J'):
            if(i==0):
                num='1'+num[i+1:]
            else:
                num=num[0:i]+'1'+num[i+1:] 
        elif (num[i]==' '):
            if(i==0):
                num='1'+num[i+1:]
            else:
                num=num[0:i]+'1'+num[i+1:]
        elif(num[i] in list1):
            if(i==0):
                num='1'+num[i+1:]
            else:
                num=num[0:i]+'1'+num[i+1:] 
        elif(num[i] not in num_list):
            if(i==0):
                num='1'+num[i+1:]
            else:
                num=num[0:i]+'1'+num[i+1:] 
    
    if(len(num)==4 and num[0]=='1'):
        num='1'+ num        
    return int(num)
    
    
def get_file_content(filePath):      
    with open(filePath, 'rb') as fp: 
        return fp.read()     
    
def horizon_ruler(ori_img,img, index_l, start_y, height, is_top):
    #cv2.imwrite('E:/AIJIA/up_ruler.jpg', ori_img)
    count=0
    start=99999
    for i in range(index_l[0]+20,index_l[len(index_l)-1]-80):
        for j in range(3,start_y-3):
            if img[j][i]==0:
                start=i
                count=1
                break
        if(count==1):
            break
    if(start==99999):
        return 0
    ori_img = ori_img[:, start-20:start+80]
    #cv2.imwrite('E:/AIJIA/up_ruler.jpg', ori_img)
    cv2.imwrite('Ruler/up_ruler.jpg', ori_img)
    ori_img = get_file_content('Ruler/up_ruler.jpg')
    

 
    
    nums=[]
  

    #client = AipOcr(Settings.APP_ID, Settings.API_KEY, Settings.SECRET_KEY)  
    options = {}
    options["language_type"] = "ENG"
    options["detect_direction"] = "true"
    options["probability"] = "true"
    

    for i in range(0,len(Settings.APP_ID)):
        try:
            client = AipOcr(Settings.APP_ID[i], Settings.API_KEY[i], Settings.SECRET_KEY[i])
            res=client.basicAccurate(ori_img,options) 
            for item in res['words_result']:
                nums=item['words']
            if(len(nums)>0):
                nums=get_int(nums)
            else:
                nums=1
            return nums
            #break
        except:
            continue

# =============================================================================
#     #精确版
#     res=client.basicAccurate(ori_img,options) 
#     #通用版
#     #res=client.general(ori_img,options)  
#     for item in res['words_result']:
#         #print(item['words'])
#         nums=item['words']
#         
#     #nums=item['words']
#     if(len(nums)>0):
#         nums=get_int(nums)
#     else:
#         nums=1
#     return nums        
#         
# =============================================================================
    

    
    
    





        



def get_prop2(ori_image,image, topRuler_y, top_pointlist, top_startpoint_y, thre2):
    up_num=1
    img_height, img_width = image.shape
    #image[topRuler_y[0]-1,:]=255
    
    #image[topRuler_y[0],:]=255
    #image[topRuler_y[0]+1,:]=255

    # pdb.set_trace()
    width_0 = 0
    
    width_0 = 0
    width_1 = img_width
    height_0 = 0
    # 因为数字在中间的时候会把在中间的数字误识别为端点，所以依此来判断数字的位置进行截图
# =============================================================================
#     if len(top_pointlist) == 2:     # 数字在标尺上方
#         height_1 = topRuler_y[0] +3
#     else:   # 数字在标尺中间
#         height_1 = topRuler_y[0] + 85
# =============================================================================
    height_1 = topRuler_y[0] +3
    
    height = height_1 - height_0
    img_up = image[height_0:height_1, width_0:width_1]
    ori_img_up = ori_image[height_0:height_1, width_0:width_1]
    
    # pdb.set_trace()
    up_num_1=[]
    for i in range(len(top_pointlist)-1):
        new_list=[]
        new_list.append(top_pointlist[i])
        new_list.append(top_pointlist[i+1])
        up_num_1.append(horizon_ruler(ori_img_up,img_up, new_list, top_startpoint_y, height, True))
    if(len(up_num_1)>0):
        up_num=max(up_num_1)

    #up_num = horizon_ruler(ori_img_up,img_up, top_pointlist, top_startpoint_y, height, True)
    #up_num = 0
    # 可能出现把其他端点的竖线当作数字的情况，这里进行排除
    #if len(up_nums) == 0:
        #up_num=1
    #elif len(up_nums) > 1:
        #up_num = max(up_nums)
    #else:
        #up_num = up_nums[0]
    print("最上标尺数字: ", end='')
    print(up_num)
    len_diff = top_pointlist[-1] - top_pointlist[0]
    if(up_num==0):
        up_num=1
    if(len_diff==0):
        len_diff=1
    return len_diff/up_num, up_num/len_diff,up_num