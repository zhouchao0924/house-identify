# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 20:05:49 2018

@author: 王科涛
"""


import cv2 as cv

def Binary(img, threshold):
    #img = cv.imread(blank_room_filename, 0)
    hline = cv.getStructuringElement(cv.MORPH_RECT, (2, 1), (-1, -1)) 
    vline = cv.getStructuringElement(cv.MORPH_RECT, (1, 2), (-1, -1))
    res1 = cv.dilate(img, hline)
    res1 = cv.dilate(res1, vline)
    res1[res1 < threshold] = 0
    res1[res1 >= threshold] = 255    
    return res1

#def gray2binary(img, threshold):
#    img[img <= threshold] = 0
#    img[img > threshold] = 255
#    return img
#
#def find_binary(img):
#    hist_cv = cv.calcHist([img], [0], None, [256], [0.0, 255.0])    
#    t = 254
#    flag = 0
#    tmp = 254
#    sum_ = 0 
#    while t > 0:
#        if hist_cv[t] != 0:
#            sum_ += hist_cv[t]
#            flag = 1
#        if flag == 1 and hist_cv[t] == 0:
#            if (sum_[0]/sum(hist_cv)[0]) > 0.003:
#                tmp = t
#                flag = 0
#                break
#        t = t - 1
#    return tmp
#
#	
#def iterabi(img,thre):
#    hist_cv = cv.calcHist([img],[0],None,[256],[0,256])
#    for i in range(thre+1):
#        hist_cv[0+i] = 0
#        hist_cv[255-i] = 0
#    
#    grey_val=np.zeros(256)
#    for i in range(256):
#        grey_val[i]=i/255
#    
#    
#    num=int(sum(sum(hist_cv))/2)
#    tmp=0
#    i=0
#    while tmp<num:
#        tmp+=hist_cv[i]
#        i+=1 
#    
#    thre = i
#    thre = thre/255
##    i=255
##    while 1:
##        if hist_cv[i]!=0:
##            hist_max=grey_val[i]
##            break
##        i-=1
##    
##    i=0
##    while 1:
##        if hist_cv[i]!=0:
##            hist_min=grey_val[i]
##            break
##        i+=1
##    
##    thre = (hist_max+hist_min)/2
#    
#    
#    
#    while 1:
#        up=np.zeros(256)
#        down=np.zeros(256)
#        
#        up[int(thre*255)+1:256]=1
#        down[0:int(thre*255)+1]=1
#        
#        up_ave=sum(sum(np.multiply(np.multiply(up,hist_cv),grey_val)))/sum(sum(np.multiply(up,hist_cv)))
#        down_ave=sum(sum(np.multiply(np.multiply(down,hist_cv),grey_val)))/sum(sum(np.multiply(down,hist_cv)))
#        
#        if (up_ave+down_ave)/2*255-thre*255<1:
#            return int((up_ave+down_ave)/2*255)
#        thre = (up_ave+down_ave)/2
#
#'''
#输入图像img,对其二值化处理,tmp_bianry是二值化的阈值
#'''
#def GrayToBinary(img):
#    tmp_binary = find_binary(img)
#    return gray2binary(img.copy(), tmp_binary)
#    
#    
#
#if __name__ == "__main__":
#    img = cv.imread('1.png')
#    img = GrayToBinary(img)
#    cv.imwrite("yuzhi.jpg", img)