from Wall import repoint
import cv2 as cv
import numpy as np
from Datastruct import Data_struct
import os
from Wall import Get_owner_wall
from Settings import Settings
min_radius_arc = Settings.min_radius_arc      #实际
max_radius_arc = Settings.max_radius_arc      #实际
max_arc_dis = Settings.max_arc_dis         #实际
max_search_point_dis = Settings.max_search_point_dis  #实际
max_points_num = Settings.max_points_num       #实际
max_dis_center = Settings.max_dis_center      #实际
max_search_wall = Settings.max_search_wall    #实际
max_width_wall = Settings.max_width_wall      #实际
min_width_wall = Settings.min_width_wall     #实际
thres_search_wall = Settings.thres_search_wall
thres_is_blank = Settings.thres_is_blank
thres_black_line = Settings.thres_black_line
def sobel_demo(image):
    grad_x = cv.Sobel(image, cv.CV_32F, 1, 0)   #对x求一阶导
    grad_y = cv.Sobel(image, cv.CV_32F, 0, 1)   #对y求一阶导
    gradx = cv.convertScaleAbs(grad_x)  #用convertScaleAbs()函数将其转回原来的uint8形式
    grady = cv.convertScaleAbs(grad_y)
    #cv.imwrite("gradient_x.jpg", gradx)  #x方向上的梯度
    #cv.imwrite("gradient_y.jpg", grady)  #y方向上的梯度
    gradxy = cv.addWeighted(gradx, 0.5, grady, 0.5, 0) #图片融合
    temp = gradxy.copy()
    gradxy[temp>Settings.sobel_thre] = 0
    gradxy[temp<=Settings.sobel_thre] = 255
    #hline = cv.getStructuringElement(cv.MORPH_RECT, (5, 1), (-1, -1)) 
    #vline = cv.getStructuringElement(cv.MORPH_RECT, (1, 2), (-1, -1))
   
    #res1 = cv.erode(gradxy, hline)
    #res1 = cv.erode(res1, vline)
    #res1 = cv.dilate(res1, hline)
#    temp = res1.copy()
#    res1[temp>40] = 0
#    res1[temp<=40] = 255
    return gradxy
def y_distance(x,y,img,prop):
    sum_dis = 0
    max_dis = 0
    count = 0
    for i in range(0+3,len(x)-3):
        if sum_dis > max_arc_dis*prop or count > max_points_num*prop:
#            if sum_dis > max_arc_dis*prop:
#                print('ysum',sum_dis)
#            if count > max_points_num*prop:
#                print('ycount',count)
            sum_dis = max_arc_dis * prop * 2
            count = max_points_num * prop * 2
            break
        a1 = np.maximum(y[i]-int(prop*max_search_point_dis),0)
        a2 = np.minimum(y[i]+int(prop*max_search_point_dis)+1,img.shape[0]-1)
        if x[i] >= img.shape[1] or y[i] >= img.shape[0]:
#            sum_dis += max_search_point_dis * 10
#            max_dis = max_search_point_dis * 10
            count += 1
        elif np.sum(img[a1:a2,x[i]]) >= (a2-a1)*255:
#            sum_dis += max_search_point_dis * 10
#            max_dis = max_search_point_dis * 10
            count += 1
        elif np.sum(img[a1:a2,x[i]]) <= 255:
#            sum_dis += max_search_point_dis * 10
#            max_dis = max_search_point_dis * 10
            count += 1
        else:
            for j in range(0,int(prop*max_search_point_dis)+1):
                a1 = np.maximum(y[i]-j,0)
                a2 = np.minimum(y[i]+j+1,img.shape[0]-1)
                if np.sum(img[a1:a2,x[i]]) < (2*j+1)*255:
                    sum_dis += j
                    if j > max_dis:
                         max_dis = j
                    break
    return sum_dis,max_dis,count
def x_distance(x,y,img,prop):
    sum_dis = 0
    max_dis = 0
    count = 0
    for i in range(0+3,len(x)-3):
        #print(sum_dis,count)
        if sum_dis > max_arc_dis*prop or count > max_points_num*prop:
#            if sum_dis > max_arc_dis*prop:
#                print('sum',sum_dis)
#            if count > max_points_num*prop:
#                print('count',count)
            sum_dis = max_arc_dis * prop * 2
            count = max_points_num * prop * 2
            break
        a1 = np.maximum(x[i]-int(prop*max_search_point_dis),0)
        a2 = np.minimum(x[i]+int(prop*max_search_point_dis)+1,img.shape[1]-1)
        if x[i] >= img.shape[1] or y[i] >= img.shape[0]:
#            sum_dis += max_search_point_dis * 10
#            max_dis = max_search_point_dis * 10
            count += 1
        elif np.sum(img[y[i],a1:a2]) >= (a2-a1)*255:
#            sum_dis += max_search_point_dis * 10
#            max_dis = max_search_point_dis * 10
            count += 1
            #print('bai',y[i],a1,a2)
        elif np.sum(img[y[i],a1:a2]) <= 255:
#            sum_dis += max_search_point_dis * 10
#            max_dis = max_search_point_dis * 10
            #print('hei')
            count += 1
        else:
            for j in range(0,int(prop*max_search_point_dis)+1):
                a1 = np.maximum(x[i]-j,0)
                a2 = np.minimum(x[i]+j+1,img.shape[1]-1)
                if np.sum(img[y[i],a1:a2]) < (a2-a1)*255:
                    sum_dis += j
                    if j > max_dis:
                         max_dis = j
                    break
    return sum_dis,max_dis,count
def cal_distance(x,y,img,prop):
    #print(center)
    x_sum_dis,x_max_dis,x_count = x_distance(x,y,img,prop)
    y_sum_dis,y_max_dis,y_count = y_distance(x,y,img,prop)
    sum_dis = np.maximum(x_sum_dis,y_sum_dis)
    max_dis = np.maximum(x_max_dis,y_max_dis)
    count = np.maximum(x_count,y_count)
    #print('a',sum_dis,max_dis,count)
    return sum_dis,max_dis,count
def is_near_wall(point,img,prop):
    x_max = img.shape[1] - 1
    y_max = img.shape[0] - 1
    a1 = np.maximum(0,point[0]-int(max_search_wall*prop))
    a2 = np.minimum(x_max,point[0]+int(max_search_wall*prop))
    b1 = np.maximum(0,point[1]-int(max_search_wall*prop))
    b2 = np.minimum(y_max,point[1]+int(max_search_wall*prop))
    #print(a1,a2,b1,b2)
    #print(np.sum(img[int(b1):int(b2),int(a1):int(a2)]),(a2-a1),(b2-b1))
    if np.sum(img[int(b1):int(b2),int(a1):int(a2)]) <= thres_search_wall * (a2-a1) * (b2-b1) * 255:
        return True
    else:
        return False
def is_blank(line,img,prop):
    x_max = img.shape[1] - 1
    y_max = img.shape[0] - 1
    if line[0] == line[2]:
        a1 = np.maximum(0,line[0]-int(max_search_wall*prop))
        a2 = np.minimum(x_max,line[0]+int(max_search_wall*prop))
        b1 = np.minimum(line[1],line[3]) + 3
        b2 = np.maximum(line[1],line[3]) - 3
        if np.sum(img[int(b1):int(b2),int(a1):int(a2)]) > thres_is_blank * (a2-a1) * (b2-b1) * 255:
            return True
    if line[1] == line[3]:
        b1 = np.maximum(0,line[1]-int(max_search_wall*prop))
        b2 = np.minimum(y_max,line[1]+int(max_search_wall*prop))
        a1 = np.minimum(line[0],line[2]) + 3
        a2 = np.maximum(line[0],line[2]) - 3
        if np.sum(img[int(b1):int(b2),int(a1):int(a2)]) > thres_is_blank * (a2-a1) * (b2-b1) * 255:
            return True
    return False
def is_valid_radius(line,img,prop):
    flag1 = is_near_wall(line[0:2],img,prop)
    flag2 = is_near_wall(line[2:4],img,prop)
    #if line[0] == 857 and line[1] == 376:
        #print(flag1,flag2)
    x_max = img.shape[1]
    y_max = img.shape[0]
    if flag1 and flag2:
        if is_blank(line,img,prop):
            return True
#    if flag1 == False and flag2 == False:
#        return False
#    if flag2:
#        line = [line[2],line[3],line[0],line[1]]
#    if line[0] == line[2]:
#        if line[1] > line[3]:
#            for i in range(int(min_radius_arc*prop),int(max_radius_arc*prop)):
#                if line[3] - i >= 0:
#                    if is_near_wall([line[2],line[3]-i],img,prop):
#                        if is_blank([line[2],line[3]-i,line[0],line[1]],img,prop):
#                            return True
#        else:
#            for i in range(int(min_radius_arc*prop),int(max_radius_arc*prop)):
#                if line[3] + i < y_max:
#                    if is_near_wall([line[2],line[3]+i],img,prop):
#                        if is_blank([line[0],line[1],line[2],line[3]+i],img,prop):
#                            return True
#    if line[1] == line[3]:
#        if line[0] > line[2]:
#            for i in range(int(min_radius_arc*prop),int(max_radius_arc*prop)):
#                if line[2] - i >= 0:
#                    if is_near_wall([line[2]-i,line[3]],img,prop):
#                        if is_blank([line[2]-i,line[3],line[0],line[1]],img,prop):
#                            return True
#        else:
#            for i in range(int(min_radius_arc*prop),int(max_radius_arc*prop)):
#                if line[2] + i < x_max:
#                    if is_near_wall([line[2]+i,line[3]],img,prop):
#                        if is_blank([line[0],line[1],line[2]+i,line[3]],img,prop):
#                            return True
    return False
def find_arc(center,grad_img,wall_img,prop):
    x_max = grad_img.shape[1]
    y_max = grad_img.shape[0]
    lines = []
    min_dis = np.ones((4,)) * max_arc_dis * prop * 10
    point_dis = np.ones((4,)) * max_search_point_dis * prop * 10
    min_count = np.ones((4,)) * max_points_num * prop * 10
    best_radius = np.zeros((4,))
    for r in range(int(min_radius_arc*prop),int(max_radius_arc*prop)):
#        centers = []
#        centers.append(center)
#        if center[0] - r >= 0:
#            centers.append([center[0]-r,center[1]])
#        else:
#            centers.append([])
#        if center[0] + r < x_max:
#            centers.append([center[0]+r,center[1]])
#        else:
#            centers.append([])
#        if center[1] - r >= 0:
#            centers.append([center[0],center[1]-r])
#        else:
#            centers.append([])
#        if center[1] + r < y_max:
#            centers.append([center[0],center[1]+r])
#        else:
#            centers.append([])
#        num1 = len(centers)
#        for i in range(num1):
#            if center[i] == []:
#                continue
        arc_points = []
        x = [i for i in range(0,r+1)]
        y = [ int(i) for i in (np.sqrt(np.power(r,2) - np.power(np.array(x),2)))]
        if center[0] + r < x_max and center[1] + r < y_max:    
            x1 = center[0] + x
            y1 = center[1] + y
            arc_points.append(x1)
            arc_points.append(y1)
        else:
            arc_points.append([])
            arc_points.append([])
        if center[0] + r < x_max and center[1] - r >= 0:    
            x1 = center[0] + x
            y1 = center[1] - y
            arc_points.append(x1)
            arc_points.append(y1)
        else:
            arc_points.append([])
            arc_points.append([])
        if center[0] - r >= 0 and center[1] + r < y_max:    
            x1 = center[0] - x
            y1 = center[1] + y
            arc_points.append(x1)
            arc_points.append(y1)
        else:
            arc_points.append([])
            arc_points.append([])
        if center[0] - r >= 0 and center[1] - r >= 0:    
            x1 = center[0] - x
            y1 = center[1] - y
            arc_points.append(x1)
            arc_points.append(y1)
        else:
            arc_points.append([])
            arc_points.append([])
        for j in range(0,4):
            if arc_points[2*j] == []:
                continue
            dis1,dis2,count = cal_distance(arc_points[2*j],arc_points[2*j+1],grad_img,prop)
            if dis1 < min_dis[j] and count < max_points_num * prop:
                min_dis[j] = dis1
                point_dis[j] = dis2
                min_count[j] = count
                best_radius[j] = r
    #if center[0] == 312 and center[1] == 303:
        #print(min_dis,min_count)
    for j in range(0,4):
        if min_dis[j] < max_arc_dis*prop and min_count[j] < max_points_num*prop:
            if j == 0:
                lines.append([center[0],center[1],center[0]+int(best_radius[j]),center[1],1,0])
                lines.append([center[0],center[1],center[0],center[1]+int(best_radius[j]),1,1])
            if j == 1:
                lines.append([center[0],center[1],center[0]+int(best_radius[j]),center[1],0,0])
                lines.append([center[0],center[1],center[0],center[1]-int(best_radius[j]),1,0])
            if j == 2:
                lines.append([center[0],center[1],center[0]-int(best_radius[j]),center[1],1,1])
                lines.append([center[0],center[1],center[0],center[1]+int(best_radius[j]),0,1])
            if j == 3:
                lines.append([center[0],center[1],center[0]-int(best_radius[j]),center[1],0,1])
                lines.append([center[0],center[1],center[0],center[1]-int(best_radius[j]),0,0])
    #print(center,lines)
    i = 0
    while i < len(lines):
        if is_valid_radius(lines[i],wall_img,prop) == False:
            lines.remove(lines[i])
            i = i - 1
        i = i + 1
    #print('valid',lines)
    return lines
def point_distance(point,line):
    dis1 = np.abs(point[0]-line[0]) + np.abs(point[1]-line[1])
    #dis2 = np.abs(point[0]-line[2]) + np.abs(point[1]-line[3])
    #dis = np.minimum(dis1,dis2)
    return dis1
def is_exist(point,lines,prop):
    num1 = len(lines)
    for i in range(0,num1):
        if point_distance(point,lines[i]) < max_dis_center*prop:
            return True
    return False
def draw_line(res,img):
    img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
    for i in range(0,len(res)):
        cv.line(img, (res[i][0],res[i][1]), (res[i][2],res[i][3]), (37,193,255), 2) 
    return img
def draw_rect(list_wall,img):
    #img[0:len(img),0:len(img[0])] = 255
    img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
    for i in range(0,len(list_wall)):
        if np.abs(list_wall[i][0] - list_wall[i][2])<=2:
            x1 = list_wall[i][0] - list_wall[i][4]
            y1 = list_wall[i][1]
            x2 = list_wall[i][2] + list_wall[i][5]
            y2 = list_wall[i][3]
            cv.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
        else:
            x1 = list_wall[i][0]
            y1 = list_wall[i][1] - list_wall[i][4]
            x2 = list_wall[i][2]
            y2 = list_wall[i][3] + list_wall[i][5]
            cv.rectangle(img,(x1,y1),(x2,y2),(255,0,0),2)
    return img 
def find_wall(point,direction,img,prop):
    x_max = img.shape[1] - 1
    y_max = img.shape[0] - 1
    point1 = 0
    point2 = 0
    for i in range(int(min_width_wall*prop),int(max_radius_arc*prop)):
        if direction == 0:
            x = point[0]
            y = np.maximum(point[1] - i,0)
        elif direction == 1:
            x = np.minimum(point[0] + i,x_max)
            y = point[1]
        elif direction == 2:
            x = point[0]
            y = np.minimum(point[1] + i,y_max)
        else:
            x = np.maximum(point[0]-i,0)
            y = point[1]
        if direction == 0 or direction == 2:
            a1 = np.maximum(x-int(max_search_wall*prop),0)
            a2 = np.minimum(x+int(max_search_wall*prop),x_max)

            if np.sum(img[y,a1:a2]) < (a2-a1) * 255 - 3:#thres_black_line * (a2-a1) * 255 - 2:
                for j in range(a1,a2):
                    if img[y,j] == 0:
                        break
                temp1 = False
                temp2 = False
                for k in range(0,int(max_width_wall*prop) + 5):
                    if j-k >= 0 and temp1 == False:
                        if img[y,j-k] == 255:
                            point1 = j-k+1
                            temp1 = True
                    if j+k < x_max and temp2 == False:
                        if img[y,j+k] == 255:
                            point2 = j+k-1
                            temp2 = True
                    if temp1 and temp2:
                        break
                #print('1 phase',point1,point2,x,y,j,k)
                if (point2 - point1)<min_width_wall*prop:
                    temp1 = False
                    temp2 = False
                    for k in range(0,a2-a1+1):
                        if temp1 == False and img[y,a1+k] == 0:
                            point1 = a1+k
                            temp1 = True
                        if temp2 == False and img[y,a2-k] == 0:
                            point2 = a2-k
                            temp2 = True
                        if temp1 and temp2:
                            break
                if temp1 == False:
                    point1 = np.maximum(j - int(max_width_wall*prop),0)
                if temp2 == False:
                    point2 = np.minimum(j + int(max_width_wall*prop),x_max)
                #print('2 phase',point1,point2,x,y,j,k)
                
                #print(point,y,point1,point2,j)
                return [x,y],[int((point1+point2)/2),y,int((point1+point2)/2)-point1,point2-int((point1+point2)/2)]
        elif direction == 1 or direction == 3:
            b1 = np.maximum(y-int(max_search_wall*prop),0)
            b2 = np.minimum(y+int(max_search_wall*prop),y_max)   
#            if point[0] == 550 and point[1] == 238:
#                print(x,np.sum(img[b1:b2,x]),(b2-b1) * 255)
            if np.sum(img[b1:b2,x]) < (b2-b1) * 255 - 3:#thres_black_line * (b2-b1) * 255:
 #               print('ha')
                for j in range(b1,b2):
                    if img[j,x] == 0:
                        break
#                print(1)
                temp1 = False
                temp2 = False
                for k in range(0,int(max_width_wall*prop) + 5):
                    if j-k >= 0 and temp1 == False:
                        if img[j-k,x] == 255:
                            point1 = j-k+1
                            temp1 = True
                            #print(2)
                    if j+k < y_max and temp2 == False:
                        if img[j+k,x] == 255:
                            point2 = j+k-1
                            temp2 = True
                            #print(3)
                    if temp1 and temp2:
                        break
                #print('1 phase',point1,point2,x,y,j,k)
                if (point2 - point1)<min_width_wall*prop:
                    temp1 = False
                    temp2 = False
                    for k in range(0,b2-b1+1):
                        if temp1 == False and img[b1+k,x] == 0:
                            point1 = b1+k
                            temp1 = True
                        if temp2 == False and img[b2-k,x] == 0:
                            point2 = b2-k
                            temp2 = True
                        if temp1 and temp2:
                            break
                if temp1 == False:
                    point1 = np.maximum(j - int(max_width_wall*prop),0)
                if temp2 == False:
                    point2 = np.minimum(j + int(max_width_wall*prop),y_max)
                #print('2 phase',point1,point2,x,y,j,k)
                #if (point2 - point1)>min_width_wall*prop and (point2 - point1)<max_width_wall*prop:
 #               print(point,x,point1,point2,j)
                return [x,y],[x,int((point1+point2)/2),int((point1+point2)/2)-point1,point2-int((point1+point2)/2)]
    return -1,-1
def intersection(a1,a2,b1,b2):
    temp1 = np.maximum(a1,b1)
    temp2 = np.minimum(a2,b2)
    return np.maximum(temp2-temp1,0)
def coordinate(middleline):
    if abs(middleline[0] - middleline[2])<=2:
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
def distance(rect1,rect2):
    dis1 = coor_dis(rect1[0],rect1[2],rect2[0],rect2[2])
    dis2 = coor_dis(rect1[1],rect1[3],rect2[1],rect2[3])
    return np.sqrt(np.power(dis1,2) + np.power(dis2,2))
def coor_dis(a1,a2,b1,b2):
    temp1 = np.maximum(a1,b1)
    temp2 = np.minimum(a2,b2)
    return np.maximum(temp1-temp2,0)
def remove_repetition(rect,prop):
    i = 0
    while i < len(rect):
        line1 = rect[i]
        x1,x2,y1,y2 = coordinate(line1)
        temp = rect.copy()
        temp.pop(i)
        for j in range(0,len(temp)):
            a1,a2,b1,b2 = coordinate(temp[j])
            area1 = (x2-x1)*(y2-y1)
            area2 = (a2-a1)*(b2-b1)
            inter1 = intersection(a1,a2,x1,x2)
            inter2 = intersection(b1,b2,y1,y2)
            inter_area = inter1*inter2
            #dis = distance((x1,y1,x2,y2),(a1,b1,a2,b2))
            #flag = (inter1/np.minimum(a2-a1,x2-x1) > 0.8 or inter2/np.minimum(b2-b1,y2-y1) > 0.8)
            if (inter_area)/np.minimum(area1,area2) > 0.45: #or (dis < 5 and flag): #or np.maximum(x2-x1,y2-y1)/prop > normal_door_width_max:
                rect.pop(i)
                i = i-1
                break
        i = i+1
    return rect
def get_middle_line(lines,img,prop):
    num1 = len(lines)
#    print(lines)
    rect = []
    for i in range(0,num1):
        #print('rect',lines[i],rect)
        if lines[i][0] == lines[i][2]:
            if lines[i][1] > lines[i][3]:
                lines[i] = [lines[i][0],lines[i][3],lines[i][2],lines[i][1],lines[i][4],lines[i][5]]
            middle_y = int((lines[i][1] + lines[i][3])/2)
            _,top = find_wall([lines[i][0],middle_y],0,img,prop)
            _,bottom = find_wall([lines[i][0],middle_y],2,img,prop)
            #print(top,bottom)
            #print([lines[i][0],middle_y],top,bottom)
            if top != -1 and bottom != -1:
                if top[2]+top[3] < bottom[2] + bottom[3]:
                    if top[2]+top[3] < max_width_wall*prop and top[2]+top[3] > min_width_wall*prop:
                        rect.append([top[0],top[1],top[0],bottom[1],top[2],top[3],lines[i][4],lines[i][5]])
                else:
                    if bottom[2]+bottom[3] < max_width_wall*prop and bottom[2]+bottom[3] > min_width_wall*prop:
                        rect.append([bottom[0],top[1],bottom[0],bottom[1],bottom[2],bottom[3],lines[i][4],lines[i][5]])
        elif lines[i][1] == lines[i][3]:
            if lines[i][0] > lines[i][2]:
                lines[i] = [lines[i][2],lines[i][1],lines[i][0],lines[i][3],lines[i][4],lines[i][5]]
            middle_x = int((lines[i][0] + lines[i][2])/2)
            _,left = find_wall([middle_x,lines[i][1]],3,img,prop)
            _,right = find_wall([middle_x,lines[i][1]],1,img,prop)
            if left != -1 and right != -1:
                if left[2]+left[3] < right[2] + right[3]:
                    if left[2]+left[3] < max_width_wall*prop and left[2]+left[3] > min_width_wall*prop:
                        rect.append([left[0],left[1],right[0],left[1],left[2],left[3],lines[i][4],lines[i][5]])
                else:
                    if right[2]+right[3] < max_width_wall*prop and right[2]+right[3] > min_width_wall*prop:
                        rect.append([left[0],right[1],right[0],right[1],right[2],right[3],lines[i][4],lines[i][5]])
    return rect
def Door_detect(nonbearwall,bearwall,img,wall_img,prop):
    grad_img = sobel_demo(img)
    list_nonb = []
    nonb_contours = nonbearwall.out_contour()
    bear_contours = bearwall.out_contour()
    nonb_contours = repoint.remove_re_point(nonb_contours)
    bear_contours = repoint.remove_re_point(bear_contours)
    for i in range(0,len(nonb_contours)):
        new_contour = nonb_contours[i].reshape(len(nonb_contours[i]),len(nonb_contours[i][0][0]))
        list_nonb.append(new_contour)
    for i in range(0,len(bear_contours)):
        new_contour = bear_contours[i].reshape(len(bear_contours[i]),len(bear_contours[i][0][0]))
        list_nonb.append(new_contour)
    #print(list_nonb)
    res = []
    for i in range(0,len(list_nonb)):
        for j in range(0,len(list_nonb[i])):
            center = list_nonb[i][j,:]
#            if center[0] != 483 or center[1] != 185:
#                continue
            if res != []:
                if is_exist(center,res,prop):
                    continue
            lines = find_arc(center,grad_img,wall_img,prop)      
            res += lines
            for k in range(0,4):
                derive_center,_ = find_wall(center,k,wall_img,prop)
                #print('derive',derive_center)
                if derive_center != -1:
                    #                continue
                    if res != []:
                        if is_exist(derive_center,res,prop):
                            continue
                    lines = find_arc(derive_center,grad_img,wall_img,prop)      
                    res += lines
#                    if derive_center[0] != 446 or derive_center[1] != 178:
#                        continue
            #print('res',res)
    res = get_middle_line(res,wall_img,prop)
    #print(res)
    img = draw_rect(res,img)
    
    single_base_position=[]
    single_Xflip=[]
    single_Yflip=[]
    single_door_id=[]
    res = remove_repetition(res,prop)
    for i in range(len(res)):
        single_base_position.append((res[i][0],res[i][1],res[i][2],res[i][3],res[i][4],res[i][5]))
        single_Xflip.append(res[i][6])
        single_Yflip.append(res[i][7])
        single_door_id.append(Get_owner_wall.Get_owner_wall((res[i][0],res[i][1],res[i][2],res[i][3],res[i][4],res[i][5]),bearwall,nonbearwall))
        
    single_door=Data_struct.Door()
    single_door.set_type(0)
    single_door.add_base_position(single_base_position)
    single_door.add_Xflip(single_Xflip)
    single_door.add_Yflip(single_Yflip)
    single_door.add_door_id(single_door_id) 
    
    #return res,img
    return single_door,img
                 
            