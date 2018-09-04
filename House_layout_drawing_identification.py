# -*- coding: utf-8 -*-
"""
Created on Fri Aug 03 15:32:07 2018

@author: 王科涛
"""

from Settings import Settings
from Datastruct import Data_struct
from Binary import Binarization
from Wall import Bearing_wall
from Wall import Nonbearing_wall
from Window import judge_window
from Door import Doors
from Ruler import Rulers
from Draw import draw_parts
from Door_opening import Door_opening
from Json import newJson
import cv2 as cv
import os
import numpy as np

def mkdir(path):
    path = path.strip()
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)  
        return True
    else:
        return False

if __name__ == "__main__":
     
    #png_list = [ 20]
    #png_list = [48,53,54,56,58,60,62,65,68,70,71,72,73,82,83,84,91,92,93,95,97,98]
    #png_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,41,42,48,53,54,56,58,60,62,65,68,70,71,72,73,82,83,84,91,92,93,95,97,98]
    png_list = [i for i in range(1,53)]
    #png_list = [3]
    
    for png in png_list:
        print(png)
        png = str(png)
        Blank_room_readfilename = "KJLtest/" + str(png) + ".png"   
        Blank_room_outfilename = "KJLresult/" + str(png)  + '/'
        mkdir(Blank_room_outfilename)

        Layout = Data_struct.Layout(str(png) + ".jpg")
        
        #原图:Blank_room_img
        try:
            print('正在读入图片...')
            Blank_room_img = cv.imread(Blank_room_readfilename, 0) 
        #cv.imwrite(Blank_room_outfilename + 'Original.jpg', Blank_room_img)
            print('图片读入完毕...')
        except:
            print(png + ': ' + '读入图片' + ' Error')
            continue
        try:
            print('图片正在进行二值化...')
            #二值化后：binary_Blank_room_img
            Binary_blank_room_img = Binarization.Binary(Blank_room_img, Settings.threshold)
#           cv.imwrite(Blank_room_outfilename + 'Binary.jpg', Binary_blank_room_img)  
            print('图片二值化完毕...')
        except:
            print(png + ': ' + '二值化' + ' Error')
            continue
        
        try:
        #if 1:
            print('正在识别标尺...')
            Ruler, up_num, up_diff, image_biaochi = Rulers.getRuler(Blank_room_img.copy(), Binary_blank_room_img.copy())
            #Ruler = Data_struct.Ruler()
            #Ruler.proportion(0.06)
            #Ruler.scale(1/0.06)
            Layout.add_ruler(Ruler)
            cv.imwrite(Blank_room_outfilename + 'biaochi.png',image_biaochi)
            print('标尺识别完毕...')
        except:
            print(png + ': '+ '识别标尺' + ' Error')
            continue
        
        try:
            print('正在识别承重墙...')
            Blankroom_bearingwall_img, bearingwall = Bearing_wall.Bearing_Wall(Blank_room_img.copy(), Settings.Bearingwall_thre,Ruler.out_proportion()) 
            cv.imwrite(Blank_room_outfilename + 'Bearingwall.jpg', Blankroom_bearingwall_img)
            print('承重墙识别完毕...')
        except:
            print(png + ': ' + '识别承重墙' + ' Error')     
            continue
        
        try:
            print('正在识别非承重墙...')        
            Blankroom_nonbearingwall_img, nonbearingwall = Nonbearing_wall.Nonbearing_Wall(Blank_room_img.copy(), Blankroom_bearingwall_img.copy(), Settings.Nonbearingwall_thre,Ruler.out_proportion())
            #np.savez(png+".npz",nonbearingwall.out_contour(),Ruler.out_proportion())
            cv.imwrite(Blank_room_outfilename + 'Nonearingwall.jpg', Blankroom_nonbearingwall_img)
            print('非承重墙识别完毕...')
        except:
            print(png+': '+'识别非承重墙'+' Error')
            continue
        
        try:
        #if 1:
            print('正在识别门洞...')
            door_opening, door_opening_id,bearingwall, nonbearingwall = Door_opening.Get_door_opening(bearingwall,nonbearingwall,Ruler.out_proportion())
            Layout.add_wall(bearingwall)
            Layout.add_wall(nonbearingwall)
            print('门洞识别完毕...')
        except:
            print(png+': '+'识别门洞'+' Error')
            continue
        
        try:
        #if 1:
            print('正在识别门...')        
            wall_img = Blankroom_nonbearingwall_img.copy()
            wall_img[Blankroom_bearingwall_img == 0] = 0
        #img_two_rect_win, img_two_piao_win, mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win, mincc_two_piao, minrr_two_piao, maxcc_two_piao, maxrr_two_piao = window.Windows_detect(Binary_blank_room_img.copy(), Ruler.out_scale())
        #single_door,sliding_door,draw_img = Doors.Door_detect(nonbearingwall, Blank_room_img.copy(), wall_img, Ruler.out_proportion(), Binary_blank_room_img.copy(), Ruler.out_scale(), bearingwall, mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win)
            single_door,double_door,sliding_door,draw_img,mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win,mincc_two_piao, minrr_two_piao, maxcc_two_piao, maxrr_two_piao = Doors.Door_detect(nonbearingwall, Blank_room_img.copy(), wall_img, Ruler.out_proportion(), Binary_blank_room_img.copy(), Ruler.out_scale(), bearingwall,door_opening.copy(),door_opening_id.copy())
            Layout.add_door(single_door)
            Layout.add_door(double_door)
            Layout.add_door(sliding_door)
            cv.imwrite(Blank_room_outfilename + 'door.png', draw_img)
            print('门识别完毕...')
        except:
            print(png+': '+'识别门'+' Error')
            continue
        
        try:
        #if 1:
            print('正在识别窗户...') 
        #img_two_rect_win, img_two_piao_win, mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win, mincc_two_piao, minrr_two_piao, maxcc_two_piao, maxrr_two_piao = window.Windows_detect(Binary_blank_room_img.copy(), Ruler.out_scale())
 #       cv.imwrite(Blank_room_outfilename + 'pu1.png', img1)
        #cv.imwrite(Blank_room_outfilename + 'pu.png', img_two_rect_win)
        #cv.imwrite(Blank_room_outfilename + 'piao.png', img_two_piao_win)
            win_normal,win_bay,win_balcony,windows_img = judge_window.judge_window_type(Blank_room_img.copy(),Binary_blank_room_img.copy(),wall_img,sliding_door,bearingwall,nonbearingwall,mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win,mincc_two_piao, minrr_two_piao, maxcc_two_piao, maxrr_two_piao,int(Settings.judge_win_thres1*Ruler.out_proportion()),int(Settings.judge_win_thres2*Ruler.out_proportion()),Ruler.out_proportion(),0)
            Layout.add_window(win_normal)
            Layout.add_window(win_bay)
            Layout.add_window(win_balcony)
            cv.imwrite(Blank_room_outfilename + 'window.png', windows_img)
            print('窗户识别完毕...') 
        except:
            print(png+': '+'识别窗户'+' Error')
            continue

# =============================================================================
# 
#         two_rec_img=Blank_room_img.copy()
#         two_rec_img = cv.cvtColor(two_rec_img, cv.COLOR_GRAY2RGB)
#         for i in range(len(mincc_two_rect_win)):
#             cv.rectangle(two_rec_img,(mincc_two_rect_win[i],minrr_two_rect_win[i]),(maxcc_two_rect_win[i],maxrr_two_rect_win[i]),(0,0,255),2)
#         cv.imwrite(Blank_room_outfilename + 'two_rect.png', two_rec_img)
#    
# =============================================================================
        try:
            Blank_room_img = cv.cvtColor(Blank_room_img, cv.COLOR_GRAY2RGB)
        except:
            print(png+': '+'cvtColor'+' Error')
            continue
      
        try:
            draw_parts.draw_examples_blank(Blank_room_img)
        except:
            print(png+': '+'draw_examples_blank'+' Error')
            continue

        try:
            print('正在画承重墙...') 
            draw_parts.draw_bearwall_division(Layout,Blank_room_img)
        except:
            print(png+': '+'draw_bearwall_division'+' Error')
            continue

        try:
            print('正在画非承重墙...')	
            draw_parts.draw_nonbearwall_division(Layout,Blank_room_img)
            #draw_parts.draw_nonbearwall(Layout,init_blank_room_img)
        except:
            print(png+': '+'draw_nonbearwall_division'+' Error')
            continue
        
        try:
            print('正在画门洞...')	
            #draw_parts.draw_door_opening(door_opening,door_opening_id,Blank_room_img)
            #cv.imwrite(Blank_room_outfilename + "dooropening.png", Blank_room_img)
        except:
            print(png+': '+'draw_nonbearwall_division'+' Error')
            continue

        try:
            print('正在画门...')
            draw_parts.draw_door(Layout,Blank_room_img)
        except:
            print(png+': '+'draw_door'+' Error')
            continue
#
        try:   
            print('正在画窗...')         
            draw_parts.draw_windows(Layout,Blank_room_img)
        except:
            print(png+': '+'draw_windows'+' Error')
            continue
        
        try:
            print('正在写入文件...') 
            cv.imwrite(Blank_room_outfilename + "all.png", Blank_room_img)
        except:
            print(png+': '+'imwrite'+' Error')
            continue

        try:
            print('正在转化json...') 
            jsonfilename=Blank_room_outfilename+'HouseJson'
            newJson.toJson(Layout,jsonfilename)
        except:
            print(png+': '+'转化Json'+' Error')
        else:
            print('done')
