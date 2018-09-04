# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 15:39:02 2018

@author: fuzy
"""

from Wall import Nonbearing_wall
import cv2 as cv
import os
import numpy as np
from Wall import repoint
import random
from Datastruct import Data_struct
from Settings import Settings
max_area_wall_thre = Settings.max_area_wall_thre
wall_width_min = Settings.wall_width_min
wall_width_max_nonbear = Settings.wall_width_max_nonbear
wall_width_max_bear = Settings.wall_width_max_bear
seg_length_min = Settings.seg_length_min
def mkdir(path):
    path=path.strip()
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False
'''
nonb_contours:非承重墙轮廓
prop：比例尺
'''
def Divide_rect_for_nonbearwall(nonbearwall,prop):
    list_nonb = []
    nonb_contours = nonbearwall.out_contour()
    nonb_contours = repoint.remove_re_point(nonb_contours)
    for i in range(0,len(nonb_contours)):
        new_contour = nonb_contours[i].reshape(len(nonb_contours[i]),len(nonb_contours[i][0][0]))
        list_nonb.append(new_contour)
    wall_width_max = wall_width_max_nonbear
    list_wall=divide_rect_list(list_nonb,prop,wall_width_max)
    nonbearwall.add_wall_division(list_wall)
    #img = draw_rect(img,list_wall,list_door)
    return nonbearwall
'''
bear_contours:承重墙轮廓
prop：比例尺
'''
def Divide_rect_for_bearwall(bearwall,prop):
    bear_contours = bearwall.out_contour()
    #list_bear=Nonbearing_wall.condict(bear_contours,(300*prop)*(300*prop))
    bear_contours = repoint.remove_re_point(bear_contours)
    list_bear = []
    for i in range(0,len(bear_contours)):
        if cv.contourArea(bear_contours[i])>max_area_wall_thre:
            continue
        new_contour = bear_contours[i].reshape(len(bear_contours[i]),len(bear_contours[i][0][0]))
        list_bear.append(new_contour)
    wall_width_max = wall_width_max_bear
    #print(list_bear)
    list_wall=divide_rect_list(list_bear,prop,wall_width_max)
    #print(list_wall)
    bearwall.add_wall_division(list_wall)
    return bearwall
def divide_rect_list(list_wall_points,prop,wall_width_max):
    list_v_wall=[]
    list_h_wall=[]
    for i in range(len(list_wall_points)):
        vwall,hwall=divide_rect(list_wall_points[i].copy(),prop,wall_width_max)
        list_v_wall += vwall
        list_h_wall += hwall
    #print(list_v_wall)
    #print(list_h_wall)
    list_wall = list_v_wall + list_h_wall
    i = 0
    while i < len(list_wall) - 1:
        x1,x2,y1,y2 = coordinate(list_wall[i])
        if (x2-x1) < wall_width_min *prop and (y2-y1) < wall_width_min *prop:
            list_wall.pop(i)
            i = i - 1
            continue
        j = i + 1
        while j < len(list_wall):
            a1,a2,b1,b2 = coordinate(list_wall[j])
            area1 = (x2-x1)*(y2-y1)
            area2 = (a2-a1)*(b2-b1)
            inter1 = intersection(a1,a2,x1,x2)
            inter2 = intersection(b1,b2,y1,y2)
            inter_area = inter1*inter2
            if (inter_area)/np.minimum(area1,area2) > 0.9:
                if list_wall[i][0] == list_wall[i][2] and list_wall[j][0] == list_wall[j][2]:
                    if area1 >= area2:
                        list_wall.pop(j)
                        break
                    else:
                        list_wall.pop(i)
                        i = i - 1
                        break
#                    else:
#                        if y2 - y1 > x2 - x1:
#                            if list_wall[i][0] == list_wall[i][2]:
#                                list_wall.pop(j)
#                                break
#                            else:
#                                list_wall.pop(i)
#                                i = i - 1
#                                break
#                        else:
#                            if list_wall[i][0] == list_wall[i][2]:
#                                list_wall.pop(i)
#                                i = i - 1
#                                break
#                            else:
#                                list_wall.pop(j)
#                                break
                elif list_wall[i][1] == list_wall[i][3] and list_wall[j][1] == list_wall[j][3]:
                    if area1 >= area2:
                        list_wall.pop(j)
                        break
                    else:
                        list_wall.pop(i)
                        i = i - 1
                        break
                else:
                    flag1 = check_near_wall(list_wall[i],list_wall.copy())
                    flag2 = check_near_wall(list_wall[j],list_wall.copy())
                    #print('ha')
                    #print(list_wall[i])
                    #print(list_wall[j])
                    #print(flag1,flag2)
                    if flag1 and flag2 == False:
                        list_wall.pop(j)
                        break
                    elif flag2 and flag1 == False:
                        list_wall.pop(i)
                        i = i - 1
                        break
                    else:
                        if area1 >= 1.2 * area2:
                            list_wall.pop(j)
                            break
                        elif area2 >= 1.2* area1:
                            list_wall.pop(i)
                            i = i - 1
                            break
                        else:
                            if y2 - y1 > x2 - x1:
                                if list_wall[i][0] == list_wall[i][2]:
                                    list_wall.pop(j)
                                    break
                                else:
                                    list_wall.pop(i)
                                    i = i - 1
                                    break
                            else:
                                if list_wall[i][0] == list_wall[i][2]:
                                    list_wall.pop(i)
                                    i = i - 1
                                    break
                                else:
                                    list_wall.pop(j)
                                    break
            j = j + 1
        i = i + 1
                
#    print(list_v_wall,list_h_wall)
#    list_v_wall,list_h_wall = modify_middle(list_v_wall,list_h_wall)
#    list_v_wall,list_h_wall = get_inter_point(list_v_wall,list_h_wall)
#    i = 0
#    while i < len(list_v_wall):
#        x1,x2,y1,y2 = coordinate(list_v_wall[i])
#        if np.abs(y1-y2) < wall_width_min * prop:
#            list_v_wall.remove(list_v_wall[i])
#            i = i -1
#        i = i + 1
#    i = 0
#    while i < len(list_h_wall):
#        x1,x2,y1,y2 = coordinate(list_h_wall[i])
#        if np.abs(x1-x2) < wall_width_min * prop:
#            list_h_wall.remove(list_h_wall[i])
#            i = i -1
#        i = i + 1
#    print(list_v_wall+list_h_wall)
    return list_wall
def check_near_wall(line1,lines):
    #flag = False
    lines.remove(line1)
    num = len(lines)
    for i in range(num):
        #x1,x2,y1,y2 = coordinate(lines[i])
        #a1,a2,b1,b2 = coordinate(lines[j])
        if line1[0] == line1[2] and lines[i][0] == lines[i][2]:
            flag1 = (lines[i][3] <= line1[3] and lines[i][3] >= line1[1]) or (line1[3] <= lines[i][3]and line1[3] >= lines[i][1])
            if np.abs(line1[0] - lines[i][0]) <= 1 and flag1:
                return True
        elif line1[1] == line1[3] and lines[i][1] == lines[i][3]:
            flag1 = (lines[i][2] <= line1[2] and lines[i][2] >= line1[0]) or (line1[2] <= lines[i][2]and line1[2] >= lines[i][0])
            if np.abs(line1[1] - lines[i][3]) <= 1 and flag1:
                return True
    return False
def distance(a,b):
    return np.maximum(np.abs(a[0]-b[0]),np.abs(a[1]-b[1]))
def get_line_coordinate(points):
    vline = []
    hline = []
    num1 = len(points)
    for i in range(num1):
        j1 = (i-1)%num1
        j2 = (i+2)%num1
        if distance(points[i],points[j1]) <= 2:
            j1 = (i-2)%num1
        if distance(points[(i+1)%num1],points[j2]) <= 2:
            j2 = (i+3)%num1
        if np.abs(points[i][0]-points[(i+1)%num1][0])<=3 and np.abs(points[i][1]-points[(i+1)%num1][1])>=seg_length_min:
            if points[i][1] < points[(i+1)%num1][1]:
                if points[j1][0] < points[i][0] and points[j2][0] < points[(i+1)%num1][0]:
                    vline.append((points[i][0],points[i][1],points[i][0],points[(i+1)%num1][1],0,0))
                elif points[j1][0] > points[i][0] and points[j2][0] < points[(i+1)%num1][0]:
                    vline.append((points[i][0],points[i][1],points[i][0],points[(i+1)%num1][1],1,0))
                elif points[j1][0] < points[i][0] and points[j2][0] > points[(i+1)%num1][0]:
                    vline.append((points[i][0],points[i][1],points[i][0],points[(i+1)%num1][1],0,1))
                else:
                    vline.append((points[i][0],points[i][1],points[i][0],points[(i+1)%num1][1],1,1))
            else:
                if points[j1][0] < points[i][0] and points[j2][0] < points[(i+1)%num1][0]:
                    vline.append((points[i][0],points[(i+1)%num1][1],points[i][0],points[i][1],0,0))
                elif points[j1][0] > points[i][0] and points[j2][0] < points[(i+1)%num1][0]:
                    vline.append((points[i][0],points[(i+1)%num1][1],points[i][0],points[i][1],0,1))
                elif points[j1][0] < points[i][0] and points[j2][0] > points[(i+1)%num1][0]:
                    vline.append((points[i][0],points[(i+1)%num1][1],points[i][0],points[i][1],1,0))
                else:
                    vline.append((points[i][0],points[(i+1)%num1][1],points[i][0],points[i][1],1,1))
        elif np.abs(points[i][1] - points[(i+1)%num1][1])<=3 and np.abs(points[i][0]-points[(i+1)%num1][0])>=seg_length_min:
            if points[i][0] < points[(i+1)%num1][0]:
                if points[j1][1] < points[i][1] and points[j2][1] < points[(i+1)%num1][1]:
                    hline.append((points[i][0],points[i][1],points[(i+1)%num1][0],points[i][1],0,0))
                elif points[j1][1] > points[i][1] and points[j2][1] < points[(i+1)%num1][1]:
                    hline.append((points[i][0],points[i][1],points[(i+1)%num1][0],points[i][1],1,0))
                elif points[j1][1] < points[i][1] and points[j2][1] > points[(i+1)%num1][1]:
                    hline.append((points[i][0],points[i][1],points[(i+1)%num1][0],points[i][1],0,1))
                else:
                    hline.append((points[i][0],points[i][1],points[(i+1)%num1][0],points[i][1],1,1))
            else:
                if points[j1][1] < points[i][1] and points[j2][1] < points[(i+1)%num1][1]:
                    hline.append((points[(i+1)%num1][0],points[i][1],points[i][0],points[i][1],0,0))
                elif points[j1][1] > points[i][1] and points[j2][1] < points[(i+1)%num1][1]:
                    hline.append((points[(i+1)%num1][0],points[i][1],points[i][0],points[i][1],0,1))
                elif points[j1][1] < points[i][1] and points[j2][1] > points[(i+1)%num1][1]:
                    hline.append((points[(i+1)%num1][0],points[i][1],points[i][0],points[i][1],1,0))
                else:
                    hline.append((points[(i+1)%num1][0],points[i][1],points[i][0],points[i][1],1,1))
    return vline,hline

def intersection(a1,a2,b1,b2):
    temp1 = np.maximum(a1,b1)
    temp2 = np.minimum(a2,b2)
    return np.maximum(temp2-temp1,0)
def bubbleSort(a,b):
    for i in range(len(b)-1):
        for j in range(len(b)-i-1):
            if b[j] > b[j+1]:
                b[j], b[j+1] = b[j+1], b[j]
                a[j], a[j+1] = a[j+1], a[j]
    return a
def direction(line1,line2):
    flag1 = 0
    flag2 = 0
    if line1[0] == line1[2]:
        if line1[0] > line2[0]:
            temp = line1
            line1 = line2
            line2 = temp
        if np.abs(line1[1]-line2[1])<=3 and line1[4] == 1 and line2[4] == 0:
            flag1 = 1
        if np.abs(line1[3]-line2[3])<=3 and line1[5] == 1 and line2[5] == 0:
            flag2 = 1
    else:
        if line1[1] > line2[1]:
            temp = line1
            line1 = line2
            line2 = temp
        if np.abs(line1[0]-line2[0])<=3 and line1[4] == 1 and line2[4] == 0:
            flag1 = 1
        if np.abs(line1[2]-line2[2]) <= 3 and line1[5] == 1 and line2[5] == 0:
            flag2 = 1
    if flag1 == 1:
        if flag2 == 1:
            return 3
        else:
            return 1
    else:
        if flag2 == 1:
            return 2
        else:
            return 0

def vline_boundary(line1,line2,init_hline,init_vline,wall_width_max,prop):
    line = [line1,line2]
    top = 0 if line1[1] < line2[1] else 1
    bottom = 0 if line1[3] < line2[3] else 1
    left = 0 if line1[0]<line2[0] else 1
    num1 = len(init_vline)
    num2 = len(init_hline)
    miny = line[top][1]
    maxy = line[1-bottom][3]
    if np.abs(line1[1]-line2[1])<=3:
        if line[left][4] == 1 or line[1-left][4] == 0:
            miny = line[top][1]
        else:
            flag = True
            for i in range(0,num1):
                dis1 = line[1-top][1] - init_vline[i][3]
                dis2 = np.abs(line[top][0] - init_vline[i][0])
                dis3 = np.abs(line[1-top][0] - init_vline[i][0])
                if dis1/prop > wall_width_min and dis1/prop < wall_width_max:
                    if dis2/prop > wall_width_min and dis2/prop < wall_width_max:
                        miny = init_vline[i][3]
                        flag = False
                        break
                    if dis3/prop > wall_width_min and dis3/prop < wall_width_max:
                        miny = init_vline[i][3]
                        flag = False
                        break
            if flag:
                for i in range(0,num2):
                    dis1 = line[1-top][1] - init_hline[i][3]
                    inter = intersection(line[left][0],line[1-left][0],init_hline[i][0],init_hline[i][2])
                    if dis1/prop > wall_width_min and dis1/prop < wall_width_max:
                        if np.abs(inter - (line[1-left][0] -line[left][0])) <= 2:
                            miny = init_hline[i][3]
                            break
    elif np.abs(line1[1]-line2[1])/prop >= wall_width_max:
        miny = line[1-top][1]
        for i in range(0,num1):
            dis1 = line[1-top][1] - init_vline[i][3]
            dis2 = np.abs(line[top][0] - init_vline[i][0])
            if dis1 >= -2 and dis1/prop < wall_width_max:
                if dis2/prop > wall_width_min and dis2/prop < wall_width_max:
                    miny = init_vline[i][3]
                    break
    elif np.abs(line1[1]-line2[1])/prop > wall_width_min:
        #if np.abs(line1[4] - line2[4]) == 0:
            #miny = line[top][1]
        #else:
        flag = True
        for i in range(0,num1):
            dis1 = line[1-top][1] - init_vline[i][3]
            dis2 = np.abs(line[top][0] - init_vline[i][0])
            dis3 = np.abs(line[1-top][0] - init_vline[i][0])
            if dis1/prop > wall_width_min and dis1/prop < wall_width_max:
                if dis2/prop > wall_width_min and dis2/prop < wall_width_max:
                    miny = init_vline[i][3]
                    flag = False
                    break
                if dis3/prop > wall_width_min and dis3/prop < wall_width_max:
                    miny = init_vline[i][3]
                    flag = False
                    break
        if flag:
            for i in range(0,num2):
                dis1 = line[1-top][1] - init_hline[i][3]
                inter = intersection(line[left][0],line[1-left][0],init_hline[i][0],init_hline[i][2])
                if dis1/prop > wall_width_min and dis1/prop < wall_width_max:
                    if np.abs(inter - (line[1-left][0] -line[left][0])) <= 2:
                        miny = init_hline[i][3]
                        break
                        
    if np.abs(line1[3]-line2[3])<=2:
        if line[left][5] == 1 or line[1-left][5] == 0:
            maxy = line[1-bottom][3]
        else:
            flag = True
            for i in range(0,num1):
                dis1 = init_vline[i][1] - line[bottom][3]
                dis2 = np.abs(line[1-bottom][0] - init_vline[i][0])
                dis3 = np.abs(line[bottom][0] - init_vline[i][0])
                if dis1/prop > wall_width_min and dis1/prop < wall_width_max:
                    if dis2/prop > wall_width_min and dis2/prop < wall_width_max:
                        maxy = init_vline[i][1]
                        flag = False
                        break
                    if dis3/prop > wall_width_min and dis3/prop < wall_width_max:
                        maxy = init_vline[i][1]
                        flag = False
                        break
            if flag:
                for i in range(0,num2):
                    dis1 = init_hline[i][3] - line[bottom][3]
                    inter = intersection(line[left][0],line[1-left][0],init_hline[i][0],init_hline[i][2])
                    if dis1/prop > wall_width_min and dis1/prop < wall_width_max:
                        if np.abs(inter - (line[1-left][0] -line[left][0] )) <= 2:
                            maxy = init_hline[i][1]
                            break
    elif np.abs(line1[3]-line2[3])/prop >= wall_width_max:
        maxy = line[bottom][3]
        for i in range(0,num1):
            dis1 = init_vline[i][1] - line[bottom][3]
            dis2 = np.abs(line[1-bottom][0] - init_vline[i][0])
            if dis1 >= -2 and dis1/prop < wall_width_max:
                if dis2/prop > wall_width_min and dis2/prop < wall_width_max:
                    maxy = init_vline[i][1]
                    break
    elif np.abs(line1[3]-line2[3])/prop > wall_width_min:
        #if np.abs(line1[5] - line2[5]) == 0:
            #maxy = line[1-bottom][3]
        #else:
        flag = True
        for i in range(0,num1):
            dis1 = init_vline[i][1] - line[bottom][3]
            dis2 = np.abs(line[1-bottom][0] - init_vline[i][0])
            dis3 = np.abs(line[bottom][0] - init_vline[i][0])
            if dis1/prop > wall_width_min and dis1/prop < wall_width_max:
                if dis2/prop > wall_width_min and dis2/prop < wall_width_max:
                    maxy = init_vline[i][1]
                    flag = False
                    break
                if dis3/prop > wall_width_min and dis3/prop < wall_width_max:
                    maxy = init_vline[i][1]
                    flag = False
                    break
        if flag:
            for i in range(0,num2):
                dis1 = init_hline[i][3] - line[bottom][3]
                inter = intersection(line[left][0],line[1-left][0],init_hline[i][0],init_hline[i][2])
                if dis1/prop > wall_width_min and dis1/prop < wall_width_max:
                    if np.abs(inter - (line[1-left][0] -line[left][0] )) <= 2:
                        maxy = init_hline[i][1]
                        break
    dis = np.abs(line[1-left][0] - line[left][0])
    direct = direction(line1,line2)
    res = (line[left][0]+int(dis/2),miny,line[left][0]+int(dis/2),maxy,int(dis/2),dis-int(dis/2),direct)
    return res
def hline_boundary(line1,line2,init_hline,init_vline,wall_width_max,prop):
    line = [line1,line2]
    left = 0 if line1[0] < line2[0] else 1
    right = 0 if line1[2] < line2[2] else 1
    top = 0 if line1[1]<line2[1] else 1
    num1 = len(init_vline)
    num2 = len(init_hline)
    minx = line[left][0]
    maxx = line[1-right][2]
    if np.abs(line1[0]-line2[0])<=2:
        if line[top][4] == 1 or line[1-top][4] == 0:
            minx = line[left][0]
        else:
            flag = True
            for i in range(0,num2):
                dis1 = line[1-left][0] - init_hline[i][2]
                dis2 = np.abs(line[left][1] - init_hline[i][1])
                dis3 = np.abs(line[1-left][1] - init_hline[i][1])
                if dis1/prop > wall_width_min and dis1/prop < wall_width_max:
                    if dis2/prop > wall_width_min and dis2/prop < wall_width_max:
                        minx = init_hline[i][2]
                        flag = False
                        break
                    if dis3/prop > wall_width_min and dis3/prop < wall_width_max:
                        minx = init_hline[i][2]
                        flag = False
                        break
            if flag:
                for i in range(0,num1):
                    dis1 = line[1-left][0] - init_vline[i][0]
                    inter = intersection(line[top][1],line[1-top][1],init_vline[i][1],init_vline[i][3])
                    if dis1/prop > wall_width_min and dis1/prop < wall_width_max:
                        if np.abs(inter - (line[1-top][1] -line[top][1])) <= 2:
                            minx = init_vline[i][0]
                            break
    elif np.abs(line1[0]-line2[0])/prop >= wall_width_max:
        minx = line[1-left][0]
        for i in range(0,num2):
            dis1 = line[1-left][0] - init_hline[i][2]
            dis2 = np.abs(line[left][1] - init_hline[i][1])
            if dis1 >=-2 and dis1/prop < wall_width_max:
                if dis2/prop > wall_width_min and dis2/prop < wall_width_max:
                    minx = init_hline[i][2]
                    break
    elif np.abs(line1[0]-line2[0])/prop > wall_width_min:
        #if np.abs(line1[4] - line2[4]) == 0:
            #minx = line[left][0]
        #else:
        flag = True
        for i in range(0,num2):
            dis1 = line[1-left][0] - init_hline[i][2]
            dis2 = np.abs(line[left][1] - init_hline[i][1])
            dis3 = np.abs(line[1-left][1] - init_hline[i][1])
            if dis1/prop > wall_width_min and dis1/prop < wall_width_max:
                if dis2/prop > wall_width_min and dis2/prop < wall_width_max:
                    minx = init_hline[i][2]
                    flag = False
                    break
                if dis3/prop > wall_width_min and dis3/prop < wall_width_max:
                    minx = init_hline[i][2]
                    flag = False
                    break
        if flag:
            for i in range(0,num1):
                dis1 = line[1-left][0] - init_vline[i][0]
                inter = intersection(line[top][1],line[1-top][1],init_vline[i][1],init_vline[i][3])
                if dis1/prop > wall_width_min and dis1/prop < wall_width_max:
                    if np.abs(inter - (line[1-top][1] -line[top][1])) <= 2:
                        minx = init_vline[i][0]
                        break
                        
    if np.abs(line1[2]-line2[2])<=2:
        if line[top][5] == 1 or line[1-top][5] == 0:
            maxx = line[1-right][2]
        else:
            flag = True
            for i in range(0,num2):
                dis1 = init_hline[i][0] - line[right][2]
                dis2 = np.abs(line[1-right][1] - init_hline[i][1])
                dis3 = np.abs(line[right][1] - init_hline[i][1])
                
                if dis1/prop > wall_width_min and dis1/prop < wall_width_max:
                    if dis2/prop > wall_width_min and dis2/prop < wall_width_max:
                        maxx = init_hline[i][0]
                        flag = False
                        break
                    if dis3/prop > wall_width_min and dis3/prop < wall_width_max:
                        maxx = init_hline[i][0]
                        flag = False
                        break
            if flag:
                for i in range(0,num1):
                    dis1 = init_vline[i][0] - line[right][2]
                    inter = intersection(line[top][1],line[1-top][1],init_vline[i][1],init_vline[i][3])
                    if dis1/prop > wall_width_min and dis1/prop < wall_width_max:
                        if np.abs(inter - (line[1-top][1] -line[top][1])) <= 2:
                            maxx = init_vline[i][0]
                            break
    elif np.abs(line1[2]-line2[2])/prop >= wall_width_max:
        maxx = line[right][2]
        for i in range(0,num2):
            dis1 = init_hline[i][0] - line[right][2]
            dis2 = np.abs(line[1-right][1] - init_hline[i][1])
            if dis1 > -2 and dis1/prop < wall_width_max:
                if dis2/prop > wall_width_min and dis2/prop < wall_width_max:
                    maxx = init_hline[i][0]
                    break
    elif np.abs(line1[2]-line2[2])/prop > wall_width_min:
        #if np.abs(line1[5] - line2[5]) == 0:
        #    maxx = line[1-right][2]
        #else:
        flag = True
        for i in range(0,num2):
            dis1 = init_hline[i][0] - line[right][2]
            dis2 = np.abs(line[1-right][1] - init_hline[i][1])
            dis3 = np.abs(line[right][1] - init_hline[i][1])
            if dis1/prop > wall_width_min and dis1/prop < wall_width_max:
                if dis2/prop > wall_width_min and dis2/prop < wall_width_max:
                    maxx = init_hline[i][0]
                    flag = False
                    break
                if dis3/prop > wall_width_min and dis3/prop < wall_width_max:
                    maxx = init_hline[i][0]
                    flag = False
                    break
        if flag:
            for i in range(0,num1):
                dis1 = init_vline[i][0] - line[right][2]
                inter = intersection(line[top][1],line[1-top][1],init_vline[i][1],init_vline[i][3])
                if dis1/prop > wall_width_min and dis1/prop < wall_width_max:
                    if np.abs(inter - (line[1-top][1] -line[top][1])) <= 2:
                        maxx = init_vline[i][0]
                        break
    dis = np.abs(line[1-top][1] - line[top][1])
    direct = direction(line1,line2)
    res = (minx,line[top][1]+int(dis/2),maxx,line[top][1]+int(dis/2),int(dis/2),dis-int(dis/2),direct)
    return res  
def segmentation_ovo(index,lines,init_vline,init_hline,wall_width_max,prop):
    if lines[0][0] == lines[0][2]:
        line1 = lines[0]
        line2 = lines[index]
        lines.remove(line1)
        lines.remove(line2)
        resline = vline_boundary(line1,line2,init_hline,init_vline,wall_width_max,prop)
        if resline[1] - line1[1] >= 2:
            lines.append((line1[0],line1[1],line1[0],resline[1],line1[4],-1))
        if resline[3] - line1[3] <= -2:
            lines.append((line1[0],resline[3],line1[0],line1[3],-1,line1[5]))
        if resline[1] - line2[1] >= 2:
            lines.append((line2[0],line2[1],line2[0],resline[1],line2[4],-1))
        if resline[3] - line2[3] <= -2:
            lines.append((line2[0],resline[3],line2[0],line2[3],-1,line2[5]))
    else:
        line1 = lines[0]
        line2 = lines[index]
        lines.remove(line1)
        lines.remove(line2)
        resline = hline_boundary(line1,line2,init_hline,init_vline,wall_width_max,prop)
        if resline[0] - line1[0] >= 2:
            lines.append((line1[0],line1[1],resline[0],line1[1],line1[4],-1))
        if resline[2] - line1[2] <= -2:
            lines.append((resline[2],line1[1],line1[2],line1[3],-1,line1[5]))
        if resline[0] - line2[0] >= 2:
            lines.append((line2[0],line2[1],resline[0],line2[1],line2[4],-1))
        if resline[2] - line2[2] <= -2:
            lines.append((resline[2],line2[1],line2[2],line2[3],-1,line2[5]))
    return resline,lines
def divide_rect(wall_points,prop,wall_width_max):
    init_vline,init_hline = get_line_coordinate(wall_points)
    #print('lines',init_vline,init_hline)
    list_vrect = []
    list_hrect = []
    vline = init_vline.copy()
    hline = init_hline.copy()
    #print(vline,hline)
    while len(vline) >= 2:
        num1 = len(vline)
        flag = True
        for i in range(1,num1):
                dis = np.abs(vline[0][0] - vline[i][0])
                if dis/prop > wall_width_min and dis/prop < wall_width_max:
                    inter_len = intersection(vline[i][1],vline[i][3],vline[0][1],vline[0][3])
                    if inter_len > 1:
                        rect,vline = segmentation_ovo(i,vline,init_vline,init_hline,wall_width_max,prop)
                        list_vrect.append(rect)
                        flag = False
                        break
        if flag:
            vline.remove(vline[0])
        
        
    while len(hline) >= 2:
        num2 = len(hline)
        flag = True
        for i in range(1,num2):
            dis = np.abs(hline[i][1] - hline[0][1])
            if dis/prop > wall_width_min and dis/prop < wall_width_max:
                inter_len = intersection(hline[i][0],hline[i][2],hline[0][0],hline[0][2])
                if inter_len > 1:
                    rect,hline = segmentation_ovo(i,hline,init_vline,init_hline,wall_width_max,prop)
                    list_hrect.append(rect)
                    flag = False
                    break
        if flag:
            hline.remove(hline[0])
    #print(list_vrect,list_hrect)        
    return list_vrect,list_hrect
def coordinate(middleline):
    if middleline[0] == middleline[2]:
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
def modify_middle(vwall,hwall):
    num1 = len(vwall)
    for i in range(num1):
        for j in range(i+1,num1):
            x1,x2,y1,y2 = coordinate(vwall[i])
            a1,a2,b1,b2 = coordinate(vwall[j])
            flag1 = np.abs(y1-b2) <= 3
            flag2 = np.abs(y2-b1) <= 3
            flag3 = (y1 >= b1 and y1 <= b2) or (y2 >= b1 and y2 <= b2)
            flag4 = (b1 >= y1 and b1 <= y2) or (b2 >= y1 and b2 <= y2)
            flag = (flag1 or flag2) or (flag3 or flag4)
            #print(flag and intersection(x1,x2,a1,a2) >= np.minimum(np.abs(x2-x1),np.abs(a2-a1)) - 3,vwall[i],vwall[j])
            if flag and intersection(x1,x2,a1,a2) >= np.minimum(np.abs(x2-x1),np.abs(a2-a1)) - 3:
                if np.abs(x2-x1) < np.abs(a2-a1):
                    vwall[j] = [vwall[i][0],vwall[j][1],vwall[i][0],vwall[j][3],vwall[i][0]-a1,a2-vwall[i][0],vwall[j][6]]
                else:
                    vwall[i] = [vwall[j][0],vwall[i][1],vwall[j][0],vwall[i][3],vwall[j][0]-x1,x2-vwall[j][0],vwall[i][6]]
                #print(vwall[i],vwall[j])
    num2 = len(hwall)
    for i in range(num2):
        for j in range(i+1,num2):
            x1,x2,y1,y2 = coordinate(hwall[i])
            a1,a2,b1,b2 = coordinate(hwall[j])
            flag1 = np.abs(x1-a2) <= 3
            flag2 = np.abs(x2-a1) <= 3
            flag3 = (x1>=a1 and x1<=a2) or (x2>=a1 and x2<=a2)
            flag4 = (a1>=x1 and a1<=x2) or (a2>=x1 and a2<=x2)
            flag = flag1 or flag2 or flag2 or flag4
            if flag and intersection(y1,y2,b1,b2) >= np.minimum(np.abs(y2-y1),np.abs(b2-b1)) - 3:
                if np.abs(y2-y1)<np.abs(b2-b1):
                    hwall[j] = [hwall[j][0],hwall[i][1],hwall[j][2],hwall[i][1],hwall[i][1]-b1,b2-hwall[i][1],hwall[j][6]]
                else:
                    hwall[i] = [hwall[i][0],hwall[j][1],hwall[i][2],hwall[j][1],hwall[j][1]-y1,y2-hwall[j][1],hwall[i][6]]
    #print(vwall,hwall)
    return vwall,hwall

def get_inter_point(vwall,hwall):
    num1 = len(vwall)
    num2 = len(hwall)
    for i in range(num1):
        for j in range(num2):
            x1,x2,y1,y2 = coordinate(vwall[i])
            a1,a2,b1,b2 = coordinate(hwall[j])
            #if intersection(x1,x2,a1,a2) >= np.abs(x2-x1) - 2 and intersection(y1,y2,b1,b2) >= np.abs(b2-b1) -2:
            flag1 = intersection(x1,x2,a1,a2) >= 1 or np.abs(x1-a2) <=2 or np.abs(x2-a1) <= 2 
            flag2 = intersection(y1,y2,b1,b2) >= 1 or np.abs(y1-b2) <=2 or np.abs(y2-b1) <= 2
            flag = flag1 and flag2
            if flag:
                #print(vwall[i],hwall[j])
                dis1 = np.abs(a1-x1)
                dis2 = np.abs(a2-x2)
                if a1 >= x1:#and a1 <= x2:
                    dis1 = 0
                if a2 <= x2:#a2 >= x1 and a2 <= x2:
                    dis2 = 0
                if dis2 >= dis1:
                    hwall[j] = [vwall[i][0],hwall[j][1],hwall[j][2],hwall[j][3],hwall[j][4],hwall[j][5],hwall[j][6]]
                else:
                    hwall[j] = [hwall[j][0],hwall[j][1],vwall[i][0],hwall[j][3],hwall[j][4],hwall[j][5],hwall[j][6]]
                dis1 = np.abs(b1-y1)
                dis2 = np.abs(b2-y2)
                if y1 >= b1:# and y1 <= b2:
                    dis1 = 0
                if y2 <= b2:#y2 >= b1 and y2 <= b2:
                    dis2 = 0
                if dis2 >= dis1:
                    vwall[i] = [vwall[i][0],hwall[j][1],vwall[i][2],vwall[i][3],vwall[i][4],vwall[i][5],vwall[i][6]]
                else:
                    vwall[i] = [vwall[i][0],vwall[i][1],vwall[i][2],hwall[j][1],vwall[i][4],vwall[i][5],vwall[i][6]]
    return vwall,hwall
def draw_rect(img,list_wall):
    img[0:len(img),0:len(img[0])] = 255
    #img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
    for i in range(0,len(list_wall)):
        if np.abs(list_wall[i][0] - list_wall[i][2])<=2:
            x1 = list_wall[i][0] - list_wall[i][4]
            y1 = list_wall[i][1]
            x2 = list_wall[i][2] + list_wall[i][5]
            y2 = list_wall[i][3]
            cv.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
        else:
            x1 = list_wall[i][0]
            y1 = list_wall[i][1] - list_wall[i][4]
            x2 = list_wall[i][2]
            y2 = list_wall[i][3] + list_wall[i][5]
            cv.rectangle(img,(x1,y1),(x2,y2),(255,0,0),2)
    return img  

def draw_contour(img,list_contour,prop):
    img[0:len(img),0:len(img[0])] = 255
    list_nonb=[]
    list_nonb = repoint.remove_re_point(list_contour)
    for i in range(0,len(list_nonb)):
        cv.drawContours(img, [list_nonb[i]], -1, (0,0,255),2)
        for j in range(len(list_nonb[i])):
            cv.drawContours(img, [list_nonb[i][j]], -1, (0,0,0),1)
    return img
if __name__ == "__main__":
    png_list = ["9"]#34
    #png_list = ["4","6", "8", "10", "14", "16", "20", "24", "28", "32", "34", "36", "38",
    #"42", "50", "52", "54", "56", "58", "60", "62", "64", "66", "68", "70", "72", "78", "80", "84",
    #"92", "94", "98"]
    for png in png_list:
        blank_room_filename = "test_pic/" + png + ".png"
        result_filename = "result_pic" + png
        out_filename = "result/"
        mkdir(out_filename)
        data = np.load(png+".npz")
        list_contours = data["arr_0"]
        prop = data["arr_1"]
        list_nonb = []
        print(prop)
        #list_bear=Nonbearing_wall.condict(list_contours,(300*prop)*(300*prop))
        print(list_contours.shape)
        list_contours = repoint.remove_re_point(list_contours)
        for i in range(0,len(list_contours)):
            new_contour = list_contours[i].reshape(len(list_contours[i]),len(list_contours[i][0][0]))
            list_nonb.append(new_contour)
        list_wall=divide_rect_list(list_nonb,prop,500)
        img = cv.imread(blank_room_filename, 0)
        img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
#        img[0:len(img),0:len(img[0])] = 255
        img = draw_rect(img,list_wall)
        #img = draw_contour(img,list_contours,prop)
        cv.imwrite(out_filename + png +"rect.png",img)