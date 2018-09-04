# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 15:34:47 2018

@author: fuzy
"""
import numpy as np
max_dis = 5
def coor_dis(a1,a2,b1,b2):
    temp1 = np.maximum(a1,b1)
    temp2 = np.minimum(a2,b2)
    return np.maximum(temp1-temp2,0)
#计算两个矩形的最近的两个点的L1距离
def distance(rect1,rect2):
    dis1 = coor_dis(rect1[0],rect1[2],rect2[0],rect2[2])
    dis2 = coor_dis(rect1[1],rect1[3],rect2[1],rect2[3])
    return np.sqrt(np.power(dis1,2) + np.power(dis2,2))
def consistency(rect1,rect2):
    inter1 = intersection(rect1[0],rect1[2],rect2[0],rect2[2])
    inter2 = intersection(rect1[1],rect1[3],rect2[1],rect2[3])
    return inter1 + inter2
def intersection(a1,a2,b1,b2):
    temp1 = np.maximum(a1,b1)
    temp2 = np.minimum(a2,b2)
    return np.maximum(temp2-temp1,0)
#由中轴线坐标和dis1，dis2计算矩形的左上点和右下点坐标
def get_coor(rect):
    if np.abs(rect[0] - rect[2])<=2:
        x1 = rect[0] - rect[4]
        y1 = rect[1]
        x2 = rect[2] + rect[5]
        y2 = rect[3]
    else:
        x1 = rect[0]
        y1 = rect[1] - rect[4]
        x2 = rect[2]
        y2 = rect[3] + rect[5]
    return (x1,y1,x2,y2)
def Get_owner_wall(position,bearwall,nonbearwall):
    bear_rect = bearwall.out_wall_division()
    nonbear_rect = nonbearwall.out_wall_division()
    bear_id = bearwall.out_wall_id()
    nonbear_id = nonbearwall.out_wall_id()
    #near_id = []
    if len(position) >=4:
        if position[0] > position[2]:
            temp = position[0]
            position[0] = position[2]
            position[2] = temp
        if position[1] > position[3]:
            temp = position[1]
            position[1] = position[3]
            position[3] = temp
    if len(position) == 6:
        position = get_coor(position)
    if len(position) == 2:
        position = (position[0],position[1],position[0],position[1])
    #dis = []
    consis = 0
    near_id = -1
    for i in range(0,len(bear_rect)):
        dis1 = distance(position,get_coor(bear_rect[i]))
        consis1 = consistency(position,get_coor(bear_rect[i]))
        if dis1 < max_dis:
            if consis1 > consis:
                consis = consis1
                near_id = bear_id[i]
            #dis.append(dis1)
            #near_id.append(bear_id[i])
    for i in range(0,len(nonbear_rect)):
        dis1 = distance(position,get_coor(nonbear_rect[i]))
        consis1 = consistency(position,get_coor(nonbear_rect[i]))
        if dis1 < max_dis:
            if consis1 > consis:
                consis = consis1
                near_id = nonbear_id[i]
            #dis.append(dis1)
            #near_id.append(nonbear_id[i])
    return near_id
if __name__ == "__main__":
    rect1 = (0,0,3,4)
    rect2 = (4,2,8,3)
    print(distance(rect1,rect2))