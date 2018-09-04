# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 15:54:18 2018

@author: 王科涛
"""

import numpy as np
import cv2
def is_line(i, j):
    if i[0] == j[0] or i[1] == j[1]:
        return 1
    else:
        return 0


def distance(a, b):
    x1, y1 = a
    x2, y2 = b
    return int(((y2 -y1)**2 + (x2 - x1)**2)**0.5)

#img = cv2.imread('4.png')  
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  
#ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)  
#  
#img, contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  

def remove_re_point(contours):
    new_contours = []
    for i in range(len(contours)):
        list3 = []
        for j in range(len(contours[i])):
            k_i = j % len(contours[i])
            k_j = (j + 1) % len(contours[i])
            if is_line([contours[i][k_i][0][0], contours[i][k_i][0][1]], [contours[i][k_j][0][0], contours[i][k_j][0][1]]) == 0 and distance((contours[i][k_i][0][0], contours[i][k_i][0][1]), (contours[i][k_j][0][0], contours[i][k_j][0][1])) < 3:
                x_i = contours[i][k_i][0][0]
                y_i = contours[i][k_i][0][1]
                x_j = contours[i][k_j][0][0]
                y_j = contours[i][k_j][0][1]
                k_1 = (j-1) % len(contours[i])
                k_2 = (j + 2) % len(contours[i])
                x_1 = contours[i][k_1][0][0]
                y_1 = contours[i][k_1][0][1]
                x_2 = contours[i][k_2][0][0]
                y_2 = contours[i][k_2][0][1]
                if (x_1 == x_i or x_2 == x_j) and (y_1 == y_i or y_2 == y_j):
                    list1 = []
                    list2 = []
                    if x_1 == x_i:
                        list1.append(x_i)
                    elif x_2 == x_j:
                        list1.append(x_j)
                    if y_1 == y_i:
                        list1.append(y_i)
                    elif y_2 == y_j:
                        list1.append(y_j)
                    list2.append(np.array(list1))
                    list3.append(np.array(list2))
                else:
                    if x_j > x_i and y_j < y_i:
                        list1 = []
                        list2 = []
                        list1.append(x_i)
                        list1.append(y_j)
                        list2.append(np.array(list1))
                        list3.append(np.array(list2))
                    elif x_j > x_i and y_j > y_i:
                        list1 = []
                        list2 = []
                        list1.append(x_j)
                        list1.append(y_i)
                        list2.append(np.array(list1))
                        list3.append(np.array(list2))
                    elif x_j < x_i and y_j > y_i:
                        list1 = []
                        list2 = []
                        list1.append(x_i)
                        list1.append(y_j)
                        list2.append(np.array(list1))
                        list3.append(np.array(list2))
                    elif x_j < x_i and y_j < y_i:
                        list1 = []
                        list2 = []
                        list1.append(x_j)
                        list1.append(y_i)
                        list2.append(np.array(list1))
                        list3.append(np.array(list2))
        list4 = []
        for j in range(len(contours[i])):
            judge = 1
            for k in range(len(list3)):
                if distance((contours[i][j][0][0], contours[i][j][0][1]), (list3[k][0][0], list3[k][0][1])) < 3:
                    list4.append(np.array(list3[k]))
                    judge = 0
                    break
            if judge == 1:
                list4.append(np.array(contours[i][j]))
        while(1):
            judge = -1
            for j in range(len(list4)-1):
                for k in range(j+1, len(list4)):
                    if list4[j][0][0] == list4[k][0][0] and list4[j][0][1] == list4[k][0][1]:
                        judge = k
                        break
            if judge == -1:
                break
            else:
                list4.pop(judge)
                        
            
        new_contours.append(np.array(list4))
    list_contours = []
    for i in range(0,len(new_contours)):            
        new_contour = new_contours[i].reshape(len(new_contours[i]),len(new_contours[i][0][0]))
        list_contours.append(new_contour)
    res = []
    for i in range(0,len(list_contours)): 
        j = 0
        temp = list_contours[i].copy().tolist()
        while j < len(temp) and len(temp) > 3:
            num = len(temp)
            if np.maximum(np.abs(temp[j][0]-temp[(j+1)%num][0]),np.abs(temp[(j+1)%num][0]-temp[(j+2)%num][0])) <= 2:
                temp.remove(temp[(j+1)%num])
                j = j-1
            elif np.maximum(np.abs(temp[j][1]-temp[(j+1)%num][1]),np.abs(temp[(j+1)%num][1]-temp[(j+2)%num][1])) <= 2:
                temp.remove(temp[(j+1)%num])
                j = j-1
            j = j + 1
        one_contour = []
        for k in range(0,len(temp)):
            one_contour.append([[temp[k][0],temp[k][1]]])
        res.append(np.array(one_contour))

    return res



if __name__ == "__main__":
    img = cv2.imread('4.png')  
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  
    ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)  
      
    img, contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  
    new_contours = remove_re_point(contours)
    img[0:len(img), 0:len(img[0])] = 255
    cv2.drawContours(img,new_contours,-1,(0,0,255),1)  
    # 
    cv2.imwrite("bearwall.png", img)