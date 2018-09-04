# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 11:44:25 2018

@author: 王科涛
"""
import cv2 as cv
import numpy as np

def Remove_corner_point(img):
    
    template_1 = np.zeros((5,5), dtype = np.uint8)
    template_1[:, :] = 255
    template_1[4, :] = 0
    template_1[:, 4] = 0
    template_1[3, 3] = 0
    w, h = template_1.shape[::-1]
    res = cv.matchTemplate(img, template_1, cv.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        img[pt[1] + 3, pt[0] + 3] = 255
    
    template_2 = np.zeros((5,5), dtype = np.uint8)
    template_2[:, :] = 255
    template_2[0, :] = 0
    template_2[:, 0] = 0
    template_2[1, 1] = 0
    w, h = template_2.shape[::-1]
    res = cv.matchTemplate(img, template_2, cv.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        img[pt[1] + 1, pt[0] + 1] = 255
    
    template_3 = np.zeros((5,5), dtype = np.uint8)
    template_3[:, :] = 255
    template_3[4, :] = 0
    template_3[:, 0] = 0
    template_3[3, 1] = 0
    w, h = template_3.shape[::-1]
    res = cv.matchTemplate(img, template_3, cv.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        img[pt[1] + 3, pt[0] + 1] = 255
    
    template_4 = np.zeros((5,5), dtype = np.uint8)
    template_4[:, :] = 255
    template_4[0, :] = 0
    template_4[:, 4] = 0
    template_4[1, 3] = 0
    w, h = template_4.shape[::-1]
    res = cv.matchTemplate(img, template_4, cv.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        img[pt[1] + 1, pt[0] + 3] = 255

    return img