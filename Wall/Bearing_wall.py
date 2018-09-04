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
传入的img是原始的灰度图
'''
def Bearing_Wall(img,bearingwall_thre,prop):
    
    img[img <= bearingwall_thre] = 0
    img[img > bearingwall_thre] = 255
    
    kernel=np.uint8(np.ones((3,3)))
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
    
    kernel = np.uint8(np.ones((5,5)))
    img = cv.dilate(img, kernel)    
    img = cv.erode(img, kernel)
    
    img = remove_corner_point.Remove_corner_point(img)    
    
#    cv.imwrite('1.jpg', img) 

    img, contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)  
#    for i in range(0,len(contours)):
#        for j in range(0,len(contours[i])):
#            cv.rectangle(img, (contours[i][j][0][0],contours[i][j][0][1]), (contours[i][j][0][0],contours[i][j][0][1]), (0,0,0), 1)
    
    bearingwall = Data_struct.Wall()
    bearingwall.set_type(0)
    bearingwall.add_contour(contours)
    bearingwall = Wall_division.Divide_rect_for_bearwall(bearingwall,prop)
    return img, bearingwall