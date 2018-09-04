# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 16:07:59 2018

@author: wutia
"""
from Door import Sliding_doors
from Door import Single_doors
import cv2 as cv
import numpy as np
from Datastruct import Data_struct
import os

from skimage import measure,color
import copy
from Door import Get_door
from Window import window


def Door_detect(nonbearingwall,Blank_img,wall_img,prop,binary_img, scale,bearingwall,door_opening,door_opening_id):
    img_two_rect_win, img_two_piao_win, mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win, mincc_two_piao, minrr_two_piao, maxcc_two_piao, maxrr_two_piao = window.Windows_detect(binary_img.copy(),scale)
    draw_img=Blank_img.copy()
    draw_img = cv.cvtColor(draw_img, cv.COLOR_GRAY2RGB)
    
    single_door_1,img = Single_doors.Door_detect(nonbearingwall,bearingwall,Blank_img,wall_img,prop)
   
    
    sobel_img=Single_doors.sobel_demo(Blank_img)
    #cv.imwrite('sobel.png',sobel_img)
    single_door_2,double_door,sliding_door_1=Sliding_doors.Door_detect(sobel_img, scale,bearingwall, nonbearingwall,mincc_two_rect_win.copy(), minrr_two_rect_win.copy(), maxcc_two_rect_win.copy(), maxrr_two_rect_win.copy(),door_opening.copy(),door_opening_id.copy())

    single_door = Get_door.union_single(single_door_1,single_door_2,prop)
    
   
    single_position=single_door.out_base_position()             
    for i in range(len(single_position)):       
        if(single_position[i][1]==single_position[i][3]):#如果是水平主轴
            cv.rectangle(draw_img,(min(single_position[i][0],single_position[i][2]),single_position[i][1]-single_position[i][4]),(max(single_position[i][0],single_position[i][2]),single_position[i][1]+single_position[i][5]),(37,255,50), 2)
        if(single_position[i][0]==single_position[i][2]):#如果是竖直主轴    
            cv.rectangle(draw_img,(single_position[i][0]-single_position[i][4],min(single_position[i][1],single_position[i][3])),(single_position[i][0]+single_position[i][5],max(single_position[i][1],single_position[i][3])),(37,255,50), 2)

# =============================================================================
    double_position=double_door.out_base_position() 
    for i in range(len(double_position)):       
        if(double_position[i][1]==double_position[i][3]):#如果是水平主轴
            cv.rectangle(draw_img,(min(double_position[i][0],double_position[i][2]),double_position[i][1]-double_position[i][4]),(max(double_position[i][0],double_position[i][2]),double_position[i][1]+double_position[i][5]),(255,50,150), 2)
        if(double_position[i][0]==double_position[i][2]):#如果是竖直主轴    
            cv.rectangle(draw_img,(double_position[i][0]-double_position[i][4],min(double_position[i][1],double_position[i][3])),(double_position[i][0]+double_position[i][5],max(double_position[i][1],double_position[i][3])),(255,50,150), 2)
#     
# =============================================================================
    #sliding_position=sliding_door_1.out_base_position()
    #print(sliding_position)
    door_opening,door_opening_id = Get_door.remove_repetition(single_position,door_opening,door_opening_id,prop)
    door_opening,door_opening_id = Get_door.remove_repetition(double_position,door_opening,door_opening_id,prop)
    door_opening,door_opening_id = Get_door.remove_repetition_two_rect(mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win,door_opening,door_opening_id,prop)
    door_opening,door_opening_id = Get_door.remove_repetition_two_rect(mincc_two_piao, minrr_two_piao, maxcc_two_piao, maxrr_two_piao,door_opening,door_opening_id,prop)
    
    sliding_door = Get_door.union_sliding(sliding_door_1,door_opening,door_opening_id,prop)
    sliding_position=sliding_door.out_base_position()
    #print(sliding_position)
    for i in range(len(sliding_position)):       
        if(sliding_position[i][1]==sliding_position[i][3]):#如果是水平主轴
            cv.rectangle(draw_img,(min(sliding_position[i][0],sliding_position[i][2]),sliding_position[i][1]-sliding_position[i][4]),(max(sliding_position[i][0],sliding_position[i][2]),sliding_position[i][1]+sliding_position[i][5]),(150,50,255), 2)
        if(sliding_position[i][0]==sliding_position[i][2]):#如果是竖直主轴    
            cv.rectangle(draw_img,(sliding_position[i][0]-sliding_position[i][4],min(sliding_position[i][1],sliding_position[i][3])),(sliding_position[i][0]+sliding_position[i][5],max(sliding_position[i][1],sliding_position[i][3])),(150,50,255), 2)

    #return single_door,sliding_door,img, draw_img
    mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win = Get_door.remove_repetition_door(mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win,single_door)
    mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win = Get_door.remove_repetition_door(mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win,double_door)
    mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win = Get_door.remove_repetition_door(mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win,sliding_door)
    return single_door,double_door,sliding_door,draw_img,mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win,mincc_two_piao, minrr_two_piao, maxcc_two_piao, maxrr_two_piao
    
