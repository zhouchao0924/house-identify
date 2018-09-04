# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 16:00:39 2018

@author: fuzy
"""

import numpy as np
import cv2 as cv
from Datastruct import Data_struct
from Door import Doors
from Settings import Settings
sliding_door_width_max = Settings.sliding_door_width_max
normal_door_width_max = Settings.normal_door_width_max
def intersection(a1,a2,b1,b2):
    temp1 = np.maximum(a1,b1)
    temp2 = np.minimum(a2,b2)
    return np.maximum(temp2-temp1,0)
def coor_dis(a1,a2,b1,b2):
    temp1 = np.maximum(a1,b1)
    temp2 = np.minimum(a2,b2)
    return np.maximum(temp1-temp2,0)
def distance(rect1,rect2):
    dis1 = coor_dis(rect1[0],rect1[2],rect2[0],rect2[2])
    dis2 = coor_dis(rect1[1],rect1[3],rect2[1],rect2[3])
    return np.sqrt(np.power(dis1,2) + np.power(dis2,2))
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
def union_single(door1,door2,prop):
    single_position_1 = door1.out_base_position()
    single_Xflip_1 = door1.out_Xflip()
    single_Yflip_1 = door1.out_Yflip()
    single_id_1 = door1.out_door_id()
    single_position_2 = door2.out_base_position()
    single_Xflip_2 = door2.out_Xflip()
    single_Yflip_2 = door2.out_Yflip()
    single_id_2 = door2.out_door_id()
    i = 0
    for i in range(len(single_position_2)):
        line1 = single_position_2[i]
        x1,x2,y1,y2 = coordinate(line1)
        flag = True
        for j in range(0,len(single_position_1)):
            a1,a2,b1,b2 = coordinate(single_position_1[j])
            area1 = (x2-x1)*(y2-y1)
            area2 = (a2-a1)*(b2-b1)
            inter1 = intersection(a1,a2,x1,x2)
            inter2 = intersection(b1,b2,y1,y2)
            inter_area = inter1*inter2
            dis = distance((x1,y1,x2,y2),(a1,b1,a2,b2))
            flag = (inter1/np.minimum(a2-a1,x2-x1) > 0.8 or inter2/np.minimum(b2-b1,y2-y1) > 0.8)
            if (inter_area)/np.minimum(area1,area2) > 0.45 or (dis < 4 and flag):#or np.maximum(x2-x1,y2-y1)/prop > normal_door_width_max:
                flag = False
                break
        if flag:
            single_position_1.append(single_position_2[i])
            single_Xflip_1.append(single_Xflip_2[i])
            single_Yflip_1.append(single_Yflip_2[i])
            single_id_1.append(single_id_2[i])
    door1.add_base_position(single_position_1)
    door1.add_Xflip(single_Xflip_1)
    door1.add_Yflip(single_Yflip_1)
    door1.add_door_id(single_id_1)
    return door1
def union_sliding(door1,door_opening,door_opening_id,prop):
    single_position = door1.out_base_position()
    single_Xflip = door1.out_Xflip()
    single_Yflip = door1.out_Yflip()
    single_id = door1.out_door_id()
    i = 0
    for i in range(len(door_opening)):
        line1 = door_opening[i]
        if line1[0] == line1[2]:
            flip = 1
        else:
            flip = 0
        x1,x2,y1,y2 = coordinate(line1)
        flag = True
        for j in range(0,len(single_position)):
            a1,a2,b1,b2 = coordinate(single_position[j])
            area1 = (x2-x1)*(y2-y1)
            area2 = (a2-a1)*(b2-b1)
            inter1 = intersection(a1,a2,x1,x2)
            inter2 = intersection(b1,b2,y1,y2)
            inter_area = inter1*inter2
            dis = distance((x1,y1,x2,y2),(a1,b1,a2,b2))
            flag = (inter1/np.minimum(a2-a1,x2-x1) > 0.8 or inter2/np.minimum(b2-b1,y2-y1) > 0.8)
            if (inter_area)/np.minimum(area1,area2) > 0.45 or (dis < 4 and flag) or np.maximum(x2-x1,y2-y1)/prop < normal_door_width_max or  np.maximum(x2-x1,y2-y1)/prop > sliding_door_width_max:
                flag = False
                break
        if flag:
            single_position.append(door_opening[i])
            single_Xflip.append(flip)
            single_Yflip.append(flip)
            single_id.append(door_opening_id[i])
    door1.add_base_position(single_position)
    door1.add_Xflip(single_Xflip)
    door1.add_Yflip(single_Yflip)
    door1.add_door_id(single_id)
    return door1
def remove_repetition_two_rect(mincc, minrr, maxcc, maxrr,door_opening,door_opening_id,prop):
    i = 0
    while i < len(door_opening):
        line1 = door_opening[i]
        x1,x2,y1,y2 = coordinate(line1)
        for j in range(0,len(mincc)):
            a1,a2,b1,b2 = mincc[j],maxcc[j],minrr[j],maxrr[j]
            area1 = (x2-x1)*(y2-y1)
            area2 = (a2-a1)*(b2-b1)
            inter1 = intersection(a1,a2,x1,x2)
            inter2 = intersection(b1,b2,y1,y2)
            inter_area = inter1*inter2
            dis = distance((x1,y1,x2,y2),(a1,b1,a2,b2))
            flag = (inter1/np.minimum(a2-a1,x2-x1) > 0.8 or inter2/np.minimum(b2-b1,y2-y1) > 0.8)
            if (inter_area)/np.minimum(area1,area2) > 0.45 or (dis < 5 and flag): #or np.maximum(x2-x1,y2-y1)/prop > normal_door_width_max:
                door_opening.remove(line1)
                door_opening_id.remove(door_opening_id[i])
                i = i-1
                break
        i = i+1
    return door_opening,door_opening_id
def remove_repetition_door(mincc, minrr, maxcc, maxrr,door):
    position = door.out_base_position()
    i = 0
    while i < len(mincc):
        #print(i,minrr)
        x1,x2,y1,y2 = mincc[i],maxcc[i],minrr[i],maxrr[i]
        for j in range(0,len(position)):
            a1,a2,b1,b2 = coordinate(position[j])
            area1 = (x2-x1)*(y2-y1)
            area2 = (a2-a1)*(b2-b1)
            inter1 = intersection(a1,a2,x1,x2)
            inter2 = intersection(b1,b2,y1,y2)
            inter_area = inter1*inter2
            dis = distance((x1,y1,x2,y2),(a1,b1,a2,b2))
            flag = (inter1/np.minimum(a2-a1,x2-x1) > 0.8 or inter2/np.minimum(b2-b1,y2-y1) > 0.8)
            if (inter_area)/np.minimum(area1,area2) > 0.45 or (dis < 5 and flag): #or np.maximum(x2-x1,y2-y1)/prop > normal_door_width_max:
                mincc.pop(i)
                minrr.pop(i)
                maxcc.pop(i)
                maxrr.pop(i)
                i = i - 1
                break
        i = i + 1
    return mincc,minrr,maxcc,maxrr
def remove_repetition(windows,door_opening,door_opening_id,prop):
    i = 0
    while i < len(door_opening):
        line1 = door_opening[i]
        x1,x2,y1,y2 = coordinate(line1)
        for j in range(0,len(windows)):
            a1,a2,b1,b2 = coordinate(windows[j])
            area1 = (x2-x1)*(y2-y1)
            area2 = (a2-a1)*(b2-b1)
            inter1 = intersection(a1,a2,x1,x2)
            inter2 = intersection(b1,b2,y1,y2)
            inter_area = inter1*inter2
            dis = distance((x1,y1,x2,y2),(a1,b1,a2,b2))
            flag = (inter1/np.minimum(a2-a1,x2-x1) > 0.8 or inter2/np.minimum(b2-b1,y2-y1) > 0.8)
            if (inter_area)/np.minimum(area1,area2) > 0.45 or (dis < 5 and flag): #or np.maximum(x2-x1,y2-y1)/prop > normal_door_width_max:
                door_opening.remove(line1)
                door_opening_id.remove(door_opening_id[i])
                i = i-1
                break
            #elif np.maximum(x2-x1,y2-y1)/prop > sliding_door_width_max:
             #   door_opening.remove(line1)
             #   door_opening_id.remove(door_opening_id[i])
             #   i = i-1
             #   break
        i = i+1
    return door_opening,door_opening_id
def Get_door(door_opening,door_opening_id,win_normal,prop,img , scale ,Wall_img,bear_wall,nonbearwall):
    windows = win_normal.out_base_position()
    single_door,double_door,sliding_door = Doors.Door_detect(img , scale ,Wall_img,bear_wall,nonbearwall)
    single_position = single_door.out_base_position()
    single_Xflip = single_door.out_Xflip()
    single_Yflip = single_door.out_Yflip()
    single_id = single_door.out_door_id()
    double_position = double_door.out_base_position()
    sliding_position = sliding_door.out_base_position()
    sliding_Xflip = sliding_door.out_Xflip()
    sliding_Yflip = sliding_door.out_Yflip()
    sliding_id = sliding_door.out_door_id()
    door_opening,door_opening_id = remove_repetition(windows,door_opening.copy(),door_opening_id.copy(),prop)
    door_opening,door_opening_id = remove_repetition(single_position,door_opening.copy(),door_opening_id.copy(),prop)
    door_opening,door_opening_id = remove_repetition(double_position,door_opening.copy(),door_opening_id.copy(),prop)
    door_opening,door_opening_id = remove_repetition(sliding_position,door_opening.copy(),door_opening_id.copy(),prop)
    for i in range(0,len(door_opening)):
        line1 = door_opening[i]
        x1,x2,y1,y2 = coordinate(line1)
        if np.maximum(x2-x1,y2-y1)/prop > normal_door_width_max:
            sliding_position.append(line1)
            sliding_Xflip.append(-1)
            sliding_Yflip.append(-1)
            sliding_id.append(door_opening_id[i])
        else:
            single_position.append(line1)
            single_Xflip.append(-1)
            single_Yflip.append(-1)

            single_id.append(door_opening_id[i])
    single_door.add_base_position(single_position)
    single_door.add_Xflip(single_Xflip)
    single_door.add_Yflip(single_Yflip)
    single_door.add_door_id(single_id)
    
    sliding_door.add_base_position(sliding_position)
    sliding_door.add_Xflip(sliding_Xflip)
    sliding_door.add_Yflip(sliding_Yflip)
    sliding_door.add_door_id(sliding_id)
    
    img_door=img.copy()
    img_door = cv.cvtColor(img_door, cv.COLOR_GRAY2RGB)
    
    single_position=single_door.out_base_position()
    double_position=double_door.out_base_position()    
    sliding_position=sliding_door.out_base_position() 
    
    for i in range(len(single_position)):
        if(single_position[i][1]==single_position[i][3]):#如果是水平主轴
            cv.rectangle(img_door,(min(single_position[i][0],single_position[i][2]),single_position[i][1]-single_position[i][4]),(max(single_position[i][0],single_position[i][2]),single_position[i][1]+single_position[i][5]),(255,0,0), 4)
        if(single_position[i][0]==single_position[i][2]):#如果是竖直主轴    
            cv.rectangle(img_door,(single_position[i][0]-single_position[i][4],min(single_position[i][1],single_position[i][3])),(single_position[i][0]+single_position[i][5],max(single_position[i][1],single_position[i][3])),(255,0,0), 4)
    
    for i in range(len(double_position)):       
        if(double_position[i][1]==double_position[i][3]):#如果是水平主轴
            cv.rectangle(img_door,(min(double_position[i][0],double_position[i][2]),double_position[i][1]-double_position[i][4]),(max(double_position[i][0],double_position[i][2]),double_position[i][1]+double_position[i][5]),(147,112,219), 4)
        if(double_position[i][0]==double_position[i][2]):#如果是竖直主轴    
            cv.rectangle(img_door,(double_position[i][0]-double_position[i][4],min(double_position[i][1],double_position[i][3])),(double_position[i][0]+double_position[i][5],max(double_position[i][1],double_position[i][3])),(147,112,219), 4)
            
    for i in range(len(sliding_position)):       
        if(sliding_position[i][1]==sliding_position[i][3]):#如果是水平主轴
            cv.rectangle(img_door,(min(sliding_position[i][0],sliding_position[i][2]),sliding_position[i][1]-sliding_position[i][4]),(max(sliding_position[i][0],sliding_position[i][2]),sliding_position[i][1]+sliding_position[i][5]),(37,193,255), 2)
        if(sliding_position[i][0]==sliding_position[i][2]):#如果是竖直主轴    
            cv.rectangle(img_door,(sliding_position[i][0]-sliding_position[i][4],min(sliding_position[i][1],sliding_position[i][3])),(sliding_position[i][0]+sliding_position[i][5],max(sliding_position[i][1],sliding_position[i][3])),(37,193,255), 2)
    
    return single_door,double_door,sliding_door,img_door
    