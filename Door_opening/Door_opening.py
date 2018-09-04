# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 13:51:43 2018

@author: fuzy
"""
import numpy as np
from Settings import Settings
door_width_min = Settings.door_width_min
wall_width_min = Settings.wall_width_min
def Get_door_opening(bearwall,nonbearwall,prop):
    bearwall_rect = bearwall.out_wall_division()
    nonbearwall_rect = nonbearwall.out_wall_division()
    #print('bear',bearwall_rect)
    #print('non',nonbearwall_rect)
#    bearwall_id = list(range(0,len1))
#    nonbearwall_id = list(range(len1,len1+len2))
    len1 = len(bearwall_rect)
    len2 = len(nonbearwall_rect)
    bearwall_id = []
    nonbearwall_id = []
    for i in range(0,len1+len2):
        if i < len1:
            bearwall_id.append(i)
        else:
            nonbearwall_id.append(i)
    num1 = len1
    num2 = len2
    max_id = len1 + len2
    #print(len1)
    #print(bearwall_rect)
    for i in range(0,len1):
        if np.abs(bearwall_rect[i][1] - bearwall_rect[i][3])<=2:
            num1 = i
            break
    for i in range(0,len2):
        if np.abs(nonbearwall_rect[i][1] - nonbearwall_rect[i][3])<=2:
            num2 = i
            break
    #print(num1,num2)
    vrect = bearwall_rect[0:num1] + nonbearwall_rect[0:num2]
    hrect = bearwall_rect[num1:] + nonbearwall_rect[num2:]
    vid = bearwall_id[0:num1] + nonbearwall_id[0:num2]
    hid = bearwall_id[num1:] + nonbearwall_id[num2:]
    door_opening,door_opening_id,bearwall_id,nonbearwall_id,bearwall_rect,nonbearwall_rect = get_door_opening(vrect,hrect,vid,hid,prop,num1,len1-num1)
    #print(bearwall_rect,nonbearwall_rect)
    len1 = len(bearwall_rect)
    len2 = len(nonbearwall_rect)
    num1 = len1
    num2 = len2
    for i in range(0,len1):
        if np.abs(bearwall_rect[i][1] - bearwall_rect[i][3])<=2:
            num1 = i
            break
    for i in range(0,len2):
        if np.abs(nonbearwall_rect[i][1] - nonbearwall_rect[i][3])<=2:
            num2 = i
            break
    vid = bearwall_id[0:num1]
    hid = bearwall_id[num1:]
    list_v_wall,list_h_wall = modify_middle(bearwall_rect[0:num1],bearwall_rect[num1:])
    list_v_wall,list_h_wall,vid,hid,max_id = get_inter_point(list_v_wall,list_h_wall,prop,vid,hid,max_id)
#    vid = bearwall_id[0:num1]
#    hid = bearwall_id[num1:]
#    i = 0
#    while i < len(list_v_wall):
#        x1,x2,y1,y2 = coordinate(list_v_wall[i])
#        if np.abs(y1-y2) < wall_width_min * prop:
#            list_v_wall.remove(list_v_wall[i])
#            vid.remove(vid[i])
#            i = i -1
#        i = i + 1
#    i = 0
#    while i < len(list_h_wall):
#        x1,x2,y1,y2 = coordinate(list_h_wall[i])
#        if np.abs(x1-x2) < wall_width_min * prop:
#            list_h_wall.remove(list_h_wall[i])
#            hid.remove(hid[i])
#            i = i -1
#        i = i + 1
    bearwall_id = vid + hid
    bearwall_rect = list_v_wall + list_h_wall
    vid = nonbearwall_id[0:num2]
    hid = nonbearwall_id[num2:]
    list_v_wall,list_h_wall = modify_middle(nonbearwall_rect[0:num2],nonbearwall_rect[num2:])
    list_v_wall,list_h_wall,vid,hid,max_id = get_inter_point(list_v_wall,list_h_wall,prop,vid,hid,max_id)
#    vid = nonbearwall_id[0:num2]
#    hid = nonbearwall_id[num2:]
#    i = 0
#    while i < len(list_v_wall):
#        x1,x2,y1,y2 = coordinate(list_v_wall[i])
#        if np.abs(y1-y2) < wall_width_min * prop:
#            list_v_wall.remove(list_v_wall[i])
#            vid.remove(vid[i])
#            i = i -1
#        i = i + 1
#    i = 0
#    while i < len(list_h_wall):
#        x1,x2,y1,y2 = coordinate(list_h_wall[i])
#        if np.abs(x1-x2) < wall_width_min * prop:
#            list_h_wall.remove(list_h_wall[i])
#            hid.remove(hid[i])
#            i = i -1
#        i = i + 1
    nonbearwall_rect = list_v_wall + list_h_wall
    nonbearwall_id = vid + hid
    
    bearwall.add_wall_id(bearwall_id)
    nonbearwall.add_wall_id(nonbearwall_id)
    for i in range(0,len(bearwall_rect)):
        bearwall_rect[i] = bearwall_rect[i][0:6]
    for i in range(0,len(nonbearwall_rect)):
        nonbearwall_rect[i] = nonbearwall_rect[i][0:6]
    
    bearwall.add_wall_division(bearwall_rect)
    nonbearwall.add_wall_division(nonbearwall_rect)
    return door_opening,door_opening_id,bearwall,nonbearwall
def modify_middle(vwall,hwall):
    #print(vwall)
    num1 = len(vwall)
    for i in range(num1):
        for j in range(i+1,num1):
            #print(vwall[i],vwall[j])
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
                    vwall[j] = (vwall[i][0],vwall[j][1],vwall[i][0],vwall[j][3],vwall[i][0]-a1,a2-vwall[i][0])
                else:
                    vwall[i] = (vwall[j][0],vwall[i][1],vwall[j][0],vwall[i][3],vwall[j][0]-x1,x2-vwall[j][0])                #print(vwall[i],vwall[j])
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
                    hwall[j] = (hwall[j][0],hwall[i][1],hwall[j][2],hwall[i][1],hwall[i][1]-b1,b2-hwall[i][1])
                else:
                    hwall[i] = (hwall[i][0],hwall[j][1],hwall[i][2],hwall[j][1],hwall[j][1]-y1,y2-hwall[j][1])
    #print(vwall,hwall)
    return vwall,hwall

def get_inter_point(vwall,hwall,prop,vid,hid,max_id):
    i = 0
    while i < len(vwall):
        j = 0
        for j in range(len(hwall)):
            #print(i,j)
            x1,x2,y1,y2 = coordinate(vwall[i])
            a1,a2,b1,b2 = coordinate(hwall[j])
            #print('yi')
            #print(x1,x2,y1,y2)
            #print(a1,a2,b1,b2)
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
                if dis1 > wall_width_min * prop and dis2 > wall_width_min * prop:
                    hwall.append((hwall[j][0],hwall[j][1],vwall[i][0],hwall[j][3],hwall[j][4],hwall[j][5]))
                    hwall[j] = (vwall[i][0],hwall[j][1],hwall[j][2],hwall[j][3],hwall[j][4],hwall[j][5])
                    #print(hwall[-1])
                    hid.append(max_id)
                    max_id = max_id + 1
                elif dis2 >= dis1:
                    hwall[j] = (vwall[i][0],hwall[j][1],hwall[j][2],hwall[j][3],hwall[j][4],hwall[j][5])
                else:
                    hwall[j] = (hwall[j][0],hwall[j][1],vwall[i][0],hwall[j][3],hwall[j][4],hwall[j][5])
                    #print(hwall[j])
                dis1 = np.abs(b1-y1)
                dis2 = np.abs(b2-y2)
                if y1 >= b1:# and y1 <= b2:
                    dis1 = 0
                if y2 <= b2:#y2 >= b1 and y2 <= b2:
                    dis2 = 0
                if dis1 > wall_width_min * prop and dis2 > wall_width_min * prop:
                    vwall.append((vwall[i][0],vwall[i][1],vwall[i][2],hwall[j][1],vwall[i][4],vwall[i][5]))
                    vwall[i] = (vwall[i][0],hwall[j][1],vwall[i][2],vwall[i][3],vwall[i][4],vwall[i][5])
                    #print(vwall[-1])
                    vid.append(max_id)
                    max_id = max_id + 1
                elif dis2 >= dis1:
                    vwall[i] = (vwall[i][0],hwall[j][1],vwall[i][2],vwall[i][3],vwall[i][4],vwall[i][5])
                else:
                    vwall[i] = (vwall[i][0],vwall[i][1],vwall[i][2],hwall[j][1],vwall[i][4],vwall[i][5])
                #print(vwall[i])
            #j = j + 1
        i = i + 1
    return vwall,hwall,vid,hid,max_id
def is_cross(line1,line2):
    if line2[0] == line2[2]:
        temp = line1
        line1 = line2
        line2 = temp
    if line1[0] <= line2[2] and line1[0] >= line2[0]:
        if line2[1] <= line1[3] and line2[1] >= line1[1]:
            return True
    return False
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
def intersection(a1,a2,b1,b2):
    temp1 = np.maximum(a1,b1)
    temp2 = np.minimum(a2,b2)
    return np.maximum(temp2-temp1,0)
def is_door_opening(middle_line,wall1,wall2,vwall,hwall):
    #print(wall1,wall2)
    #print(vwall)
    if wall1[0] == wall1[2]:
        vwall.remove(wall1)
    else:
        hwall.remove(wall1)
    if wall2[0] == wall2[2]:
        vwall.remove(wall2)
    else:
        hwall.remove(wall2)
    temp = 1
    if middle_line[0] == middle_line[2]:
        temp = 0
    flag = True
    for i in range(len(vwall)):
        if temp == 0:
            test_line = [vwall[i][0]-vwall[i][4],int((vwall[i][1]+vwall[i][3])/2),vwall[i][0]+vwall[i][5],int((vwall[i][1]+vwall[i][3])/2)]
        else:
            test_line = vwall[i][0:4]
        if is_cross(middle_line,test_line):
            flag = False
    for i in range(len(hwall)):
        if temp == 0:
            test_line = hwall[i][0:4]
        else:
            test_line = [int((hwall[i][0]+hwall[i][2])/2),hwall[i][1]-hwall[i][4],int((hwall[i][0]+hwall[i][2])/2),hwall[i][1]+hwall[i][5]]
        if is_cross(middle_line,test_line):
            flag = False
    return flag
def is_match(line1,line2,prop):
    x1,x2,y1,y2 = coordinate(line1)
    a1,a2,b1,b2 = coordinate(line2)
    if line1[0] == line1[2] and line2[0] == line2[2]:
        if intersection(x1,x2,a1,a2) >= np.minimum(np.abs(x2-x1),np.abs(a2-a1)) - 3:
            if line2[3] < line1[1]:
                dis = np.abs(line2[3] - line1[1])
                flag = line1[6] == 1 or line1[6] == 3 or line2[6] == 2 or line2[6] == 3
                if dis/prop > door_width_min and flag:
                    if np.abs(x2-x1) <= np.abs(a2 -a1):
                        res = (line1[0],line2[3],line1[0],line1[1],line1[4],line1[5])
                    else:
                        res = (line2[0],line2[3],line2[0],line1[1],line2[4],line2[5])
                    if np.abs(x1-a1) <= 3 and np.abs(x2-a2) <= 3:
                        flag1 = line2[6] == 1 or line2[6] == 3
                        flag2 = line1[6] == 2 or line1[6] == 3
                        if flag1 == True:
                            if flag2 == True:
                                direct = 3
                            else:
                                direct = 1
                        else:
                            if flag2 == True:
                                direct = 2
                            else:
                                direct = 0
                        wallcombine = (line1[0],line2[1],line1[2],line1[3],line1[4],line1[5],direct)
                        return res,wallcombine
                    else:
                        return res,-1
            elif line1[3] < line2[1]:
                dis = np.abs(line1[3] - line2[1])
                flag = line1[6] == 2 or line1[6] == 3 or line2[6] == 1 or line2[6] == 3
                if dis/prop > door_width_min and flag:
                    if np.abs(x2-x1) <= np.abs(a2 -a1):
                        res = (line1[0],line1[3],line1[0],line2[1],line1[4],line1[5])
                    else:
                        res = (line2[0],line1[3],line2[0],line2[1],line2[4],line2[5])
                    if np.abs(x1-a1) <= 3 and np.abs(x2-a2) <= 3:
                        flag2 = line2[6] == 2 or line2[6] == 3
                        flag1 = line1[6] == 1 or line1[6] == 3
                        if flag1 == True:
                            if flag2 == True:
                                direct = 3
                            else:
                                direct = 1
                        else:
                            if flag2 == True:
                                direct = 2
                            else:
                                direct = 0
                        wallcombine = (line1[0],line1[1],line1[2],line2[3],line1[4],line1[5],direct)
                        return res,wallcombine
                    else:
                        return res,-1
    elif line1[1] == line1[3] and line2[1] == line2[3]:
        if intersection(y1,y2,b1,b2) >= np.minimum(np.abs(y2-y1),np.abs(b2-b1)) - 3:
            if line2[2] < line1[0]:
                dis = np.abs(line2[2] - line1[0])
                flag = line1[6] == 1 or line1[6] == 3 or line2[6] == 2 or line2[6] == 3
                if dis/prop > door_width_min and flag:
                    if np.abs(y2-y1) <= np.abs(b2 -b1):
                        res =  (line2[2],line1[1],line1[0],line1[1],line1[4],line1[5])
                    else:
                        res = (line2[2],line2[1],line1[0],line2[1],line2[4],line2[5])
                    if np.abs(y1-b1) <=3 and np.abs(y2-b2) <= 3:
                        flag1 = line2[6] == 1 or line2[6] == 3
                        flag2 = line1[6] == 2 or line1[6] == 3
                        if flag1 == True:
                            if flag2 == True:
                                direct = 3
                            else:
                                direct = 1
                        else:
                            if flag2 == True:
                                direct = 2
                            else:
                                direct = 0
                        wallcombine = (line2[0],line1[1],line1[2],line1[3],line1[4],line1[5],direct)
                        return res,wallcombine
                    else:
                        return res,-1
            elif line1[2] < line2[0]:
                dis = np.abs(line1[2] - line2[0])
                flag = line1[6] == 2 or line1[6] == 3 or line2[6] == 1 or line2[6] == 3
                if dis/prop > door_width_min and flag:
                    if np.abs(y2-y1) <= np.abs(b2 -b1):
                        res = (line1[2],line1[1],line2[0],line1[1],line1[4],line1[5])
                    else:
                        res = (line1[2],line2[1],line2[0],line2[1],line2[4],line2[5])
                    if np.abs(y1-b1) <=3 and np.abs(y2-b2) <= 3:
                        flag2 = line2[6] == 2 or line2[6] == 3
                        flag1 = line1[6] == 1 or line1[6] == 3
                        if flag1 == True:
                            if flag2 == True:
                                direct = 3
                            else:
                                direct = 1
                        else:
                            if flag2 == True:
                                direct = 2
                            else:
                                direct = 0
                        wallcombine = (line1[0],line1[1],line2[2],line1[3],line1[4],line1[5],direct)
                        return res,wallcombine
                    else:
                        return res,-1
#    else:
#        if line1[0] == line1[2]:
#            temp = line1
#            line1 = line2
#            line2 = temp
#            x1,x2,y1,y2 = coordinate(line1)
#            a1,a2,b1,b2 = coordinate(line2)
#        if a2 < line1[0]:
#            if intersection(y1,y2,b1,b2) >= np.minimum(np.abs(y2-y1),np.abs(b2-b1)) - 3:
#                dis = np.abs(a2 - line1[0])
#                if dis/prop > door_width_min:
#                    return (a2,line1[1],line1[0],line1[3],line1[4],line1[5]),-1
#        elif a1 > line1[2]:
#            if intersection(y1,y2,b1,b2) >= np.minimum(np.abs(y2-y1),np.abs(b2-b1)) - 3:
#                dis = np.abs(a1 - line1[2])
#                if dis/prop > door_width_min:
#                    return (line1[2],line1[1],a1,line1[3],line1[4],line1[5]),-1
#        elif y2 < line2[1]:
#            if intersection(x1,x2,a1,a2) >= np.minimum(np.abs(x2-x1),np.abs(a2-a1)) - 3:
#                dis = np.abs(y2-line2[1])
#                if dis/prop > door_width_min:
#                    return (line2[0],y2,line2[2],line2[1],line2[4],line2[5]),-1
#        elif y1 > line2[3]:
#            if intersection(x1,x2,a1,a2) >= np.minimum(np.abs(x2-x1),np.abs(a2-a1)) - 3:
#                dis = np.abs(y1-line2[3])
#                if dis/prop > door_width_min:
#                    return (line2[0],line2[3],line2[2],y1,line2[4],line2[5]),-1
    return -1,-1
def get_door_opening(vwall,hwall,vid,hid,prop,num1,num2):
    door_opening = []
    door_id = []
    wall = vwall.copy() + hwall.copy()
    wallid = vid.copy() + hid.copy()
    num = len(vwall)
    #print(vwall,hwall)
    i = 0
    while i < len(wall):
        j = i+1
        while j < len(wall):
            doorop,wallcombine = is_match(wall[i],wall[j],prop)
            #print(i,j,wall[j])
            if doorop != -1:
                if is_door_opening(doorop,wall[i],wall[j],vwall.copy(),hwall.copy()):
                    door_opening.append(doorop)
                    door_id.append(wallid[i])
                    if wallcombine != -1:
                        if wall[i][0] == wall[i][2]:
                            vwall.remove(wall[i])
                            vwall.append(wallcombine)
                        else:
                            hwall.remove(wall[i])
                            hwall.append(wallcombine)
                        wall[i] = wallcombine
                        wall.pop(j)
                        wallid.pop(j)
                        j = j - 1
                #v_door_id.append(vid[i])
                        if j < num:
                            num = num - 1
                        if j < num1:
                            num1 = num1 - 1
                        if j >= num and j < num + num2:
                            num2 = num2 - 1
            j = j + 1
        i = i + 1
    vwall = wall[0:num]
    hwall = wall[num:]
    vid = wallid[0:num]
    hid = wallid[num:]
    bearwall_id = vid[0:num1] + hid[0:num2]
    nonbearwall_id = vid[num1:] + hid[num2:]
    bearwall_rect = vwall[0:num1] + hwall[0:num2]
    nonbearwall_rect = vwall[num1:] + hwall[num2:]
    return door_opening,door_id,bearwall_id,nonbearwall_id,bearwall_rect,nonbearwall_rect
