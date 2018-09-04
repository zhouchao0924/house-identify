# -*- coding: utf-8 -*-
"""
Created on Wed Aug 08 09:37:06 2018

@author: 王科涛
"""

import cv2 as cv
from skimage import measure

from Settings import Settings


def rect_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    disx = abs((x1 + x2)/2 - (x3 + x4)/2)
    disy = abs((y1 + y2)/2 - (y3 + y4)/2)
    bianx = (x2 - x1)/2 + (x4 - x3)/2
    biany = (y2 - y1)/2 + (y4 - y3)/2
    if disx < bianx and disy < biany:
        return 1
    else:
        return 0


def judge_remove_door(mincc_two, minrr_two, maxcc_two, maxrr_two, singledoor_mincc, singledoor_minrr, singledoor_maxcc, singledoor_maxrr):
    m = len(mincc_two)
    n = len(singledoor_mincc)

    mincc = []
    minrr = []
    maxcc = []
    maxrr = []    
    for i in range(m):
        judge = 1
        for j in range(n):
            if rect_intersect(mincc_two[i], minrr_two[i], maxcc_two[i], maxrr_two[i], singledoor_mincc[j], singledoor_minrr[j], singledoor_maxcc[j], singledoor_maxrr[j]) == 1:
                judge = 0
                break
        if judge == 1:
            mincc.append(mincc_two[i])
            minrr.append(minrr_two[i])
            maxcc.append(maxcc_two[i])
            maxrr.append(maxrr_two[i])
    
    return mincc, minrr, maxcc, maxrr
    


'''
min_thre 外接矩形最小阈值
max_area 外接矩形和实际面积最大差距
'''
def get_rect_corner_position(img, scale, min_thre, max_area):
    label_image=measure.label(img, connectivity = 2)  #8连通区域标记
    minrr=[]
    mincc=[]
    maxrr=[]
    maxcc=[]
    for region in measure.regionprops(label_image): 
        #忽略小区域
        area_2 = region.area * scale * scale
        if area_2 < min_thre:
            continue
        minr, minc, maxr, maxc = region.bbox
        area_1 = (maxr - minr) * (maxc - minc) * scale * scale
        if abs(area_1 - area_2) > max_area:
            continue
        
        minrr.append(minr)
        mincc.append(minc)
        maxrr.append(maxr)
        maxcc.append(maxc)
    m = len(minrr)
    img = cv.cvtColor(img.copy(), cv.COLOR_GRAY2RGB)
#    print(m)
    for i in range(m):
        cv.rectangle(img, (mincc[i],minrr[i]), (maxcc[i],maxrr[i]), (0,0,255), 1) 
#    cv.imwrite('juxing.jpg', img)
    return mincc, minrr, maxcc, maxrr
    
    
'''
min_thre 外接矩形最小阈值
max_area 外接矩形和实际面积最大差距百分比
'''
def get_piao_corner_position(img, scale, min_thre, max_area):
    label_image=measure.label(img, connectivity = 2)  #8连通区域标记
    minrr=[]#y坐标
    mincc=[]#x坐标
    maxrr=[]#y坐标
    maxcc=[]#x坐标
    for region in measure.regionprops(label_image): #循环得到每一个连通区域属性集
        #忽略小区域
        area_2 = region.area * scale *scale
        if area_2 < min_thre:
            continue
        minr, minc, maxr, maxc = region.bbox
        area_1 = (maxr - minr) * (maxc - minc) * scale * scale
#        print((area_1, area_2))
        if area_2 / area_1 > max_area:
            continue

        minrr.append(minr)
        mincc.append(minc)
        maxrr.append(maxr)
        maxcc.append(maxc)
    m = len(minrr)
#    print(m)
    for i in range(m):
        cv.rectangle(img, (mincc[i],minrr[i]), (maxcc[i],maxrr[i]), (0,0,255), 3) 
#    cv.imwrite('juxing1.jpg', img)
    return mincc, minrr, maxcc, maxrr

'''
min_thre  窗户中第一个和第二个矩形长宽比最小值（长的：短的）
max_dis   窗户中矩形间最大间隔
max_long  窗户中第三个矩形和第一个矩形两边最大相差间隔
pro       图的比例尺像素：毫米
min_kuan  窗户的最小宽度
max_kuan  窗户的最大宽度
'''
def detect_two_rect_windows(img, mincc_x, minrr_y, maxcc_x, maxrr_y, singledoor_mincc, singledoor_minrr, singledoor_maxcc, singledoor_maxrr, scale, min_thre, max_dis, max_long, min_kuan, max_kuan):
    minrr_two = []#y坐标
    mincc_two = []#x坐标
    maxrr_two = []#y坐标
    maxcc_two = []#x坐标
    m = len(minrr_y)
    
    for i in range(m):
        if (maxrr_y[i] - minrr_y[i]) / (maxcc_x[i] - mincc_x[i]) > min_thre:
            for j in range(m):
                if j != i and abs(maxcc_x[i] - mincc_x[j]) < max_dis and abs(minrr_y[i] - minrr_y[j]) < max_dis and abs((maxcc_x[j] - mincc_x[j]) - (maxcc_x[i] - mincc_x[i])) < max_long and abs((maxrr_y[j] - minrr_y[j]) - (maxrr_y[i] - minrr_y[i])) < max_long:
                    if (maxcc_x[j] - mincc_x[i]) * scale > min_kuan and (maxcc_x[j] - mincc_x[i]) * scale < max_kuan:
#                        if np.sum(wall_img[minrr_y[i] - 4:minrr_y[i] + 1, mincc_x[i]:maxcc_x[j] + 1]) < 255*5*(maxcc_x[j] - mincc_x[i] + 1) or np.sum(wall_img[maxrr_y[i]:maxrr_y[i] + 5, mincc_x[i]:maxcc_x[j] + 1]) < 255*5*(maxcc_x[j] - mincc_x[i] + 1):
                            mincc_two.append(mincc_x[i])
                            minrr_two.append(minrr_y[i])
                            maxcc_two.append(maxcc_x[j])
                            maxrr_two.append(maxrr_y[j])
                            break 
                
    
    for i in range(m):
        if (maxcc_x[i] - mincc_x[i]) / (maxrr_y[i]-minrr_y[i]) > min_thre:
            for j in range(m):
                if j != i and abs(mincc_x[i] - mincc_x[j]) < max_dis and abs(maxrr_y[i] - minrr_y[j]) < max_dis and abs((maxcc_x[j] - mincc_x[j]) - (maxcc_x[i] - mincc_x[i])) < max_long and abs((maxrr_y[j] - minrr_y[j]) - (maxrr_y[i] - minrr_y[i])) < max_long:
                    if (maxrr_y[j] - minrr_y[i]) * scale > min_kuan and (maxrr_y[j] - minrr_y[i]) * scale < max_kuan:
#                        if np.sum(wall_img[minrr_y[i]:maxrr_y[j] + 1, mincc_x[i] - 4:mincc_x[i] + 1]) < 255*2*(maxrr_y[j] - minrr_y[i] + 1) or np.sum(wall_img[minrr_y[i]:maxrr_y[j] + 1, maxcc_x[i]:maxcc_x[i] + 5]) < 255*5*(maxrr_y[j] - minrr_y[i] + 1):
                            mincc_two.append(mincc_x[i])
                            minrr_two.append(minrr_y[i])
                            maxcc_two.append(maxcc_x[j])
                            maxrr_two.append(maxrr_y[j])
                            break
    
    m = len(minrr_two)
    img1 = img.copy()    
    for i in range(m):
        cv.rectangle(img1, (mincc_two[i],minrr_two[i]), (maxcc_two[i],maxrr_two[i]), (0,0,0), 3) 

    mincc_two, minrr_two, maxcc_two, maxrr_two = judge_remove_door(mincc_two, minrr_two, maxcc_two, maxrr_two, singledoor_mincc, singledoor_minrr, singledoor_maxcc, singledoor_maxrr)
    
    img = cv.cvtColor(img.copy(), cv.COLOR_GRAY2RGB)
    m = len(minrr_two)
#    print(m)
    for i in range(m):
        cv.rectangle(img, (mincc_two[i],minrr_two[i]), (maxcc_two[i],maxrr_two[i]), (0,255,255), 2) 
#    cv.imwrite('juxing.jpg', img)
    return mincc_two, minrr_two, maxcc_two, maxrr_two, img



def detect_two_piao_windows(img, mincc_x, minrr_y, maxcc_x, maxrr_y, scale, max_dis, max_offset, min_kuan, max_kuan):
    minrr_two = []#y坐标
    mincc_two = []#x坐标
    maxrr_two = []#y坐标
    maxcc_two = []#x坐标
    m = len(minrr_y)
    
    for i in range(m):
            for j in range(m):
                if j != i and abs(mincc_x[i] - mincc_x[j]) < max_dis and abs((minrr_y[i] - minrr_y[j]) - (maxrr_y[j] - maxrr_y[i])) < max_offset and maxcc_x[i] < maxcc_x[j] and minrr_y[j] < minrr_y[i] and maxrr_y[i] < maxrr_y[j]:                  
                    if (minrr_y[i] - minrr_y[j]) * scale * 2 > min_kuan and (minrr_y[i] - minrr_y[j]) * scale * 2 < max_kuan:
#                        if np.sum(wall_img[minrr_y[j]:minrr_y[i] + 1, mincc_x[j] - 4:mincc_x[j] + 1]) < 255*5*(minrr_y[i] - minrr_y[j] + 1) or np.sum(wall_img[maxrr_y[i]:maxrr_y[j] + 1, mincc_x[j] - 4:mincc_x[j] + 1]) < 255*5*(maxrr_y[j] - maxrr_y[i] + 1):    
                            mincc_two.append(min(mincc_x[i], mincc_x[j]))
                            minrr_two.append(min(minrr_y[i], minrr_y[j]))
                            maxcc_two.append(max(maxcc_x[i], maxcc_x[j]))
                            maxrr_two.append(max(maxrr_y[i], maxrr_y[j]))
                            break

    for i in range(m):
            for j in range(m):
                if j != i and abs(maxcc_x[i] - maxcc_x[j]) < max_dis and abs((minrr_y[i] - minrr_y[j]) - (maxrr_y[j] - maxrr_y[i])) < max_offset and mincc_x[j] < mincc_x[i] and minrr_y[j] < minrr_y[i] and maxrr_y[i] < maxrr_y[j]:                  
                    if (minrr_y[i] - minrr_y[j]) * scale * 2 > min_kuan and (minrr_y[i] - minrr_y[j]) * scale * 2 < max_kuan:
 #                       if np.sum(wall_img[minrr_y[j]:minrr_y[i] + 1, maxcc_x[j]:maxcc_x[j] + 5]) < 255*5*(minrr_y[i] - minrr_y[j] + 1) or np.sum(wall_img[maxrr_y[i]:maxrr_y[j] + 1, maxcc_x[j]:maxcc_x[j] + 5]) < 255*5*(maxrr_y[j] - maxrr_y[i] + 1):    
                            mincc_two.append(min(mincc_x[i], mincc_x[j]))
                            minrr_two.append(min(minrr_y[i], minrr_y[j]))
                            maxcc_two.append(max(maxcc_x[i], maxcc_x[j]))
                            maxrr_two.append(max(maxrr_y[i], maxrr_y[j]))
                            break
    
    for i in range(m):
            for j in range(m):   
                if j != i and abs(minrr_y[i] - minrr_y[j]) < max_dis and abs((mincc_x[i] - mincc_x[j]) - (maxcc_x[j] - maxcc_x[i])) < max_offset and maxrr_y[i] < maxrr_y[j] and mincc_x[j] < mincc_x[i] and maxcc_x[i] < maxcc_x[j]:
                    if (mincc_x[i] - mincc_x[j]) * scale * 2 > min_kuan and (mincc_x[i] - mincc_x[j]) * scale * 2 < max_kuan:
#                        if np.sum(wall_img[minrr_y[j] - 4:minrr_y[j] + 1, mincc_x[j]:mincc_x[i] + 1]) < 255*5*(mincc_x[i] - mincc_x[j] + 1) or np.sum(wall_img[minrr_y[j] - 4:minrr_y[j] + 1, maxcc_x[i]:maxcc_x[j] + 1]) < 255*5*(maxcc_x[j] - maxcc_x[i] + 1):    
                            mincc_two.append(min(mincc_x[i], mincc_x[j]))
                            minrr_two.append(min(minrr_y[i], minrr_y[j]))
                            maxcc_two.append(max(maxcc_x[i], maxcc_x[j]))
                            maxrr_two.append(max(maxrr_y[i], maxrr_y[j]))
                            break
                    
    for i in range(m):
            for j in range(m):
                if j != i and abs(maxrr_y[i] - maxrr_y[j]) < max_dis and abs((mincc_x[i] - mincc_x[j]) - (maxcc_x[j] - maxcc_x[i])) < max_offset and minrr_y[j] < minrr_y[i] and mincc_x[j] < mincc_x[i] and maxcc_x[i] < maxcc_x[j]:
                    if (mincc_x[i] - mincc_x[j]) * scale * 2 > min_kuan and (mincc_x[i] - mincc_x[j]) * scale * 2 < max_kuan:
#                        if np.sum(wall_img[maxrr_y[j]:maxrr_y[j] + 5, mincc_x[j]:mincc_x[i] + 1]) < 255*5*(mincc_x[i] - mincc_x[j] + 1) or np.sum(wall_img[maxrr_y[j]:maxrr_y[j] + 5, maxcc_x[i]:maxcc_x[j] + 1]) < 255*5*(maxcc_x[j] - maxcc_x[i] + 1):    
                            mincc_two.append(min(mincc_x[i], mincc_x[j]))
                            minrr_two.append(min(minrr_y[i], minrr_y[j]))
                            maxcc_two.append(max(maxcc_x[i], maxcc_x[j]))
                            maxrr_two.append(max(maxrr_y[i], maxrr_y[j]))
                            break
    
    img = cv.cvtColor(img.copy(), cv.COLOR_GRAY2RGB)                
    m = len(minrr_two)
#    print(m)
    for i in range(m):
        cv.rectangle(img, (mincc_two[i],minrr_two[i]), (maxcc_two[i],maxrr_two[i]), (255,0,255), 2) 
#    cv.imwrite('juxing2.jpg', img)
    return mincc_two, minrr_two, maxcc_two, maxrr_two, img


def deal_door(singledoorlist):
    m = len(singledoorlist)

    mincc = []
    minrr = []
    maxcc = []
    maxrr = []
    for i in range(m):
        x1, y1, x2, y2, a, b = singledoorlist[i]
        if x1 == x2:
            door_mincc = x1 - a
            door_minrr = y1
            door_maxcc = x2 + b
            door_maxrr = y2
        elif y1 == y2:
            door_mincc = x1
            door_minrr = y1 - a
            door_maxcc = x2
            door_maxrr = y2 + b
        mincc.append(door_mincc)
        minrr.append(door_minrr)
        maxcc.append(door_maxcc)
        maxrr.append(door_maxrr)        
            
    return mincc, minrr, maxcc, maxrr


def Windows_detect(img, scale): #single_door, sliding_door):
    init_decoration_room_img = img.copy()  
    #singledoorlist = single_door.out_base_position()
    #slidingdoorlist = sliding_door.out_base_position()
    #singledoorlist.extend(slidingdoorlist)
    singledoorlist = []
    door_mincc, door_minrr, door_maxcc, door_maxrr = deal_door(singledoorlist)

#    slidingdoor_mincc, slidingdoor_minrr, slidingdoor_maxcc, slidingdoor_maxrr = deal_door(slidingdoorlist)
    
    
    mincc_rect, minrr_rect, maxcc_rect, maxrr_rect = get_rect_corner_position(init_decoration_room_img.copy(), scale, Settings.rect_position_min_thre, Settings.rect_position_max_area)
    mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win, img_two_rect_win = detect_two_rect_windows(init_decoration_room_img.copy(), mincc_rect, minrr_rect, maxcc_rect, maxrr_rect, door_mincc, door_minrr, door_maxcc, door_maxrr, scale, Settings.rect_two_min_thre, Settings.rect_two_max_dis, Settings.rect_two_max_long, Settings.rect_two_min_kuan, Settings.rect_two_max_kuan)
    
    mincc_piao, minrr_piao, maxcc_piao, maxrr_piao = get_piao_corner_position(init_decoration_room_img.copy(), scale, Settings.piao_position_min_thre, Settings.piao_position_max_area)
    mincc_two_piao, minrr_two_piao, maxcc_two_piao, maxrr_two_piao, img_two_piao_win = detect_two_piao_windows(init_decoration_room_img.copy(), mincc_piao, minrr_piao, maxcc_piao, maxrr_piao, scale, Settings.piao_two_max_dis, Settings.piao_two_max_offset, Settings.piao_two_min_kuan, Settings.piao_two_max_kuan)
    return img_two_rect_win, img_two_piao_win, mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win, mincc_two_piao, minrr_two_piao, maxcc_two_piao, maxrr_two_piao
    
    
    
    
    