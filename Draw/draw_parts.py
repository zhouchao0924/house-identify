# -*- coding: utf-8 -*-
"""
Created on Tue May 15 18:59:45 2018

@author: wutia
"""

from Datastruct import Data_struct
import cv2 as cv
import copy
import math

def draw_examples_blank(img_blank):
    blank_shape=img_blank.shape
    blank_width=blank_shape[0]
    blank_length=blank_shape[1]
    start_y=int(blank_width*0.6)
    start_x=int(blank_length*0.85)
    
    line_start_x=start_x
    line_end_x=int(blank_length*0.90)
    
    dis=int((blank_width-start_y)/12)
    
    #cv.line(img_blank, (line_start_x,start_y), (line_end_x,start_y), (0,0,0), 2) 
    #cv.putText(img_blank,'ruler',(line_end_x+10,start_y),cv.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)    
    
    cv.line(img_blank, (line_start_x,start_y+dis), (line_end_x,start_y+dis), (0,0,255), 2) 
    cv.putText(img_blank,'bearwall',(line_end_x+10,start_y+dis),cv.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
    
    cv.line(img_blank, (line_start_x,start_y+dis*2), (line_end_x,start_y+dis*2), (0,165,255), 2) 
    cv.putText(img_blank,'nonbearwall',(line_end_x+10,start_y+dis*2),cv.FONT_HERSHEY_SIMPLEX,0.5,(0,165,255),2)
    
    cv.line(img_blank, (line_start_x,start_y+dis*3), (line_end_x,start_y+dis*3), (255,0,0), 2)
    cv.putText(img_blank,'flue',(line_end_x+10,start_y+dis*3),cv.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)
    
    cv.line(img_blank, (line_start_x,start_y+dis*4), (line_end_x,start_y+dis*4), (240,32,160), 2) 
    cv.putText(img_blank,'window',(line_end_x+10,start_y+dis*4),cv.FONT_HERSHEY_SIMPLEX,0.5,(240,32,160),2)
    
    cv.line(img_blank, (line_start_x,start_y+dis*5), (line_end_x,start_y+dis*5), (255,191,0), 2)
    cv.putText(img_blank,'bay_window',(line_end_x+10,start_y+dis*5),cv.FONT_HERSHEY_SIMPLEX,0.5,(255,191,0),2)
    
    cv.line(img_blank, (line_start_x,start_y+dis*6), (line_end_x,start_y+dis*6), (180,110,255), 2) 
    cv.putText(img_blank,'balcony',(line_end_x+10,start_y+dis*6),cv.FONT_HERSHEY_SIMPLEX,0.5,(180,110,255),2)
    
    cv.line(img_blank, (line_start_x,start_y+dis*7), (line_end_x,start_y+dis*7), (0,238,0), 2)     
    cv.putText(img_blank,'singledoor',(line_end_x+10,start_y+dis*7),cv.FONT_HERSHEY_SIMPLEX,0.5,(0,238,0),2)
    
    cv.line(img_blank, (line_start_x,start_y+dis*8), (line_end_x,start_y+dis*8), (80,10,139), 2) #(147,112,219)
    cv.putText(img_blank,'doubledoor',(line_end_x+10,start_y+dis*8),cv.FONT_HERSHEY_SIMPLEX,0.5,(80,10,139),2)
    
    cv.line(img_blank, (line_start_x,start_y+dis*9), (line_end_x,start_y+dis*9), (0,255,255), 2) #(37,193,255)
    cv.putText(img_blank,'slidingdoor',(line_end_x+10,start_y+dis*9),cv.FONT_HERSHEY_SIMPLEX,0.5,(0,255,255),2)

def draw_examples_decoration(img_decoration):
    decoration_shape=img_decoration.shape
    decoration_width=decoration_shape[0]
    decoration_length=decoration_shape[1]   
    decoration_start_y=decoration_width-1200
    decoration_start_x=decoration_length-1200
    
#    cv.line(img_decoration, (decoration_start_x,decoration_start_y), (decoration_start_x+400,decoration_start_y), (0,0,255), 5) 
#    cv.putText(img_decoration,'ruler',(decoration_start_x+450,decoration_start_y+20),cv.FONT_HERSHEY_SIMPLEX,4,(0,0,255),4)    
#    cv.line(img_decoration, (decoration_start_x,decoration_start_y+150), (decoration_start_x+400,decoration_start_y+150), (255,0,0), 5) 
#    cv.putText(img_decoration,'singledoor',(decoration_start_x+450,decoration_start_y+150+20),cv.FONT_HERSHEY_SIMPLEX,4,(255,0,0),4)
#    cv.line(img_decoration, (decoration_start_x,decoration_start_y+300), (decoration_start_x+400,decoration_start_y+300), (147,112,219), 5) 
#    cv.putText(img_decoration,'doubledoor',(decoration_start_x+450,decoration_start_y+300+20),cv.FONT_HERSHEY_SIMPLEX,4,(147,112,219),4)
#    cv.line(img_decoration, (decoration_start_x,decoration_start_y+450), (decoration_start_x+400,decoration_start_y+450), (37,193,255), 5) 
#    cv.putText(img_decoration,'slidingdoor',(decoration_start_x+450,decoration_start_y+450+20),cv.FONT_HERSHEY_SIMPLEX,4,(37,193,255),4)


def draw_ruler(layout,img_decoration):
    #img_blank = copy.copy(img_blank)
    #img_blank = cv.cvtColor(img_blank, cv.COLOR_GRAY2RGB)
    
    #img_decoration = copy.copy(img_decoration)
    #img_decoration = cv.cvtColor(img_decoration, cv.COLOR_GRAY2RGB)


    rulerlist=layout.out_rulerlist()
    pix_loc_top=rulerlist.data_dic['top_ruler'].out_pixel_loc()
    pix_loc_down=rulerlist.data_dic['down_ruler'].out_pixel_loc()
    pix_loc_left=rulerlist.data_dic['left_ruler'].out_pixel_loc()
    pix_loc_right=rulerlist.data_dic['right_ruler'].out_pixel_loc()
    
    for i in range(len(pix_loc_top)):
        cv.rectangle(img_decoration, (pix_loc_top[i][0]-10,pix_loc_top[i][1]-10), (pix_loc_top[i][0]+10,pix_loc_top[i][1]+10), (0,0,255), 2)            
    for i in range(len(pix_loc_down)):
        cv.rectangle(img_decoration, (pix_loc_down[i][0]-10,pix_loc_down[i][1]-10), (pix_loc_down[i][0]+10,pix_loc_down[i][1]+10), (0,0,255), 2)            
    for i in range(len(pix_loc_left)):
        cv.rectangle(img_decoration, (pix_loc_left[i][0]-10,pix_loc_left[i][1]-10), (pix_loc_left[i][0]+10,pix_loc_left[i][1]+10), (0,0,255), 2)            
    for i in range(len(pix_loc_right)):
        cv.rectangle(img_decoration, (pix_loc_right[i][0]-10,pix_loc_right[i][1]-10), (pix_loc_right[i][0]+10,pix_loc_right[i][1]+10), (0,0,255), 2)            
   
    #return img_blank,img_decoration


def draw_bearwall(layout,img_blank):
   # img_blank = cv.cvtColor(img_blank, cv.COLOR_GRAY2RGB)
    walls = layout.out_walls()

    bearwall = walls[0]    
    
    bearwall_position=bearwall.out_contour()
   # bearwall_position=bearwall_position[0]
    #for i in range(0,len(bearwall_position)):
        #for j in range(0,len(bearwall_position[i])):
            #cv.rectangle(img_blank, (bearwall_position[i][j][0][0]-2,bearwall_position[i][j][0][1]-2), (bearwall_position[i][j][0][0]+2,bearwall_position[i][j][0][1]+2), (0,0,255), 3)
    cv.drawContours(img_blank, bearwall_position, -1, (0,0,255), 2)
    
    #return img_blank,img_decoration

def draw_nonbearwall(layout,img_blank):
    walls = layout.out_walls()

    non_bearwall = walls[1]
        
    non_bearwall_position=non_bearwall.out_contour()
    #non_bearwall_position=non_bearwall_position[0]

   
    #for i in range(0,len(non_bearwall_position)):
        #for j in range(0,len(non_bearwall_position[i])):
            #cv.rectangle(img_blank, (non_bearwall_position[i][j][0][0]-2,non_bearwall_position[i][j][0][1]-2), (non_bearwall_position[i][j][0][0]+2,non_bearwall_position[i][j][0][1]+2), (0,165,255), 3)
    cv.drawContours(img_blank, non_bearwall_position, -1, (0,165,255), 2)

    #return img_blank,img_decoration
def draw_rect(list_rect,rect_id,img_blank,color1,color2,flag):
    for i in range(0,len(list_rect)):
        if abs(list_rect[i][0] - list_rect[i][2])<=2:
            x1 = list_rect[i][0] - list_rect[i][4]
            y1 = list_rect[i][1]
            x2 = list_rect[i][2] + list_rect[i][5]
            y2 = list_rect[i][3]
            cv.rectangle(img_blank,(x1,y1),(x2,y2),color1,2)
            if flag:
                cv.putText(img_blank,str(rect_id[i]),(list_rect[i][0],int((list_rect[i][1]+list_rect[i][3])/2)),cv.FONT_HERSHEY_SIMPLEX,2,(155,50,0),4)
        else:
            x1 = list_rect[i][0]
            y1 = list_rect[i][1] - list_rect[i][4]
            x2 = list_rect[i][2]
            y2 = list_rect[i][3] + list_rect[i][5]
            cv.rectangle(img_blank,(x1,y1),(x2,y2),color2,2)
            if flag:
                cv.putText(img_blank,str(rect_id[i]),(int((list_rect[i][0]+list_rect[i][2])/2),list_rect[i][1]),cv.FONT_HERSHEY_SIMPLEX,2,(155,50,0),4)
def draw_bearwall_division(layout,img_blank):
    walls = layout.out_walls()
    bearwall = walls[0]        
    list_wall=bearwall.out_wall_division()
    wall_id = bearwall.out_wall_id()
    draw_rect(list_wall,wall_id,img_blank,(0,0,255),(0,0,255),False)

def draw_nonbearwall_division(layout,img_blank):
    walls = layout.out_walls()
    non_bearwall = walls[1]        
    list_wall=non_bearwall.out_wall_division()
    wall_id = non_bearwall.out_wall_id()
    draw_rect(list_wall,wall_id,img_blank,(0,165,255),(0,165,255),False)
    
def draw_door_opening(door_opening,door_opening_id,img_blank):
    draw_rect(door_opening,door_opening_id,img_blank,(0,255,0),(0,255,0),False)
    
def draw_door(layout,img_blank):
    doors = layout.out_doors()[0]
    door_rect = doors.out_base_position()
    draw_rect(door_rect,list(range(0,len(door_rect))),img_blank,(0,238,0),(0,238,0),False)
    doors = layout.out_doors()[1]
    door_rect = doors.out_base_position()
    draw_rect(door_rect,list(range(0,len(door_rect))),img_blank,(80,10,139),(80,10,139),False)#(147,112,219)98,230,138
    doors = layout.out_doors()[2]
    door_rect = doors.out_base_position()
    draw_rect(door_rect,list(range(0,len(door_rect))),img_blank,(0,255,255),(0,255,255),False)
def draw_flues(layout,img_blank):
    flues = layout.out_flues()
    for i in range(len(flues)):
        position=flues[i].out_position()
        #cv.putText(img_blank, 'flue',(position[0],position[1]),cv.FONT_HERSHEY_SIMPLEX ,2,(0,255,255),1)        
        cv.rectangle(img_blank, (position[0],position[1]), (position[0]+flues[i].out_length(),position[1]+flues[i].out_width()), (255,0,0), 10)    
    
    #return img_blank,img_decoration
    
  
  
    
def draw_windows(layout,img_blank):
    windows = layout.out_windows()
    win_normal = windows[0]
    win_bay = windows[1]
    win_balcony = windows[2]
    
    base_position_normal=win_normal.out_base_position()
    xflip_normal=win_normal.out_Xflip()
    yflip_normal=win_normal.out_Yflip()
    for i in range(len(base_position_normal)):
        (a_x,a_y,b_x,b_y,dis1,dis2)=base_position_normal[i]
        if xflip_normal[i]==1 and yflip_normal[i]==0:
            a_y-=dis1
            b_y+=dis1
        elif xflip_normal[i]==0 and yflip_normal[i]==1:
            a_x-=dis1
            b_x+=dis1
        else:
            print('error: wrong Xflip and Yflip')
        cv.rectangle(img_blank, (a_x,a_y), (b_x,b_y), (240,32,160), 2)

    base_position_balcony=win_balcony.out_base_position()
    xflip_balcony=win_balcony.out_Xflip()
    yflip_balcony=win_balcony.out_Yflip()
    for i in range(len(base_position_balcony)):
        (a_x,a_y,b_x,b_y,dis1,dis2)=base_position_balcony[i]
        if xflip_balcony[i]==1 and yflip_balcony[i]==0:
            a_y-=dis1
            b_y+=dis1
        elif xflip_balcony[i]==0 and yflip_balcony[i]==1:
            a_x-=dis1
            b_x+=dis1
        else:
            print('error: wrong Xflip and Yflip')
        cv.rectangle(img_blank, (a_x,a_y), (b_x,b_y),(180,110,255), 2)
    
    base_position_bay=win_bay.out_base_position()
    xflip_bay=win_bay.out_Xflip()
    yflip_bay=win_bay.out_Yflip()
    for i in range(len(base_position_bay)):
        (a_x,a_y,b_x,b_y,dis1,dis2)=base_position_bay[i]
        if xflip_bay[i]==1 and yflip_bay[i]==0 and dis1==0:
            b_y+=dis2
        elif xflip_bay[i]==1 and yflip_bay[i]==0 and dis2==0:
            a_y-=dis1
        elif xflip_bay[i]==0 and yflip_bay[i]==1 and dis1==0:
            b_x+=dis2
        elif xflip_bay[i]==0 and yflip_bay[i]==1 and dis2==0:
            a_x-=dis1
        else:
            pass
        cv.rectangle(img_blank, (a_x,a_y), (b_x,b_y), (255,191,0), 2)
    
    
    
    