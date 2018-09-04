# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 15:34:47 2018


"""



import cv2 as cv
import numpy as np
from skimage import measure,color
import copy
from Datastruct import Data_struct
from Wall import Get_owner_wall
from Settings import Settings
from Door import Get_door
'''
min_hudu_area  封闭扇形面积的下界
max_hudu_area  封闭扇形面积的上界
min_zonghengbi 封闭扇形纵横比（y方向长度:x方向长度）下界
max_zonghengbi 封闭扇形纵横比（y方向长度:x方向长度）上界
'''


'''
min_xiju_area  细矩形面积的下界
max_xiju_area  细矩形面积的上界
min_zonghengbi 细矩形纵横比（短长度:长长度）下界
max_zonghengbi 细矩形纵横比（短长度:长长度）上界
max_len        细矩形长长度的上界(实际数值 1m)
'''
#x1,x2,y1,y2是底座的坐标，derectoin是底座水平0/竖直1
def Is_beside_wall(x1,y1,x2,y2,derection,Wall_img):
    if derection==1:
        for i in range(min(x1,x2),min(x1,x2)-140,-1):
            if (Wall_img[y1][i]==0):
                return 1
        for i in range(max(x1,x2),max(x1,x2)+140):
            if (Wall_img[y1][i]==0):
                return 1           
    if derection==0:   
        for j in range(min(y1,y2),min(y1,y2)-140,-1):
            if (Wall_img[j][x1]==0):
                return 1
        for j in range(max(y1,y2),max(y1,y2)+140,-1):
            if (Wall_img[j][x1]==0):
                return 1
      
'''
thre  细矩形和封闭扇形端点连接处的所允许的偏差
thre1 表示细矩形端点往里多少个像素
thre2 表示距离 水平细矩形上下/竖直细矩形左右 多少像素开始搜
thre3 门纵横比的下界
thre4 门纵横比的上界

thre6 两个水平相邻门y坐标的距离最大值，竖直相邻门x坐标的距离最大值
thre8,thre9:门宽度的最小最大值(实际数值：0.7m-1m)
'''
def single_door_deal(img, scale, mincc, maxcc, minrr, maxrr, thre, thre1, thre2,thre3,thre4,thre6,thre7,thre8,thre9,bear_wall,nonbearwall):
    minrr_door=[]#y坐标
    mincc_door=[]#x坐标
    maxrr_door=[]#y坐标
    maxcc_door=[]#x坐标
    

    
    ori_single_base_position=[]
    ori_single_Xflip=[]
    ori_single_Yflip=[]
    ori_door_id=[]
    
    m = len(mincc)
    for i in range(m):
        a = 0
        y1 = y2 = y3 = y4 = 9999
        x1 = x2 = x3 = x4 = 9999
        index=0
        for thre11 in range(thre1,thre1+4):
            if maxcc[i] - mincc[i] > maxrr[i] - minrr[i]:
                for a in range(minrr[i] - thre2, 0, -1):
                    if img[a][mincc[i] + thre11]==0:
                        y1 = a                   
                        break
                for a in range(minrr[i] - thre2, 0, -1):
                    if img[a][maxcc[i] - thre11]==0:
                        y2 = a
                        break
                for a in range(maxrr[i] + thre2, len(img)):
                    if img[a][mincc[i] + thre11]==0:
                        y3 = a                   
                        break
                for a in range(maxrr[i] + thre2, len(img)):
                    if img[a][maxcc[i] - thre11]==0:
                        y4 = a
                        break   
                if(((abs(y2 - y1))/(maxcc[i] - mincc[i])) > thre3 and ((abs(y2 - y1))/(maxcc[i] - mincc[i])) < thre4 and max(minrr[i]-y1,minrr[i]-y2)<(maxcc[i]-mincc[i]+thre7)):
                    if(y2 < y1):# and Get_owner_wall.Get_owner_wall([maxcc[i],maxrr[i],maxcc[i],y2,maxcc[i]-mincc[i],0],bear_wall,nonbearwall)!=-1):       
                        mincc_door.append(mincc[i])
                        minrr_door.append(y2)
                        maxcc_door.append(maxcc[i])
                        maxrr_door.append(maxrr[i])
                        
                        y_middle=int((minrr[i]+maxrr[i])/2)
                        ori_single_base_position.append([mincc[i],y_middle,maxcc[i],y_middle,y_middle-minrr[i],maxrr[i]-y_middle])


                        #ori_single_base_position.append([maxcc[i],y2,maxcc[i],maxrr[i],maxcc[i]-mincc[i],0])
                        ori_single_Xflip.append(0)
                        ori_single_Yflip.append(0)
                        ori_door_id.append(Get_owner_wall.Get_owner_wall([mincc[i],y_middle,maxcc[i],y_middle,y_middle-minrr[i],maxrr[i]-y_middle],bear_wall,nonbearwall))
                        
                        index=1
                    if(y2>y1):# and Get_owner_wall.Get_owner_wall([mincc[i],maxrr[i],mincc[i],y1,0,maxcc[i]-mincc[i]],bear_wall,nonbearwall)!=-1):       
                        mincc_door.append(mincc[i])
                        minrr_door.append(y1)
                        maxcc_door.append(maxcc[i])
                        maxrr_door.append(maxrr[i])
                        
                        y_middle=int((minrr[i]+maxrr[i])/2)
                        ori_single_base_position.append([mincc[i],y_middle,maxcc[i],y_middle,y_middle-minrr[i],maxrr[i]-y_middle])
                        
                        #ori_single_base_position.append([mincc[i],y1,mincc[i],maxrr[i],0,maxcc[i]-mincc[i]])
                        ori_single_Xflip.append(0)
                        ori_single_Yflip.append(1)
                        ori_door_id.append(Get_owner_wall.Get_owner_wall([mincc[i],y_middle,maxcc[i],y_middle,y_middle-minrr[i],maxrr[i]-y_middle],bear_wall,nonbearwall))
                        
                        
                        index=1
                if(((abs(y3 - y4))/(maxcc[i] - mincc[i])) > thre3 and ((abs(y3 - y4))/(maxcc[i] - mincc[i])) < thre4 and max(y3-maxrr[i],y4-maxrr[i])<(maxcc[i]-mincc[i]+thre7)):
                    if(y3 < y4 ):#and Get_owner_wall.Get_owner_wall([maxcc[i],minrr[i],maxcc[i],y4,maxcc[i]-mincc[i],0],bear_wall,nonbearwall)!=-1):     
                        mincc_door.append(mincc[i])
                        minrr_door.append(minrr[i])
                        maxcc_door.append(maxcc[i])
                        maxrr_door.append(y4)
                        
                        y_middle=int((minrr[i]+maxrr[i])/2)
                        ori_single_base_position.append([mincc[i],y_middle,maxcc[i],y_middle,y_middle-minrr[i],maxrr[i]-y_middle])

                        #ori_single_base_position.append([maxcc[i],minrr[i],maxcc[i],y4,maxcc[i]-mincc[i],0])
                        ori_single_Xflip.append(1)
                        ori_single_Yflip.append(1)
                        ori_door_id.append(Get_owner_wall.Get_owner_wall([mincc[i],y_middle,maxcc[i],y_middle,y_middle-minrr[i],maxrr[i]-y_middle],bear_wall,nonbearwall))
                        
                        index=1
                    if(y3 > y4 ):#and Get_owner_wall.Get_owner_wall([mincc[i],minrr[i],mincc[i],y3,0,maxcc[i]-mincc[i]],bear_wall,nonbearwall)!=-1):
                        mincc_door.append(mincc[i])
                        minrr_door.append(minrr[i])
                        maxcc_door.append(maxcc[i])
                        maxrr_door.append(y3)
                        
                        y_middle=int((minrr[i]+maxrr[i])/2)
                        ori_single_base_position.append([mincc[i],y_middle,maxcc[i],y_middle,y_middle-minrr[i],maxrr[i]-y_middle])
                        
                        #ori_single_base_position.append([mincc[i],minrr[i],mincc[i],y3,0,maxcc[i]-mincc[i]])
                        ori_single_Xflip.append(1)
                        ori_single_Yflip.append(0)
                        ori_door_id.append(Get_owner_wall.Get_owner_wall([mincc[i],y_middle,maxcc[i],y_middle,y_middle-minrr[i],maxrr[i]-y_middle],bear_wall,nonbearwall))
                        index=1
            if(maxcc[i] - mincc[i] < maxrr[i] - minrr[i]):
                for a in range(mincc[i] - thre2, 0, -1):
                    if img[minrr[i] + thre11][a] == 0:
                        x1 = a                   
                        break
                for a in range(mincc[i] - thre2, 0, -1):
                    if img[maxrr[i] - thre11][a] == 0:
                        x2 = a
                        break
                for a in range(maxcc[i] + thre2, len(img[0])):
                    if img[minrr[i] + thre11][a] == 0:
                        x3 = a                   
                        break
                for a in range(maxcc[i] + thre2, len(img[0])):
                    if img[maxrr[i] - thre11][a] == 0:
                        x4 = a
                        break   
                if(((abs(x2 - x1))/(maxrr[i] - minrr[i])) > thre3 and ((abs(x2 - x1))/(maxrr[i] - minrr[i])) < thre4 and max(mincc[i]-x1,mincc[i]-x2)<(maxrr[i]-minrr[i]+thre7)):
                    if(x2 < x1):# and Get_owner_wall.Get_owner_wall([maxcc[i],maxrr[i],x2,maxrr[i],maxrr[i]-minrr[i],0],bear_wall,nonbearwall)!=-1):              
                        mincc_door.append(x2)
                        minrr_door.append(minrr[i])
                        maxcc_door.append(maxcc[i])
                        maxrr_door.append(maxrr[i])
                        
                        x_middle=int((mincc[i]+maxcc[i])/2)
                        ori_single_base_position.append([x_middle,minrr[i],x_middle,maxrr[i],x_middle-mincc[i],maxcc[i]-x_middle])
                        
                        #ori_single_base_position.append([x2,maxrr[i],maxcc[i],maxrr[i],maxrr[i]-minrr[i],0])
                        ori_single_Xflip.append(1)
                        ori_single_Yflip.append(0)
                        ori_door_id.append(Get_owner_wall.Get_owner_wall([x_middle,minrr[i],x_middle,maxrr[i],x_middle-mincc[i],maxcc[i]-x_middle],bear_wall,nonbearwall))
                        index=1
                    if(x2 > x1):# and Get_owner_wall.Get_owner_wall([maxcc[i],minrr[i],x1,minrr[i],0,maxrr[i]-minrr[i]],bear_wall,nonbearwall)!=-1):              
                        mincc_door.append(x1)
                        minrr_door.append(minrr[i])
                        maxcc_door.append(maxcc[i])
                        maxrr_door.append(maxrr[i])
                        
                        x_middle=int((mincc[i]+maxcc[i])/2)
                        ori_single_base_position.append([x_middle,minrr[i],x_middle,maxrr[i],x_middle-mincc[i],maxcc[i]-x_middle])
                        
                        #ori_single_base_position.append([x1,minrr[i],maxcc[i],minrr[i],0,maxrr[i]-minrr[i]])
                        ori_single_Xflip.append(1)
                        ori_single_Yflip.append(1)
                        ori_door_id.append(Get_owner_wall.Get_owner_wall([x_middle,minrr[i],x_middle,maxrr[i],x_middle-mincc[i],maxcc[i]-x_middle],bear_wall,nonbearwall))
                        index=1
                if(((abs(x3 - x4))/(maxrr[i] - minrr[i])) > thre3 and ((abs(x3 - x4))/(maxrr[i] - minrr[i])) < thre4 and max(x3-mincc[i],x4-mincc[i])<(maxrr[i]-minrr[i]+thre7)):
                    if(x3 < x4 ):#and Get_owner_wall.Get_owner_wall([mincc[i],maxrr[i],x4,maxrr[i],maxrr[i]-minrr[i],0],bear_wall,nonbearwall)!=-1):                
                        mincc_door.append(mincc[i])
                        minrr_door.append(minrr[i])
                        maxcc_door.append(x4)
                        maxrr_door.append(maxrr[i])

                        x_middle=int((mincc[i]+maxcc[i])/2)
                        ori_single_base_position.append([x_middle,minrr[i],x_middle,maxrr[i],x_middle-mincc[i],maxcc[i]-x_middle])
                        
                        #ori_single_base_position.append([mincc[i],maxrr[i],x4,maxrr[i],maxrr[i]-minrr[i],0])
                        ori_single_Xflip.append(0)
                        ori_single_Yflip.append(0)
                        ori_door_id.append(Get_owner_wall.Get_owner_wall([x_middle,minrr[i],x_middle,maxrr[i],x_middle-mincc[i],maxcc[i]-x_middle],bear_wall,nonbearwall))
                        index=1
                    if(x3 > x4):# and Get_owner_wall.Get_owner_wall([mincc[i],minrr[i],x3,minrr[i],0,maxrr[i]-minrr[i]],bear_wall,nonbearwall)!=-1): 
                        mincc_door.append(mincc[i])
                        minrr_door.append(minrr[i])
                        maxcc_door.append(x3)
                        maxrr_door.append(maxrr[i])

                        x_middle=int((mincc[i]+maxcc[i])/2)
                        ori_single_base_position.append([x_middle,minrr[i],x_middle,maxrr[i],x_middle-mincc[i],maxcc[i]-x_middle])

                       # ori_single_base_position.append([mincc[i],minrr[i],x3,minrr[i],0,maxrr[i]-minrr[i]])
                        ori_single_Xflip.append(0)
                        ori_single_Yflip.append(1)
                        ori_door_id.append(Get_owner_wall.Get_owner_wall([x_middle,minrr[i],x_middle,maxrr[i],x_middle-mincc[i],maxcc[i]-x_middle],bear_wall,nonbearwall))
                        index=1
            if(index==1):
                break

# =============================================================================
#     draw_img = cv.cvtColor(draw_img, cv.COLOR_GRAY2RGB)
# 
#     for i in range(len(ori_single_base_position)):       
#         if(ori_single_base_position[i][1]==ori_single_base_position[i][3]):#如果是水平主轴
#             cv.rectangle(draw_img,(min(ori_single_base_position[i][0],ori_single_base_position[i][2]),ori_single_base_position[i][1]-ori_single_base_position[i][4]),(max(ori_single_base_position[i][0],ori_single_base_position[i][2]),ori_single_base_position[i][1]+ori_single_base_position[i][5]),(37,193,255), 2)
#         if(ori_single_base_position[i][0]==ori_single_base_position[i][2]):#如果是竖直主轴    
#             cv.rectangle(draw_img,(ori_single_base_position[i][0]-ori_single_base_position[i][4],min(ori_single_base_position[i][1],ori_single_base_position[i][3])),(ori_single_base_position[i][0]+ori_single_base_position[i][5],max(ori_single_base_position[i][1],ori_single_base_position[i][3])),(37,193,255), 2)
# 
#     #m = len(mincc_door)
#     #for i in range(m):
#         #cv.rectangle(img_door,(mincc_door[i],minrr_door[i]),(maxcc_door[i],maxrr_door[i]),(0,0,255),3)
#     cv.imwrite('draw_img.jpg', draw_img)  
#     
# =============================================================================



    single_base_position=[]
    single_Xflip=[]
    single_Yflip=[]
    single_door_id=[]
    for i in range(len(mincc_door)):
        if (max(maxcc_door[i]-mincc_door[i],maxrr_door[i]-minrr_door[i])*scale >thre8 and max(maxcc_door[i]-mincc_door[i],maxrr_door[i]-minrr_door[i])*scale <thre9):            
            single_base_position.append(ori_single_base_position[i])
            single_Xflip.append(ori_single_Xflip[i])
            single_Yflip.append(ori_single_Yflip[i]) 
            single_door_id.append(ori_door_id[i])
            #cv.line(img2,(ori_single_base_position[i][0],ori_single_base_position[i][1]),(ori_single_base_position[i][2],ori_single_base_position[i][3]),(0,0,255), 5)
    
    
    single_door=Data_struct.Door()
    single_door.set_type(0)
    single_door.add_base_position(single_base_position)
    single_door.add_Xflip(single_Xflip)
    single_door.add_Yflip(single_Yflip)
    single_door.add_door_id(single_door_id)        
            
           
  
    return single_door


'''
thre1 表示细矩形端点往里多少个像素
thre2 表示距离 水平细矩形上下/竖直细矩形左右 多少像素开始搜
thre3,thre4 两边找到的点距离底座的距离的比值范围
thre5 中间找到的点的距离/两边距离的最大值
thre6 底座的长度至少是边的多少倍
thre7 中间点距离底座的最大距离
'''
def double_door_deal(img, mincc, maxcc, minrr, maxrr ,thre1 ,thre2 ,thre3 ,thre4 ,thre5,thre6 ,thre7,bear_wall,nonbearwall):
    
    double_door=Data_struct.Door()
    double_door.set_type(1)        
    double_base_position=[]
    double_Xflip=[]
    double_Yflip=[]
    double_door_id=[]
    y1=y2=y3=x1=x2=x3=0
    y4=y5=y6=x4=x5=x6=99999
    for i in range(len(mincc)):
        if(maxcc[i]-mincc[i]>maxrr[i]-minrr[i]):
            y1_list=[]
            for thre11 in range(thre1,thre1+6):
                for a in range(minrr[i] - thre2, 0, -1):
                    if img[a][mincc[i] + thre11]==0:
                        y1_list.append(a)
                        break
            if(len(y1_list)>0):
                y1=max(y1_list)      
            y1_dis=minrr[i]-y1
            
            y2_list=[]
            for thre11 in range(thre1,thre1+6):
                for a in range(minrr[i] - thre2, 0, -1):
                    if img[a][maxcc[i] - thre11]==0:
                        y2_list.append(a)
                        break
            if(len(y2_list)>0):
                y2=max(y2_list)
            y2_dis=minrr[i]-y2

            y3_list=[]  
            middle=int((mincc[i]+maxcc[i])/2)
            for b in range(middle-8,middle+8):
                for a in range(minrr[i] - thre2, 0, -1):
                    if img[a][b]==0:
                        y3_list.append(a)
                        break
            if(len(y3_list)>0):
                y3=max(y3_list)
            else:
                y3=0
            y3_dis=minrr[i]-y3
            
            y4_list=[]
            for thre11 in range(thre1,thre1+6):
                for a in range(maxrr[i] + thre2, len(img)):
                    if img[a][mincc[i] + thre11]==0:
                        y4_list.append(a)                
                        break
            if(len(y4_list)>0):
                y4=min(y4_list)
            y4_dis=y4-maxrr[i]
            
            y5_list=[]
            for thre11 in range(thre1,thre1+6):
                for a in range(maxrr[i] + thre2, len(img)):
                    if img[a][maxcc[i] - thre11]==0:
                        y5_list.append(a)
                        break 
            if(len(y5_list)>0):
                y5=min(y5_list)       
            y5_dis=y5-maxrr[i]
                
            y6_list=[]
            for b in range(middle-8,middle+8):
                for a in range(maxrr[i] + thre2, len(img)):
                    if img[a][b]==0:
                        y6_list.append(a)
                        break
            if(len(y6_list)>0):
                y6=min(y6_list)
            else:
                y6=9999
            y6_dis=y6-maxrr[i]
            
            if(thre3<(y1_dis/y2_dis)<thre4 and (maxcc[i]-mincc[i])/4<max(y1_dis,y2_dis)<(maxcc[i]-mincc[i])  and maxcc[i]-mincc[i]>((max(y1_dis,y2_dis))*thre6) and y3_dis<thre7):#and y3_dis/(max(y1_dis,y2_dis))<thre5
                index=0
                for mm in range(mincc[i]+thre1+4,mincc[i]+thre1+10):
                    for nn in range(minrr[i]-thre2,y1,-1):
                        if(img[nn][mm]==0):
                            index=1
                            break
                    if(index==1):
                        break
                if(index==1):    
                    y_middle=int((minrr[i]+maxrr[i])/2)
                    double_base_position.append([mincc[i],y_middle,maxcc[i],y_middle,y_middle-minrr[i],maxrr[i]-y_middle])
                    double_Xflip.append(0)
                    double_Yflip.append(0)
                    double_door_id.append(Get_owner_wall.Get_owner_wall([mincc[i],y_middle,maxcc[i],y_middle,y_middle-minrr[i],maxrr[i]-y_middle],bear_wall,nonbearwall))

            if(thre3<(y4_dis/y5_dis)<thre4 and (maxcc[i]-mincc[i])/4<max(y4_dis,y5_dis)<(maxcc[i]-mincc[i])  and maxcc[i]-mincc[i]>((max(y1_dis,y2_dis))*thre6) and y6_dis<thre7):#and y6_dis/(max(y4_dis,y5_dis))<thre5
                index=0
                for mm in range(mincc[i]+thre1+4,mincc[i]+thre1+10):
                    for nn in range(maxrr[i]+thre2,y4):
                        if(img[nn][mm]==0):
                            index=1
                            break
                    if(index==1):
                        break
                if(index==1):    
                    y_middle=int((minrr[i]+maxrr[i])/2)
                    double_base_position.append([mincc[i],y_middle,maxcc[i],y_middle,y_middle-minrr[i],maxrr[i]-y_middle])
                    double_Xflip.append(1)
                    double_Yflip.append(0)
                    double_door_id.append(Get_owner_wall.Get_owner_wall([mincc[i],y_middle,maxcc[i],y_middle,y_middle-minrr[i],maxrr[i]-y_middle],bear_wall,nonbearwall))
           
        elif(maxrr[i]-minrr[i]>maxcc[i]-mincc[i]):
            x1_list=[]
            for thre11 in range(thre1,thre1+6):
                for a in range(mincc[i] - thre2, 0, -1):
                    if img[minrr[i] + thre11][a] == 0:
                        x1_list.append(a)               
                        break
            if(len(x1_list)>0):
                x1=max(x1_list)
            x1_dis=mincc[i]-x1
            
            x2_list=[]
            for thre11 in range(thre1,thre1+6):
                for a in range(mincc[i] - thre2, 0, -1):
                    if img[maxrr[i] - thre11][a] == 0:
                        x2_list.append(a)
                        break
            if(len(x2_list)>0):
                x2=max(x2_list)
            x2_dis=mincc[i]-x2
            
            middle=int((minrr[i]+maxrr[i])/2)
            x3_list=[]
            for a in range(middle-8,middle+8):
                for b in range(mincc[i] - thre2, 0, -1):
                    if img[a][b]==0:
                        x3_list.append(b)
                        break
            
            if(len(x3_list)>0):
                x3=max(x3_list)
            x3_dis=mincc[i]-x3
                    
            x4_list=[]
            for thre11 in range(thre1,thre1+6):
                for a in range(maxcc[i] + thre2, len(img[0])):
                    if img[minrr[i] + thre11][a] == 0:
                        x4_list.append(a)                  
                        break
            if(len(x4_list)>0):
                x4=min(x4_list)
            x4_dis=x4-maxcc[i]
            
            x5_list=[]
            for thre11 in range(thre1,thre1+6):
                for a in range(maxcc[i] + thre2, len(img[0])):
                    if img[maxrr[i] - thre11][a] == 0:
                        x5_list.append(a)        
                        break 
            if(len(x5_list)>0):
                x5=min(x5_list)      
            x5_dis=x5-maxcc[i]
            x6_list=[]
            for a in range(middle-8,middle+8):
                for b in range(maxcc[i] + thre2, len(img[0])):
                    if img[a][b]==0:
                        x6_list.append(b)
                        break
            if(len(x6_list)>0):
                x6=min(x6_list)
            x6_dis=x6-maxcc[i]
            
            if(thre3<(x1_dis/x2_dis)<thre4 and (maxrr[i]-minrr[i])/4<max(x1_dis,x2_dis)<(maxrr[i]-minrr[i])  and maxrr[i]-minrr[i]>((max(x1_dis,x2_dis))*thre6) and x3_dis<thre7):#and x3_dis/(max(x1_dis,x2_dis))<thre5
                index=0
                for mm in range(minrr[i]+thre1+4,minrr[i]+thre1+10):
                    for nn in range(mincc[i]-thre2,x1,-1):
                        if(img[mm][nn]==0):
                            index=1
                            break
                    if(index==1):
                        break
                if(index==1):    
                    x_middle=int((mincc[i]+maxcc[i])/2)
                    double_base_position.append([x_middle,minrr[i],x_middle,maxrr[i],x_middle-mincc[i],maxcc[i]-x_middle])
                    double_Xflip.append(1)
                    double_Yflip.append(0)
                    double_door_id.append(Get_owner_wall.Get_owner_wall([x_middle,minrr[i],x_middle,maxrr[i],x_middle-mincc[i],maxcc[i]-x_middle],bear_wall,nonbearwall))
                    

            if(thre3<(x4_dis/x5_dis)<thre4 and (maxrr[i]-minrr[i])/4<max(x4_dis,x5_dis)<(maxrr[i]-minrr[i])  and maxrr[i]-minrr[i]>((max(x4_dis,x5_dis))*thre6) and x6_dis<thre7):#and x6_dis/(max(x4_dis,x5_dis))<thre5
                index=0
                for mm in range(minrr[i]+thre1+4,minrr[i]+thre1+10):
                    for nn in range(maxcc[i]+thre2,x4):
                        if(img[mm][nn]==0):
                            index=1
                            break
                    if(index==1):
                        break
                if(index==1):    
                    x_middle=int((mincc[i]+maxcc[i])/2)
                    double_base_position.append([x_middle,minrr[i],x_middle,maxrr[i],x_middle-mincc[i],maxcc[i]-x_middle])
                    double_Xflip.append(0)
                    double_Yflip.append(0)
                    double_door_id.append(Get_owner_wall.Get_owner_wall([x_middle,minrr[i],x_middle,maxrr[i],x_middle-mincc[i],maxcc[i]-x_middle],bear_wall,nonbearwall))
            
            
            

    double_door.add_base_position(double_base_position)
    double_door.add_Xflip(double_Xflip)
    double_door.add_Yflip(double_Yflip)
    double_door.add_door_id(double_door_id)  
    
    return double_door      




def get_corner_position_ju(img,scale, min_xiju_area, max_xiju_area, min_zonghengbi, max_zonghengbi,max_len):#细矩形
    label_image=measure.label(img, connectivity = 2)  #4连通区域标记
    minrr=[]#y坐标
    mincc=[]#x坐标
    maxrr=[]#y坐标
    maxcc=[]#x坐标
    for region in measure.regionprops(label_image):
        if region.area < min_xiju_area or region.area > max_xiju_area:
            continue
        minr, minc, maxr, maxc = region.bbox
        minrr.append(minr)
        mincc.append(minc)
        maxrr.append(maxr)
        maxcc.append(maxc)
    minrr_1=[]#y坐标
    mincc_1=[]#x坐标
    maxrr_1=[]#y坐标
    maxcc_1=[]#x坐标
    m = len(minrr)
#    count = 0
    img= cv.cvtColor(img, cv.COLOR_GRAY2RGB)
    for i in range(m):
        if min((maxrr[i] - minrr[i])/(maxcc[i] -mincc[i]), (maxcc[i] -mincc[i])/(maxrr[i] - minrr[i])) > min_zonghengbi and min((maxrr[i] - minrr[i])/(maxcc[i] -mincc[i]), (maxcc[i] -mincc[i])/(maxrr[i] - minrr[i])) < max_zonghengbi and max(maxcc[i] -mincc[i], maxrr[i] - minrr[i]) * scale < max_len:
            cv.rectangle(img,(mincc[i],minrr[i]),(maxcc[i],maxrr[i]),(66,90,255),3)
#            count += 1
            minrr_1.append(minrr[i])
            mincc_1.append(mincc[i])
            maxrr_1.append(maxrr[i])
            maxcc_1.append(maxcc[i])
#    print(count)
    #cv.imwrite('E:\\Lab\\DR\\door_test_v2\\jieguo\\'+str(num)+'-xiju.jpg', img) 
    
    cv.imwrite('juxing/juxing.png',img)
    return mincc_1, maxcc_1, minrr_1, maxrr_1 




        



def get_corner_position(img):
    label_image=measure.label(img,connectivity=2)  #8连通区域标记
    minrr=[]#y坐标
    mincc=[]#x坐标
    maxrr=[]#y坐标
    maxcc=[]#x坐标
    for region in measure.regionprops(label_image): #循环得到每一个连通区域属性集
        #忽略小区域
        if region.area < 100:
            continue
        minr, minc, maxr, maxc = region.bbox
        minrr.append(minr)
        mincc.append(minc)
        maxrr.append(maxr)
        maxcc.append(maxc)
#    m=len(minrr)
#    for i in range(m):
#        cv.rectangle(img,(mincc[i],minrr[i]),(maxcc[i],maxrr[i]),(0,0,255),3)
#    cv.imwrite('juxing.jpg', img)  
    return mincc, maxcc, minrr, maxrr

def detect_slidingdoor_xiju(mincc,minrr,maxcc,maxrr,thre): 
    minrr_xiju=[]#y坐标
    mincc_xiju=[]#x坐标
    maxrr_xiju=[]#y坐标
    maxcc_xiju=[]#x坐标
    lenm=len(mincc)
    for i in range(lenm):
        x_diff_i=maxcc[i]-mincc[i]
        y_diff_i=maxrr[i]-minrr[i]
        if ((min(x_diff_i,y_diff_i)/max(x_diff_i,y_diff_i))<thre and x_diff_i>=1 and y_diff_i>=1):
            minrr_xiju.append(minrr[i])
            mincc_xiju.append(mincc[i])
            maxrr_xiju.append(maxrr[i])
            maxcc_xiju.append(maxcc[i])
    return mincc_xiju,minrr_xiju,maxcc_xiju,maxrr_xiju


def delete_repeatslidingdoor(sliding_position,sliding_Xflip,sliding_Yflip,sliding_door_id,bear_wall,nonbearwall):
    new_sliding_position=[]
    new_sliding_Xflip=[]
    new_sliding_Yflip=[]
    new_sliding_door_id=[]
    
    minrr_sliding=[]
    maxrr_sliding=[]
    mincc_sliding=[]
    maxcc_sliding=[]
    repeat_index=[]


    for i in range(len(sliding_position)):
        if(sliding_Xflip[i]==0 and sliding_Yflip[i]==0):
            mincc_sliding.append(min(sliding_position[i][0],sliding_position[i][2]))
            maxcc_sliding.append(max(sliding_position[i][0],sliding_position[i][2]))
            minrr_sliding.append(sliding_position[i][1]-sliding_position[i][4])
            maxrr_sliding.append(sliding_position[i][1]+sliding_position[i][5])
        if(sliding_Xflip[i]==1 and sliding_Yflip[i]==1):
            mincc_sliding.append(sliding_position[i][0]-sliding_position[i][4])
            maxcc_sliding.append(sliding_position[i][0]+sliding_position[i][5])
            minrr_sliding.append(min(sliding_position[i][1],sliding_position[i][3]))
            maxrr_sliding.append(max(sliding_position[i][1],sliding_position[i][3]))
    
    for i in range(len(minrr_sliding)):
        for j in range(i+1,len(minrr_sliding)):
            if(sliding_Xflip[i]==sliding_Xflip[j] and sliding_Yflip[i]==sliding_Yflip[j]):
                if((abs(mincc_sliding[i]-maxcc_sliding[j])<5 or abs(mincc_sliding[j]-maxcc_sliding[i])<5) and abs(minrr_sliding[i]-minrr_sliding[j])<3 and abs(maxrr_sliding[i]-maxrr_sliding[j])<3):
                    y_middle=int((min(minrr_sliding[i],minrr_sliding[j])+max(maxrr_sliding[i],maxrr_sliding[j]))/2)
                    x_min=min(mincc_sliding[i],mincc_sliding[j])
                    x_max=max(maxcc_sliding[i],maxcc_sliding[j])
                    new_sliding_position.append([x_min,y_middle,x_max,y_middle,y_middle-min(minrr_sliding[i],minrr_sliding[j]),max(maxrr_sliding[i],maxrr_sliding[j])-y_middle])
                    new_sliding_Xflip.append(sliding_Xflip[i])
                    new_sliding_Yflip.append(sliding_Yflip[i])
                    new_sliding_door_id.append(Get_owner_wall.Get_owner_wall([x_min,y_middle,x_min,y_middle,y_middle-min(minrr_sliding[i],minrr_sliding[j]),max(maxrr_sliding[i],maxrr_sliding[j])-y_middle],bear_wall,nonbearwall))
                    repeat_index.append(i)
                    repeat_index.append(j)
                if((abs(minrr_sliding[i]-maxrr_sliding[j])<5 or abs(minrr_sliding[j]-maxrr_sliding[i])<5) and abs(mincc_sliding[i]-mincc_sliding[j])<3 and abs(maxcc_sliding[i]-maxcc_sliding[j])<3):
                    x_middle=int((min(mincc_sliding[i],mincc_sliding[j])+max(maxcc_sliding[i],maxcc_sliding[j]))/2)
                    y_min=min(minrr_sliding[i],minrr_sliding[j])
                    y_max=max(maxrr_sliding[i],maxrr_sliding[j])
                    new_sliding_position.append([x_middle,y_min,x_middle,y_max,x_middle-min(mincc_sliding[i],mincc_sliding[j]),max(maxcc_sliding[i],maxcc_sliding[j])-x_middle])
                    new_sliding_Xflip.append(sliding_Xflip[i])
                    new_sliding_Yflip.append(sliding_Yflip[i])
                    new_sliding_door_id.append(Get_owner_wall.Get_owner_wall([x_middle,y_min,x_middle,y_max,x_middle-min(mincc_sliding[i],mincc_sliding[j]),max(maxcc_sliding[i],maxcc_sliding[j])-x_middle],bear_wall,nonbearwall))
                    repeat_index.append(i)
                    repeat_index.append(j)
                if((mincc_sliding[j]<mincc_sliding[i]<maxcc_sliding[j] or mincc_sliding[i]<mincc_sliding[j]<maxcc_sliding[i]) and abs(minrr_sliding[i]-minrr_sliding[j])<3 and abs(maxrr_sliding[i]-maxrr_sliding[j])<3):
                    y_middle=int((min(minrr_sliding[i],minrr_sliding[j])+max(maxrr_sliding[i],maxrr_sliding[j]))/2)
                    x_min=min(mincc_sliding[i],mincc_sliding[j])
                    x_max=max(maxcc_sliding[i],maxcc_sliding[j])
                    new_sliding_position.append([x_min,y_middle,x_max,y_middle,y_middle-min(minrr_sliding[i],minrr_sliding[j]),max(maxrr_sliding[i],maxrr_sliding[j])-y_middle])
                    new_sliding_Xflip.append(sliding_Xflip[i])
                    new_sliding_Yflip.append(sliding_Yflip[i])
                    new_sliding_door_id.append(Get_owner_wall.Get_owner_wall([x_min,y_middle,x_min,y_middle,y_middle-min(minrr_sliding[i],minrr_sliding[j]),max(maxrr_sliding[i],maxrr_sliding[j])-y_middle],bear_wall,nonbearwall))
                    repeat_index.append(i)
                    repeat_index.append(j)
                if((minrr_sliding[j]<minrr_sliding[i]<maxrr_sliding[j] or minrr_sliding[i]<minrr_sliding[j]<maxrr_sliding[i])  and abs(mincc_sliding[i]-mincc_sliding[j])<3 and abs(maxcc_sliding[i]-maxcc_sliding[j])<3):
                    x_middle=int((min(mincc_sliding[i],mincc_sliding[j])+max(maxcc_sliding[i],maxcc_sliding[j]))/2)
                    y_min=min(minrr_sliding[i],minrr_sliding[j])
                    y_max=max(maxrr_sliding[i],maxrr_sliding[j])
                    new_sliding_position.append([x_middle,y_min,x_middle,y_max,x_middle-min(mincc_sliding[i],mincc_sliding[j]),max(maxcc_sliding[i],maxcc_sliding[j])-x_middle])
                    new_sliding_Xflip.append(sliding_Xflip[i])
                    new_sliding_Yflip.append(sliding_Yflip[i])
                    new_sliding_door_id.append(Get_owner_wall.Get_owner_wall([x_middle,y_min,x_middle,y_max,x_middle-min(mincc_sliding[i],mincc_sliding[j]),max(maxcc_sliding[i],maxcc_sliding[j])-x_middle],bear_wall,nonbearwall))
                    repeat_index.append(i)
                    repeat_index.append(j)
                
    
    for i in range(len(minrr_sliding)):
        if i not in repeat_index:
            new_sliding_position.append(sliding_position[i])
            new_sliding_Xflip.append(sliding_Xflip[i])
            new_sliding_Yflip.append(sliding_Yflip[i])
            new_sliding_door_id.append(sliding_door_id[i])
                    
            
    return new_sliding_position, new_sliding_Xflip,new_sliding_Yflip ,new_sliding_door_id      
    
    
    
#thre1,thre2:推拉门的两个矩形的比例限制
#thre3:两个细矩形之间的最大值
#thre4：两个细矩形至少交错开多少####!!以后改成用百分比来限制！！

#thre6:细矩形短的那条边的长度最多相差多少
def detect_slidingdoor(mincc,maxcc,minrr,maxrr,thre1,thre2,thre3,thre4,thre6,bear_wall,nonbearwall):    

    sliding_base_position=[]
    sliding_Xflip=[]
    sliding_Yflip=[]
    sliding_door_id=[]
    
    sliding_index=[]
    #slidingdoor=[]
    lenm=len(mincc)
    for i in range(lenm):
        for j in range(i+1,lenm):
            x_diff_i=maxcc[i]-mincc[i]
            y_diff_i=maxrr[i]-minrr[i]
            x_diff_j=maxcc[j]-mincc[j]
            y_diff_j=maxrr[j]-minrr[j]
            if (x_diff_i>y_diff_i):
                if(maxrr[i]<=minrr[j]):#水平推拉门
                    if ((x_diff_i/x_diff_j)>thre1 and (x_diff_i/x_diff_j)<thre2 and abs(y_diff_i-y_diff_j)<thre6 and (minrr[j]-maxrr[i]<thre3) and abs(mincc[j]-mincc[i])>thre4 and abs(mincc[j]-mincc[i])<(max(x_diff_i,x_diff_j)+5)):
                        y_middle=int((max(maxrr[i],maxrr[j])+min(minrr[i],minrr[j]))/2)
                        y_up=abs(y_middle-min(minrr[i],minrr[j]))
                        y_down=abs(max(maxrr[i],maxrr[j])-y_middle)
                        #cv.line(Wall_img,(min(mincc[i],mincc[j]), y_middle),(max(maxrr[i],maxrr[j]),y_middle),(0,0,255),5)
                        #cv.imwrite('aa.png',Wall_img)
                        #if(Get_owner_wall.Get_owner_wall([min(mincc[i],mincc[j]), y_middle,max(maxcc[i],maxcc[j]),y_middle,y_up,y_down],bear_wall,nonbearwall)!=-1):
                        sliding_base_position.append([min(mincc[i],mincc[j]), y_middle,max(maxcc[i],maxcc[j]),y_middle,y_up,y_down])
                        sliding_Xflip.append(0)  
                        sliding_Yflip.append(0)
                        sliding_door_id.append(Get_owner_wall.Get_owner_wall([min(mincc[i],mincc[j]), y_middle,max(maxcc[i],maxcc[j]),y_middle,y_up,y_down],bear_wall,nonbearwall))
                        sliding_index.append(i)
                        sliding_index.append(j)
                if(maxrr[j]<minrr[i]):
                    if ((x_diff_i/x_diff_j)>thre1 and (x_diff_i/x_diff_j)<thre2  and abs(y_diff_i-y_diff_j)<thre6 and (y_diff_i/y_diff_j)<thre2 and (minrr[i]-maxrr[j]<thre3) and abs(mincc[j]-mincc[i])>thre4 and abs(mincc[j]-mincc[i])<(max(x_diff_i,x_diff_j)+5)):
                        y_middle=int((max(maxrr[i],maxrr[j])+min(minrr[i],minrr[j]))/2)
                        y_up=abs(y_middle-min(minrr[i],minrr[j]))
                        y_down=abs(max(maxrr[i],maxrr[j])-y_middle)
                        #if(Get_owner_wall.Get_owner_wall([min(mincc[i],mincc[j]), y_middle,max(maxcc[i],maxcc[j]),y_middle,y_up,y_down],bear_wall,nonbearwall)!=-1):
                        sliding_base_position.append([min(mincc[i],mincc[j]), y_middle,max(maxcc[i],maxcc[j]),y_middle,y_up,y_down])
                        sliding_Xflip.append(0)  
                        sliding_Yflip.append(0)
                        sliding_door_id.append(Get_owner_wall.Get_owner_wall([min(mincc[i],mincc[j]), y_middle,max(maxcc[i],maxcc[j]),y_middle,y_up,y_down],bear_wall,nonbearwall))
                        sliding_index.append(i)
                        sliding_index.append(j)

                       
            if (x_diff_i<y_diff_i):
                if(maxcc[i]<=mincc[j]):
                    if ((y_diff_i/y_diff_j)>thre1 and (y_diff_i/y_diff_j)<thre2  and abs(x_diff_i-x_diff_j)<thre6 and (x_diff_i/x_diff_j)<thre2 and (mincc[j]-maxcc[i]<thre3)and abs(minrr[j]-minrr[i])>thre4 and abs(minrr[j]-minrr[i])<(max(y_diff_i,y_diff_j)+5)):
                        x_middle=int((max(maxcc[i],maxcc[j])+min(mincc[i],mincc[j]))/2)
                        x_left=abs(x_middle-min(mincc[i],mincc[j]))
                        x_right=abs(max(maxcc[i],maxcc[j])-x_middle)
                        #if(Get_owner_wall.Get_owner_wall([x_middle,min(minrr[i],minrr[j]),x_middle,max(maxrr[i],maxrr[j]),x_left,x_right],bear_wall,nonbearwall)!=-1):
                        sliding_base_position.append([x_middle,min(minrr[i],minrr[j]),x_middle,max(maxrr[i],maxrr[j]),x_left,x_right])
                        sliding_Xflip.append(1)  
                        sliding_Yflip.append(1)
                        sliding_door_id.append(Get_owner_wall.Get_owner_wall([x_middle,min(minrr[i],minrr[j]),x_middle,max(maxrr[i],maxrr[j]),x_left,x_right],bear_wall,nonbearwall))
                        sliding_index.append(i)
                        sliding_index.append(j)
                      
                if(maxcc[j]<mincc[i]):
                    if ((y_diff_i/y_diff_j)>thre1 and (y_diff_i/y_diff_j)<thre2  and abs(x_diff_i-x_diff_j)<thre6 and (x_diff_i/x_diff_j)<thre2 and (mincc[i]-maxcc[j]<thre3)and abs(minrr[j]-minrr[i])>thre4 and abs(minrr[j]-minrr[i])<(max(y_diff_i,y_diff_j)+5)):#原来是+20
                        x_middle=int((max(maxcc[i],maxcc[j])+min(mincc[i],mincc[j]))/2)
                        x_left=abs(x_middle-min(mincc[i],mincc[j]))
                        x_right=abs(max(maxcc[i],maxcc[j])-x_middle)
                        #if(Get_owner_wall.Get_owner_wall([x_middle,min(minrr[i],minrr[j]),x_middle,max(maxrr[i],maxrr[j]),x_left,x_right],bear_wall,nonbearwall)!=-1):
                        sliding_base_position.append([x_middle,min(minrr[i],minrr[j]),x_middle,max(maxrr[i],maxrr[j]),x_left,x_right])
                        sliding_Xflip.append(1)  
                        sliding_Yflip.append(1)
                        sliding_door_id.append(Get_owner_wall.Get_owner_wall([x_middle,min(minrr[i],minrr[j]),x_middle,max(maxrr[i],maxrr[j]),x_left,x_right],bear_wall,nonbearwall))
                        sliding_index.append(i)
                        sliding_index.append(j)
    
    for i in range(len(mincc)):
        for j in range(i+1,len(mincc)):
            for k in range(j+1,len(mincc)):
                if(i not in sliding_index and j not in sliding_index and k not in sliding_index):
                    sort_mincc=[mincc[i],mincc[j],mincc[k]]
                    sort_mincc.sort()
                    sort_maxcc=[maxcc[i],maxcc[j],maxcc[k]]
                    sort_maxcc.sort()
                    sort_minrr=[minrr[i],minrr[j],minrr[k]]
                    sort_minrr.sort()
                    sort_maxrr=[maxrr[i],maxrr[j],maxrr[k]]
                    sort_maxrr.sort()
                    if(0<sort_mincc[1]-sort_maxcc[0]<5 and 0<sort_mincc[2]-sort_maxcc[1]<5 and sort_minrr[1]-sort_minrr[0]<10 and sort_minrr[2]-sort_minrr[1]<10 and sort_maxrr[1]-sort_maxrr[0]<10 and sort_maxrr[2]-sort_maxrr[1]<10):
                        y_middle=int((sort_minrr[0]+sort_maxrr[2])/2)
                        y_up=y_middle-sort_minrr[0]
                        y_down=sort_maxrr[2]-y_middle
                        sliding_base_position.append([sort_mincc[0], y_middle,sort_maxcc[2],y_middle,y_up,y_down])
                        sliding_Xflip.append(0)  
                        sliding_Yflip.append(0)
                        sliding_door_id.append(Get_owner_wall.Get_owner_wall([sort_mincc[0], y_middle,sort_maxcc[2],y_middle,y_up,y_down],bear_wall,nonbearwall))
                        sliding_index.append(i)
                        sliding_index.append(j)
                        sliding_index.append(k)
                    if(0<sort_minrr[1]-sort_maxrr[0]<5 and 0<sort_minrr[2]-sort_maxrr[1]<5 and sort_mincc[1]-sort_mincc[0]<10 and sort_mincc[2]-sort_mincc[1]<10 and sort_maxcc[1]-sort_maxcc[0]<10 and sort_maxcc[2]-sort_maxcc[1]<10):
                        x_middle=int((sort_mincc[0]+sort_maxcc[2])/2)
                        x_left=x_middle-sort_mincc[0]
                        x_right=sort_maxcc[2]-x_middle
                        sliding_base_position.append([x_middle,sort_minrr[0],x_middle,sort_minrr[2],x_left,x_right])
                        sliding_Xflip.append(1)  
                        sliding_Yflip.append(1)
                        sliding_door_id.append(Get_owner_wall.Get_owner_wall([x_middle,sort_minrr[0],x_middle,sort_minrr[2],x_left,x_right],bear_wall,nonbearwall))
                        sliding_index.append(i)
                        sliding_index.append(j)
                        sliding_index.append(k)
    

                 
   
    new_sliding_base_position,new_sliding_Xflip,new_sliding_Yflip,new_sliding_door_id=delete_repeatslidingdoor(sliding_base_position,sliding_Xflip,sliding_Yflip,sliding_door_id,bear_wall,nonbearwall)            
    
    sliding_door=Data_struct.Door()          
    sliding_door.set_type(2)
    sliding_door.add_base_position(new_sliding_base_position)
    sliding_door.add_Xflip(new_sliding_Xflip)
    sliding_door.add_Yflip(new_sliding_Yflip)
    sliding_door.add_door_id(new_sliding_door_id)
# =============================================================================
#     sliding_door.add_base_position(sliding_base_position)
#     sliding_door.add_Xflip(sliding_Xflip)
#     sliding_door.add_Yflip(sliding_Yflip)
#     sliding_door.add_door_id(sliding_door_id)
# =============================================================================
    return sliding_door
    #return mincc_slidingdoor,maxcc_slidingdoor,minrr_slidingdoor,maxrr_slidingdoor,slidingdoor_derection
def coordinate(middleline):
    if abs(middleline[0] - middleline[2])<=2:
        x1 = middleline[0] - middleline[4]
        y1 = middleline[1]
        x2 = middleline[2] + middleline[5]
        y2 = middleline[3]
    else:
        x1 = middleline[0]
        y1 = middleline[1] - middleline[4]
        x2 = middleline[2]
        y2 = middleline[3] + middleline[5]
    return x1,x2,y1,y2
'''
传入的img是二值化以后的图
'''
def Door_detect(img , scale,bear_wall,nonbearwall, mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win,door_opening,door_opening_id):
    door_opening,door_opening_id = Get_door.remove_repetition_two_rect( mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win,door_opening,door_opening_id,1/scale)
    for i in range(len(door_opening)):
        x1,x2,y1,y2 = coordinate(door_opening[i])
        mincc_two_rect_win.append(x1)
        minrr_two_rect_win.append(y1)
        maxcc_two_rect_win.append(x2)
        maxrr_two_rect_win.append(y2)
    img_v1 = copy.copy(img)
    c_img = copy.copy(img)
    img_door=copy.copy(img)
    #doors=[]
# =============================================================================
#     img_door = cv.cvtColor(img_door, cv.COLOR_GRAY2RGB)
#     for i in range(len(mincc_two_rect_win)):
#         cv.rectangle(img_door,(mincc_two_rect_win[i],minrr_two_rect_win[i]),(maxcc_two_rect_win[i],maxrr_two_rect_win[i]),(0,0,255),2)
#     cv.imwrite('two_rect.png', img_door)
# =============================================================================


    mincc_x, maxcc_x, minrr_y, maxrr_y = get_corner_position(img_v1)
    mincc_ju, maxcc_ju, minrr_ju, maxrr_ju = get_corner_position_ju(c_img,scale, Settings.min_rectangle_area, Settings.max_rectangle_area, Settings.min_ratio,Settings.max_ratio, Settings.max_lenth )
   
    single_door = single_door_deal(c_img, scale, mincc_two_rect_win, maxcc_two_rect_win, minrr_two_rect_win, maxrr_two_rect_win, Settings.max_error ,Settings.inner_dis, Settings.thre, Settings.min_sca, Settings.max_sca, Settings.max_dis,Settings.err,Settings.min_len,Settings.max_len,bear_wall,nonbearwall)
    #doors.extend(singledoor)
    #doors.extend(doubledoor)

    sliding_door= detect_slidingdoor(mincc_ju, maxcc_ju, minrr_ju, maxrr_ju, Settings.min_sliding_ratio, Settings.max_sliding_ratio, Settings.max_distance, Settings.min_jiaocuo, Settings.min_xiangcha,bear_wall,nonbearwall)   
    
    double_door=double_door_deal(c_img, mincc_two_rect_win, maxcc_two_rect_win, minrr_two_rect_win, maxrr_two_rect_win,Settings.inner,Settings.outer,Settings.double_minsca,Settings.double_maxsca,Settings.middle_maxdis_sca,Settings.min_times,Settings.middle_dis,bear_wall,nonbearwall)

# =============================================================================
#     sliding_position=double_door.out_base_position() 
#     img_door = cv.cvtColor(img_door, cv.COLOR_GRAY2RGB)
#     for i in range(len(sliding_position)):       
#         if(sliding_position[i][1]==sliding_position[i][3]):#如果是水平主轴
#             cv.rectangle(img_door,(min(sliding_position[i][0],sliding_position[i][2]),sliding_position[i][1]-sliding_position[i][4]),(max(sliding_position[i][0],sliding_position[i][2]),sliding_position[i][1]+sliding_position[i][5]),(37,193,255), 2)
#         if(sliding_position[i][0]==sliding_position[i][2]):#如果是竖直主轴    
#             cv.rectangle(img_door,(sliding_position[i][0]-sliding_position[i][4],min(sliding_position[i][1],sliding_position[i][3])),(sliding_position[i][0]+sliding_position[i][5],max(sliding_position[i][1],sliding_position[i][3])),(37,193,255), 2)
#     
#     cv.imwrite('door.png',img_door)
# =============================================================================
    
   
    return single_door,double_door,sliding_door#,img_door

def delete_single_door(img,single_door,delete_xy):
    new_single_door=Data_struct.Door()
    img_single = copy.copy(img)
    single_position=single_door.out_base_position()
    single_Xflip=single_door.out_Xflip()
    single_Yflip=single_door.out_Yflip()
    single_door_id=single_door.out_door_id()
    delete_index=[]
    single_xy=[]
    for i in range(len(single_position)):
        if(single_position[i][1]==single_position[i][3]):#如果是水平主轴
            x1=min(single_position[i][0],single_position[i][2])
            y1=single_position[i][1]-single_position[i][4]
            x2=max(single_position[i][0],single_position[i][2])
            y2=single_position[i][1]+single_position[i][5]
            single_xy.append([x1,y1,x2,y2])
        if(single_position[i][0]==single_position[i][2]):#如果是竖直主轴   
            x1=single_position[i][0]-single_position[i][4]
            y1=min(single_position[i][1],single_position[i][3])
            x2=single_position[i][0]+single_position[i][5]
            y2=max(single_position[i][1],single_position[i][3])
            single_xy.append([x1,y1,x2,y2])
            
    delete_x=delete_xy[0]
    delete_y=delete_xy[1]
    for i in range(len(single_xy)):
        x1=single_xy[i][0]
        y1=single_xy[i][1]
        x2=single_xy[i][2]
        y2=single_xy[i][3]
        if(delete_x>x1 and delete_x<x2 and delete_y>y1 and delete_y<y2):
            delete_index.append(i)
            break
#    print(delete_index)
#    print(single_position)
#    print(single_Xflip)
#    print(single_Yflip)
    for i in range(len(delete_index)):
        single_position.pop(delete_index[i])
        single_Xflip.pop(delete_index[i])
        single_Yflip.pop(delete_index[i])
        single_door_id.pop(delete_index[i])
   
    new_single_door.set_type(0)
    new_single_door.add_base_position(single_position)
    new_single_door.add_Xflip(single_Xflip)
    new_single_door.add_Yflip(single_Yflip)
    new_single_door.add_door_id(single_door_id)   
    
    img_single = cv.cvtColor(img_single, cv.COLOR_GRAY2RGB)
    for i in range(len(single_position)):
        if(single_position[i][1]==single_position[i][3]):#如果是水平主轴
            cv.rectangle(img_single,(min(single_position[i][0],single_position[i][2]),single_position[i][1]-single_position[i][4]),(max(single_position[i][0],single_position[i][2]),single_position[i][1]+single_position[i][5]),(255,0,0), 10)
        if(single_position[i][0]==single_position[i][2]):#如果是竖直主轴    
            cv.rectangle(img_single,(single_position[i][0]-single_position[i][4],min(single_position[i][1],single_position[i][3])),(single_position[i][0]+single_position[i][5],max(single_position[i][1],single_position[i][3])),(255,0,0), 10)

    return new_single_door#,img_single
    
    
def delete_double_door(img,double_door,delete_xy):
    new_double_door=Data_struct.Door()
    img_double = copy.copy(img)

    delete_index=[]
    double_position=double_door.out_base_position()
    double_Xflip=double_door.out_Xflip()
    double_Yflip=double_door.out_Yflip()
    double_door_id=double_door.out_door_id()
    
    double_xy=[]
    for i in range(len(double_position)):       
        if(double_position[i][1]==double_position[i][3]):#如果是水平主轴
            x1=min(double_position[i][0],double_position[i][2])
            y1=double_position[i][1]-double_position[i][4]
            x2=max(double_position[i][0],double_position[i][2])
            y2=double_position[i][1]+double_position[i][5]
            double_xy.append([x1,y1,x2,y2])
        if(double_position[i][0]==double_position[i][2]):#如果是竖直主轴    
            x1=double_position[i][0]-double_position[i][4]
            y1=min(double_position[i][1],double_position[i][3])
            x2=double_position[i][0]+double_position[i][5]
            y2=max(double_position[i][1],double_position[i][3])
            double_xy.append([x1,y1,x2,y2])
            
    delete_x=delete_xy[0]
    delete_y=delete_xy[1]
    for i in range(len(double_xy)):
        x1=double_xy[i][0]
        y1=double_xy[i][1]
        x2=double_xy[i][2]
        y2=double_xy[i][3]
        if(delete_x>x1 and delete_x<x2 and delete_y>y1 and delete_y<y2):
            delete_index.append(i)
            break
    for i in range(len(delete_index)):
        double_position.pop(delete_index[i])
        double_Xflip.pop(delete_index[i])
        double_Yflip.pop(delete_index[i])
        double_door_id.pop(delete_index[i])
   
    new_double_door.set_type(1)
    new_double_door.add_base_position(double_position)
    new_double_door.add_Xflip(double_Xflip)
    new_double_door.add_Yflip(double_Yflip)
    new_double_door.add_door_id(double_door_id)      
    
    img_double = cv.cvtColor(img_double, cv.COLOR_GRAY2RGB)
    for i in range(len(double_position)):       
        if(double_position[i][1]==double_position[i][3]):#如果是水平主轴
            cv.rectangle(img_double,(min(double_position[i][0],double_position[i][2]),double_position[i][1]-double_position[i][4]),(max(double_position[i][0],double_position[i][2]),double_position[i][1]+double_position[i][5]),(147,112,219), 10)
        if(double_position[i][0]==double_position[i][2]):#如果是竖直主轴    
            cv.rectangle(img_double,(double_position[i][0]-double_position[i][4],min(double_position[i][1],double_position[i][3])),(double_position[i][0]+double_position[i][5],max(double_position[i][1],double_position[i][3])),(147,112,219), 10)

    return new_double_door#,img_double

def delete_sliding_door(img,slding_door,delete_xy):
    new_sliding_door=Data_struct.Door()
    img_slding = copy.copy(img)
    sliding_position=slding_door.out_base_position()
    sliding_Xflip=slding_door.out_Xflip()
    sliding_Yflip=slding_door.out_Yflip()
    sliding_door_id=slding_door.out_door_id()
    sliding_xy=[]
    delete_index=[]        
    for i in range(len(sliding_position)):       
        if(sliding_position[i][1]==sliding_position[i][3]):#如果是水平主轴
            x1=min(sliding_position[i][0],sliding_position[i][2])
            y1=sliding_position[i][1]-sliding_position[i][4]
            x2=max(sliding_position[i][0],sliding_position[i][2])
            y2=sliding_position[i][1]+sliding_position[i][5]
            sliding_xy.append([x1,y1,x2,y2])
        if(sliding_position[i][0]==sliding_position[i][2]):#如果是竖直主轴    
            x1=sliding_position[i][0]-sliding_position[i][4]
            y1=min(sliding_position[i][1],sliding_position[i][3])
            x2=sliding_position[i][0]+sliding_position[i][5]
            y2=max(sliding_position[i][1],sliding_position[i][3])
            sliding_xy.append([x1,y1,x2,y2])
    
    delete_x=delete_xy[0]
    delete_y=delete_xy[1]
    for i in range(len(sliding_xy)):
        x1=sliding_xy[i][0]
        y1=sliding_xy[i][1]
        x2=sliding_xy[i][2]
        y2=sliding_xy[i][3]
        if(delete_x>x1 and delete_x<x2 and delete_y>y1 and delete_y<y2):
            delete_index.append(i)
            break
    for i in range(len(delete_index)):
        sliding_position.pop(delete_index[i])
        sliding_Xflip.pop(delete_index[i])
        sliding_Yflip.pop(delete_index[i])
        sliding_door_id.pop(delete_index[i])
        
    new_sliding_door.set_type(1)
    new_sliding_door.add_base_position(sliding_position)
    new_sliding_door.add_Xflip(sliding_Xflip)
    new_sliding_door.add_Yflip(sliding_Yflip)
    new_sliding_door.add_door_id(sliding_door_id)      
    
    img_slding = cv.cvtColor(img_slding, cv.COLOR_GRAY2RGB)
            
    for i in range(len(sliding_position)):       
        if(sliding_position[i][1]==sliding_position[i][3]):#如果是水平主轴
            cv.rectangle(img_slding,(min(sliding_position[i][0],sliding_position[i][2]),sliding_position[i][1]-sliding_position[i][4]),(max(sliding_position[i][0],sliding_position[i][2]),sliding_position[i][1]+sliding_position[i][5]),(37,193,255), 10)
        if(sliding_position[i][0]==sliding_position[i][2]):#如果是竖直主轴    
            cv.rectangle(img_slding,(sliding_position[i][0]-sliding_position[i][4],min(sliding_position[i][1],sliding_position[i][3])),(sliding_position[i][0]+sliding_position[i][5],max(sliding_position[i][1],sliding_position[i][3])),(37,193,255), 10)
            
      
    return new_sliding_door#,img_slding



def delete_door(img,single_door,double_door,sliding_door,delete_xy):
    new_img_door = copy.copy(img)
    new_img_door = cv.cvtColor(new_img_door, cv.COLOR_GRAY2RGB)
    new_single_door=delete_single_door(img,single_door,delete_xy)
    new_double_door=delete_double_door(img,double_door,delete_xy)
    new_sliding_door=delete_sliding_door(img,sliding_door,delete_xy)
    
    new_single_position=new_single_door.out_base_position()
    new_double_position=new_double_door.out_base_position()    
    new_sliding_position=new_sliding_door.out_base_position()

    for i in range(len(new_single_position)):
        if(new_single_position[i][1]==new_single_position[i][3]):#如果是水平主轴
            cv.rectangle(new_img_door,(min(new_single_position[i][0],new_single_position[i][2]),new_single_position[i][1]-new_single_position[i][4]),(max(new_single_position[i][0],new_single_position[i][2]),new_single_position[i][1]+new_single_position[i][5]),(255,0,0), 4)
        if(new_single_position[i][0]==new_single_position[i][2]):#如果是竖直主轴    
            cv.rectangle(new_img_door,(new_single_position[i][0]-new_single_position[i][4],min(new_single_position[i][1],new_single_position[i][3])),(new_single_position[i][0]+new_single_position[i][5],max(new_single_position[i][1],new_single_position[i][3])),(255,0,0), 4)
    
    for i in range(len(new_double_position)):       
        if(new_double_position[i][1]==new_double_position[i][3]):#如果是水平主轴
            cv.rectangle(new_img_door,(min(new_double_position[i][0],new_double_position[i][2]),new_double_position[i][1]-new_double_position[i][4]),(max(new_double_position[i][0],new_double_position[i][2]),new_double_position[i][1]+new_double_position[i][5]),(147,112,219), 4)
        if(new_double_position[i][0]==new_double_position[i][2]):#如果是竖直主轴    
            cv.rectangle(new_img_door,(new_double_position[i][0]-new_double_position[i][4],min(new_double_position[i][1],new_double_position[i][3])),(new_double_position[i][0]+new_double_position[i][5],max(new_double_position[i][1],new_double_position[i][3])),(147,112,219), 4)
            
    for i in range(len(new_sliding_position)):       
        if(new_sliding_position[i][1]==new_sliding_position[i][3]):#如果是水平主轴
            cv.rectangle(new_img_door,(min(new_sliding_position[i][0],new_sliding_position[i][2]),new_sliding_position[i][1]-new_sliding_position[i][4]),(max(new_sliding_position[i][0],new_sliding_position[i][2]),new_sliding_position[i][1]+new_sliding_position[i][5]),(37,193,255), 2)
        if(new_sliding_position[i][0]==new_sliding_position[i][2]):#如果是竖直主轴    
            cv.rectangle(new_img_door,(new_sliding_position[i][0]-new_sliding_position[i][4],min(new_sliding_position[i][1],new_sliding_position[i][3])),(new_sliding_position[i][0]+new_sliding_position[i][5],max(new_sliding_position[i][1],new_sliding_position[i][3])),(37,193,255), 2)

    return  new_single_door, new_double_door , new_sliding_door ,new_img_door
    