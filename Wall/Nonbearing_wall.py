# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 18:25:06 2018

@author: 王科涛
"""
from Datastruct import Data_struct
from Wall import remove_corner_point
from Wall import Wall_division

import cv2 as cv
import numpy as np
from skimage import measure


'''
传入的img是原始的灰度图;
传入的bearingwall_img是承重墙识别图;
'''
def Nonbearing_Wall(img, bearingwall_img,nonbearingwall_thre,prop):
    img[img <= nonbearingwall_thre] = 0
    img[img> nonbearingwall_thre] = 255
    img[bearingwall_img == 0] = 255
    
#    cv.imwrite('1.jpg', img) 
        
    kernel = np.uint8(np.ones((3,3)))
    img = cv.dilate(img, kernel)    
    img = cv.erode(img, kernel)

    img[img == 0] = 1
    label_image=measure.label(img, connectivity = 1)
    for region in measure.regionprops(label_image):
        minr, minc, maxr, maxc = region.bbox
        if region.area < 100:
            img[minr:maxr, minc:maxc] = 255
            continue
    img[img == 1] = 0

#    cv.imwrite('2.jpg', img)
    
    kernel = np.uint8(np.ones((5,5)))
    img = cv.dilate(img, kernel)    
    img = cv.erode(img, kernel)
    
#    cv.imwrite('3.jpg', img)
    
    img = remove_corner_point.Remove_corner_point(img)    

#    cv.imwrite('4.jpg', img)
    
    img, contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)  
#    for i in range(0,len(contours)):
#        for j in range(0,len(contours[i])):
#            cv.rectangle(img, (contours[i][j][0][0],contours[i][j][0][1]), (contours[i][j][0][0],contours[i][j][0][1]), (0,0,0), 1)
    
#    cv.imwrite('5.jpg', img)    
    
    nonbearingwall = Data_struct.Wall()
    nonbearingwall.set_type(1)
    nonbearingwall.add_contour(contours)   
    nonbearingwall = Wall_division.Divide_rect_for_nonbearwall(nonbearingwall,prop)
    return img, nonbearingwall