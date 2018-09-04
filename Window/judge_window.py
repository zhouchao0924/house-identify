# -*- coding: utf-8 -*-

import cv2
from Wall import Get_owner_wall
from Window import window
import numpy as np
from Datastruct import Data_struct

def is_line(init_img,pointA, pointB):
    x_A,y_A = pointA
    x_B,y_B = pointB
    if x_A==x_B and y_A==y_B:
        return False
    if x_A!=x_B and y_A!=y_B:
        return False
    
    if x_A<0 or x_B<0 or y_A<0 or y_B<0:
        return False
    
    tmp_img=init_img[min(x_A,x_B):max(x_A,x_B)+1,min(y_A,y_B):max(y_A,y_B)+1]
    return (sum(sum(tmp_img))==0)
    
def draw_rect(filename,mincc_win,minrr_win,maxcc_win,maxrr_win,color):
    new_img=cv2.imread(filename)
    for i in range(len(mincc_win)):
        cv2.rectangle(new_img, (mincc_win[i],minrr_win[i]), (maxcc_win[i],maxrr_win[i]), color, 3)
    return new_img

def check_iou(list_A,list_B):#检测两个矩形是否相交
    mincc_A = list_A[0]
    minrr_A = list_A[1]
    maxcc_A = list_A[2]
    maxrr_A = list_A[3]
    mincc_B = list_B[0]
    minrr_B = list_B[1]
    maxcc_B = list_B[2]
    maxrr_B = list_B[3]
    
    if maxcc_A < mincc_B or mincc_A > maxcc_B or maxrr_A < minrr_B or minrr_A > maxrr_B:
        return 0
    return 1

def get_new_points(init_img,pointA, pointB):#vol==0 x相同   vol==1 y相同
    A_x,A_y = pointA
    B_x,B_y = pointB
    
    if A_x==B_x:
        vol=0
    if A_y==B_y:
        vol=1
    
    if vol==0:
        beg=min(A_y,B_y)
        while 1:
            if init_img[A_x,beg]==0 and init_img[A_x,beg+1]==255:
                break
            beg+=1
        new_mincc=beg
        beg=max(A_y,B_y)
        while 1:
            if init_img[A_x,beg]==0 and init_img[A_x,beg-1]==255:
                break
            beg-=1
        new_maxcc=beg
        new_pointA=(A_x,new_mincc)
        new_pointB=(B_x,new_maxcc)
        return new_pointA, new_pointB
    else:
        beg=min(A_x,B_x)
        while 1:
            if init_img[beg,A_y]==0 and init_img[beg+1,A_y]==255:
                break
            beg+=1
        new_minrr=beg
        beg=max(A_x,B_x)
        while 1:
            if init_img[beg,A_y]==0 and init_img[beg-1,A_y]==255:
                break
            beg-=1
        new_maxrr=beg
        new_pointA=(new_minrr,A_y)
        new_pointB=(new_maxrr,B_y)
        return new_pointA, new_pointB

def check_line(init_img, pointA, pointB, my_dir,thre):#my_dir==-1 减    #my_dir==1 加 
    A_x,A_y = pointA
    B_x,B_y = pointB
    vol=0
    if A_x==B_x:
        vol=0
    if A_y==B_y:
        vol=1
        
    res=0
    line_index=-1
    beg=0
    if vol==0:
        beg=A_x
        tmp_img=init_img[:,min(A_y,B_y):(max(A_y,B_y)+1)]
        tmp_sum_img=np.sum(tmp_img,axis=1)
        list_sum_img = tmp_sum_img.tolist()
        flag=0
        count=0
        while count<thre:
            beg = beg + my_dir
            if flag==0 and list_sum_img[beg]!=0:
                flag=1
            if flag==1 and list_sum_img[beg]==0:
                #return 1
                line_index=beg
                res=1
                break
            count = count + 1
    else:
        beg=A_y
        tmp_img=init_img[min(A_x,B_x):(max(A_x,B_x)+1),:]
        tmp_sum_img=np.sum(tmp_img,axis=0)
        list_sum_img = tmp_sum_img.tolist()
        flag=0
        count=0
        while count<thre:
            beg = beg + my_dir
            if flag==0 and list_sum_img[beg]!=0:
                flag=1
            if flag==1 and list_sum_img[beg]==0:
                #return 1
                line_index=beg
                res=1
                break
            count = count + 1
            
    if vol==0:
        pointA2=(beg,A_y)
        pointB2=(beg,B_y)
    else:
        pointA2=(A_x,beg)
        pointB2=(B_x,beg)
        
    if not (is_line(init_img,pointA, pointA2) and is_line(init_img,pointB, pointB2)):
        res=0
        line_index=-1
            
    return res,line_index

#thres1:飘窗纵深
#thres2:推拉门和阳台距离
def judge_window_type(room_img,init_img,wall_img,sliding_door,bear_wall,nonbearwall,mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win, mincc_two_piao, minrr_two_piao, maxcc_two_piao, maxrr_two_piao,thres1,thres2,prop,is_drawing):
    new_img = cv2.cvtColor(room_img.copy(), cv2.COLOR_GRAY2RGB)
#    
#    init_img = Binarization.Binary(new_img,Settings.threshold)
    list_pos=sliding_door.out_base_position()
    
    list_slidingdoor=[]
    
    for i in range(len(list_pos)):
        a_x,a_y,b_x,b_y,dis_1,dis_2=list_pos[i]
        if a_x==b_x:
            list_slidingdoor.append((a_x-dis_1,a_y,b_x+dis_2,b_y))
        elif a_y==b_y:
            list_slidingdoor.append((a_x,a_y-dis_1,b_x,b_y+dis_2))
        else:
            pass

    minrr_slidingdoor=[]#y坐标
    mincc_slidingdoor=[]#x坐标
    maxrr_slidingdoor=[]#y坐标
    maxcc_slidingdoor=[]#x坐标
    for i in range(len(list_slidingdoor)):
        tmp=list_slidingdoor[i]
        minrr_slidingdoor.append(tmp[1])#y坐标
        mincc_slidingdoor.append(tmp[0])#x坐标
        maxrr_slidingdoor.append(tmp[3])#y坐标
        maxcc_slidingdoor.append(tmp[2])#x坐标
    
#    mincc_rect, minrr_rect, maxcc_rect, maxrr_rect = Windows_decoration.get_rect_corner_position(init_img.copy(), 200, 100)
#    mincc_three_rect_win, minrr_three_rect_win, maxcc_three_rect_win, maxrr_three_rect_win, img_three_rect_win, biaohao_rect = Windows_decoration.detect_three_rect_followup_windows(init_img.copy(), wall_img.copy(), mincc_rect, minrr_rect, maxcc_rect, maxrr_rect, 20, 2.0, 15, prop, 70, 300, 2.0)
#    mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win, img_two_rect_win, biaohao_rect = Windows_decoration.detect_two_rect_windows(init_img.copy(), wall_img.copy(), biaohao_rect, mincc_rect, minrr_rect, maxcc_rect, maxrr_rect, 20, 2.0, 15, prop, 70, 300)
#    
#    mincc_ban, minrr_ban, maxcc_ban, maxrr_ban = Windows_decoration.get_ban_corner_position(init_img.copy(), 200, 0.3)
#    mincc_three_rect_ban_win, minrr_three_rect_ban_win, maxcc_three_rect_ban_win, maxrr_three_rect_ban_win, img_three_rect_ban_win, biaohao_ban = Windows_decoration.detect_three_rect_ban_windows(init_img.copy(), mincc_ban, minrr_ban, maxcc_ban, maxrr_ban, 5, prop, 70, 300)
#    mincc_two_rect_ban_win, minrr_two_rect_ban_win, maxcc_two_rect_ban_win, maxrr_two_rect_ban_win, img_two_rect_ban_win, biaohao_ban = Windows_decoration.detect_two_rect_ban_windows(init_img.copy(), wall_img.copy(), biaohao_ban, mincc_ban, minrr_ban, maxcc_ban, maxrr_ban, 5, prop, 70, 300)
#    
#    mincc_piao, minrr_piao, maxcc_piao, maxrr_piao = Windows_decoration.get_piao_corner_position(init_img.copy(), 200, 0.4)
#    mincc_three_piao, minrr_three_piao, maxcc_three_piao, maxrr_three_piao, img_three_piao_win, biaohao_piao = Windows_decoration.detect_three_piao_windows(init_img.copy(), mincc_piao, minrr_piao, maxcc_piao, maxrr_piao, 5, 10, prop, 70, 300)
#    mincc_two_piao, minrr_two_piao, maxcc_two_piao, maxrr_two_piao, img_two_piao_win, biaohao_piao = Windows_decoration.detect_two_piao_windows(init_img.copy(), wall_img.copy(), biaohao_piao, mincc_piao, minrr_piao, maxcc_piao, maxrr_piao, 5, 10, prop, 70, 300)
#    
    #img_two_rect_win, img_two_piao_win, mincc_two_rect_win, minrr_two_rect_win, maxcc_two_rect_win, maxrr_two_rect_win, mincc_two_piao, minrr_two_piao, maxcc_two_piao, maxrr_two_piao = window.Windows_detect(init_img.copy(), 1/prop, single_door)

    mincc_three_rect_win=[]
    minrr_three_rect_win=[]
    maxcc_three_rect_win=[]
    maxrr_three_rect_win=[]
    mincc_three_rect_ban_win=[]
    minrr_three_rect_ban_win=[]
    maxcc_three_rect_ban_win=[]
    maxrr_three_rect_ban_win=[]
    mincc_three_piao=[]
    minrr_three_piao=[]
    maxcc_three_piao=[]
    maxrr_three_piao=[]
    mincc_two_rect_ban_win=[]
    minrr_two_rect_ban_win=[]
    maxcc_two_rect_ban_win=[]
    maxrr_two_rect_ban_win=[]
    
    mincc_win=[]
    minrr_win=[]
    maxcc_win=[]
    maxrr_win=[]
    two_mincc_win=[]
    two_minrr_win=[]
    two_maxcc_win=[]
    two_maxrr_win=[]
    
    for i in range(len(mincc_three_rect_win)):
        mincc_win.append(mincc_three_rect_win[i])
        minrr_win.append(minrr_three_rect_win[i])
        maxcc_win.append(maxcc_three_rect_win[i])
        maxrr_win.append(maxrr_three_rect_win[i])
        
    for i in range(len(mincc_three_rect_ban_win)):
        mincc_win.append(mincc_three_rect_ban_win[i])
        minrr_win.append(minrr_three_rect_ban_win[i])
        maxcc_win.append(maxcc_three_rect_ban_win[i])
        maxrr_win.append(maxrr_three_rect_ban_win[i])
        
    for i in range(len(mincc_three_piao)):
        mincc_win.append(mincc_three_piao[i])
        minrr_win.append(minrr_three_piao[i])
        maxcc_win.append(maxcc_three_piao[i])
        maxrr_win.append(maxrr_three_piao[i])
        
    #两层
    for i in range(len(mincc_two_rect_win)):
        two_mincc_win.append(mincc_two_rect_win[i])
        two_minrr_win.append(minrr_two_rect_win[i])
        two_maxcc_win.append(maxcc_two_rect_win[i])
        two_maxrr_win.append(maxrr_two_rect_win[i])
        
    for i in range(len(mincc_two_rect_ban_win)):
        two_mincc_win.append(mincc_two_rect_ban_win[i])
        two_minrr_win.append(minrr_two_rect_ban_win[i])
        two_maxcc_win.append(maxcc_two_rect_ban_win[i])
        two_maxrr_win.append(maxrr_two_rect_ban_win[i])
        
    for i in range(len(mincc_two_piao)):
        two_mincc_win.append(mincc_two_piao[i])
        two_minrr_win.append(minrr_two_piao[i])
        two_maxcc_win.append(maxcc_two_piao[i])
        two_maxrr_win.append(maxrr_two_piao[i])
        
    ###############################
    tmp_mincc_win=mincc_win.copy()
    tmp_minrr_win=minrr_win.copy()
    tmp_maxcc_win=maxcc_win.copy()
    tmp_maxrr_win=maxrr_win.copy()
    
    for i in range(len(mincc_slidingdoor)):
        tmp_mincc_win.append(mincc_slidingdoor[i])
        tmp_minrr_win.append(minrr_slidingdoor[i])
        tmp_maxcc_win.append(maxcc_slidingdoor[i])
        tmp_maxrr_win.append(maxrr_slidingdoor[i])
        
    for j in range(len(two_mincc_win)):
        mincc_win.append(two_mincc_win[j])
        minrr_win.append(two_minrr_win[j])
        maxcc_win.append(two_maxcc_win[j])
        maxrr_win.append(two_maxrr_win[j])
    ###############################
#    new_img = draw_rect(filename,two_mincc_win,two_minrr_win,two_maxcc_win,two_maxrr_win,(0,0,255))
#    cv2.imwrite('my_img.jpg', new_img)
#    aaaa=[]
#    for i in range(len(mincc_win)):
#        aaaa.append([mincc_win[i],minrr_win[i],maxcc_win[i],maxrr_win[i]])
        
    list_type=[]
    list_line=[]
    list_dir=[]## 0：占位符  1：上  2：下  3：左  4：右
    list_wid=[]
    for i in range(0,len(mincc_win)):
        if abs(mincc_win[i]-maxcc_win[i])>abs(minrr_win[i]-maxrr_win[i]):
            dir_win=1
        else:
            dir_win=0
        
        tmp=0#0:普通窗  1:阳台  2：飘窗  -1:删除
        line=(-1,-1,-1,-1)
        l_dir=0
        l_wid=-1
        
        
        #长宽太小删除窗户
        if max(abs(mincc_win[i]-maxcc_win[i]),abs(minrr_win[i]-maxrr_win[i]))<375*prop:
            tmp=-1
        ###############
        
#        t_img=init_img[minrr_win[i]-1:maxrr_win[i]+1,mincc_win[i]-1:maxcc_win[i]+1]
        
#        my_sum1=np.sum(t_img,axis=1)
#        my_list_img1 = my_sum1.tolist()
#        
#        my_sum2=np.sum(t_img,axis=0)
#        my_list_img2 = my_sum2.tolist()
        
        
        #窗户短边太长，删除
#        if my_list_img1[0]==0 and my_list_img1[len(my_list_img1)-1]==0 and my_list_img2[0]==0 and my_list_img2[len(my_list_img2)-1]==0:
#            a,b=t_img.shape
#            if min(a,b)>750*prop:
#                tmp=-1
        #################
        
        #检测阳台
        for j in range(0,len(mincc_slidingdoor)):
            if abs(mincc_slidingdoor[j]-maxcc_slidingdoor[j])>abs(minrr_slidingdoor[j]-maxrr_slidingdoor[j]):
                dir_sdoor=1
            else:
                dir_sdoor=0
            
#            print(abs((minrr_win[i]+maxrr_win[i])/2-(minrr_slidingdoor[j]+maxrr_slidingdoor[j])/2))
#            print(thres2)
            if dir_win==1 and dir_sdoor==1 and abs((mincc_win[i]+maxcc_win[i])/2-(mincc_slidingdoor[j]+maxcc_slidingdoor[j])/2)<abs(mincc_slidingdoor[j]-maxcc_slidingdoor[j])/4 and abs((minrr_win[i]+maxrr_win[i])/2-(minrr_slidingdoor[j]+maxrr_slidingdoor[j])/2)<thres2:
                tmp=1
                mincc_win[i]=min(mincc_win[i],mincc_slidingdoor[j])
                maxcc_win[i]=max(maxcc_win[i],maxcc_slidingdoor[j])
                minrr_win[i]=min(minrr_win[i],minrr_slidingdoor[j])
                maxrr_win[i]=max(maxrr_win[i],maxrr_slidingdoor[j])
                
#            print(abs((mincc_win[i]+maxcc_win[i])/2-(mincc_slidingdoor[j]+maxcc_slidingdoor[j])/2))
#            print(thres2)
            if dir_win==0 and dir_sdoor==0 and abs((minrr_win[i]+maxrr_win[i])/2-(minrr_slidingdoor[j]+maxrr_slidingdoor[j])/2)<abs(minrr_slidingdoor[j]-maxrr_slidingdoor[j])/4 and abs((mincc_win[i]+maxcc_win[i])/2-(mincc_slidingdoor[j]+maxcc_slidingdoor[j])/2)<thres2:
                tmp=1
                mincc_win[i]=min(mincc_win[i],mincc_slidingdoor[j])
                maxcc_win[i]=max(maxcc_win[i],maxcc_slidingdoor[j])
                minrr_win[i]=min(minrr_win[i],minrr_slidingdoor[j])
                maxrr_win[i]=max(maxrr_win[i],maxrr_slidingdoor[j])
        #################
        
        #检测飘窗
        if tmp==0 and tmp!=-1:
            if dir_win==1:
                tmp_img=init_img[:,mincc_win[i]-1:maxcc_win[i]+1]/255
                sum_t_img=np.sum(tmp_img,axis=1)
                list_sum_img = sum_t_img.tolist()
                if list_sum_img[minrr_win[i]-1]==0 and list_sum_img[maxrr_win[i]]==0:
                    if check_line(init_img, (minrr_win[i]-1, mincc_win[i]-1), (minrr_win[i]-1, maxcc_win[i]), -1,thres1)[0] or check_line(init_img, (maxrr_win[i], mincc_win[i]-1), (maxrr_win[i], maxcc_win[i]), 1,thres1)[0] :
                        num_line=max(check_line(init_img, (minrr_win[i]-1, mincc_win[i]-1), (minrr_win[i]-1, maxcc_win[i]), -1,thres1)[1],check_line(init_img, (maxrr_win[i], mincc_win[i]-1), (maxrr_win[i], maxcc_win[i]), 1,thres1)[1])
                        if num_line>=maxrr_win[i]:
                            l_dir=1
                            l_wid=abs(num_line-(minrr_win[i]-1))
                        if num_line<minrr_win[i]-1:
                            l_dir=2
                            l_wid=abs(num_line-maxrr_win[i])
                        tmp=2
                        line=(num_line,mincc_win[i]-1,num_line,maxcc_win[i])

                if list_sum_img[minrr_win[i]-1]==0 and list_sum_img[maxrr_win[i]]>0:
                    new_pointA, new_pointB = get_new_points(init_img,(maxrr_win[i],mincc_win[i]-1), (maxrr_win[i],maxcc_win[i]))
                    if check_line(init_img, new_pointA, new_pointB, 1,thres1)[0]:
                        num_line=check_line(init_img, new_pointA, new_pointB, 1,thres1)[1]
                        l_dir=1
                        l_wid=abs(num_line-(minrr_win[i]-1))
                        tmp=2
                        line=(num_line,mincc_win[i]-1,num_line,maxcc_win[i])
                    
                if list_sum_img[minrr_win[i]-1]>0 and list_sum_img[maxrr_win[i]]==0:
                    new_pointA, new_pointB = get_new_points(init_img,(minrr_win[i]-1,mincc_win[i]-1), (minrr_win[i]-1,maxcc_win[i]))
                    if check_line(init_img, new_pointA, new_pointB, -1,thres1)[0]:
                        num_line=check_line(init_img, new_pointA, new_pointB, -1,thres1)[1]
                        l_dir=2
                        l_wid=abs(num_line-maxrr_win[i])
                        tmp=2
                        line=(num_line,mincc_win[i]-1,num_line,maxcc_win[i])
                
            else:
                tmp_img=init_img[minrr_win[i]-1:maxrr_win[i]+1,:]/255
                sum_t_img=np.sum(tmp_img,axis=0)
                list_sum_img = sum_t_img.tolist()
                if list_sum_img[mincc_win[i]-1]==0 and list_sum_img[maxcc_win[i]]==0:
                    if check_line(init_img, (minrr_win[i]-1, mincc_win[i]-1), (maxrr_win[i], mincc_win[i]-1), -1,thres1)[0] or check_line(init_img, (minrr_win[i]-1, maxcc_win[i]+1), (maxrr_win[i]+1, maxcc_win[i]+1), 1,thres1)[0] :
                        num_line=max(check_line(init_img, (minrr_win[i]-1, mincc_win[i]-1), (maxrr_win[i], mincc_win[i]-1), -1,thres1)[1],check_line(init_img, (minrr_win[i]-1, maxcc_win[i]+1), (maxrr_win[i]+1, maxcc_win[i]+1), 1,thres1)[1])
                        if num_line>=maxcc_win[i]:
                            l_dir=3
                            l_wid=abs(num_line-(mincc_win[i]-1))
                        if num_line<mincc_win[i]-1:
                            l_dir=4
                            l_wid=abs(num_line-maxcc_win[i])
                        tmp=2
                        line=(minrr_win[i]-1,num_line,maxrr_win[i],num_line)
                        
                if list_sum_img[mincc_win[i]-1]==0 and list_sum_img[maxcc_win[i]]>0:
                    new_pointA, new_pointB = get_new_points(init_img,(minrr_win[i]-1,maxcc_win[i]), (maxrr_win[i],maxcc_win[i]))
                    if check_line(init_img, new_pointA, new_pointB, 1,thres1)[0]:
                        num_line=check_line(init_img, new_pointA, new_pointB, 1,thres1)[1]
                        l_dir=3
                        l_wid=abs(num_line-(mincc_win[i]-1))
                        tmp=2
                        line=(minrr_win[i]-1,num_line,maxrr_win[i],num_line)
                    
                if list_sum_img[mincc_win[i]-1]>0 and list_sum_img[maxcc_win[i]]==0:
                    new_pointA, new_pointB = get_new_points(init_img,(minrr_win[i]-1,mincc_win[i]-1), (maxrr_win[i],mincc_win[i]-1))
                    if check_line(init_img, new_pointA, new_pointB, -1,thres1)[0]:
                        num_line=check_line(init_img, new_pointA, new_pointB, -1,thres1)[1]
                        l_dir=4
                        l_wid=abs(num_line-maxcc_win[i])
                        tmp=2
                        line=(minrr_win[i]-1,num_line,maxrr_win[i],num_line)
        ##################
        
        if tmp==0 or tmp==1:
            if abs(mincc_win[i]-maxcc_win[i])>abs(minrr_win[i]-maxrr_win[i]):
                line=(int((minrr_win[i]+maxrr_win[i])/2),mincc_win[i]-1,int((minrr_win[i]+maxrr_win[i])/2),maxcc_win[i])
                l_dir=0
                l_wid=int(abs(minrr_win[i]-maxrr_win[i])/2)
            else:
                line=(minrr_win[i]-1,int((mincc_win[i]+maxcc_win[i])/2),maxrr_win[i],int((mincc_win[i]+maxcc_win[i])/2))
                l_dir=0
                l_wid=int(abs(mincc_win[i]-maxcc_win[i])/2)
        
        list_type.append(tmp)
        list_line.append(line)
        list_dir.append(l_dir)
        list_wid.append(l_wid)
        
    ###画图
    m = len(list_type)
    for i in range(m):
        if list_type[i]==0:
            (a_x,a_y,b_x,b_y)=list_line[i]
            cv2.line(new_img, (a_y,a_x), (b_y,b_x), (255,255,0), 6)
            if a_x==b_x:
                a_x-=list_wid[i]
                b_x+=list_wid[i]
            elif a_y==b_y:
                a_y-=list_wid[i]
                b_y+=list_wid[i]
            
            cv2.rectangle(new_img, (a_y,a_x), (b_y,b_x), (0,0,255), 3)
        if list_type[i]==1:
            (a_x,a_y,b_x,b_y)=list_line[i]
            cv2.line(new_img, (a_y,a_x), (b_y,b_x), (255,255,0), 6)
            if a_x==b_x:
                a_x-=list_wid[i]
                b_x+=list_wid[i]
            elif a_y==b_y:
                a_y-=list_wid[i]
                b_y+=list_wid[i]
            
            cv2.rectangle(new_img, (a_y,a_x), (b_y,b_x), (0,255,0), 3)
        if list_type[i]==2:
            (a_x,a_y,b_x,b_y)=list_line[i]
            cv2.line(new_img, (a_y,a_x), (b_y,b_x), (255,255,0), 6)
            if list_dir[i]==1:
                a_x-=list_wid[i]
            if list_dir[i]==2:
                b_x+=list_wid[i]
            if list_dir[i]==3:
                a_y-=list_wid[i]
            if list_dir[i]==4:
                b_y+=list_wid[i]
            
            cv2.rectangle(new_img, (a_y,a_x), (b_y,b_x), (255,0,0), 3)
            
    if is_drawing==1:
        cv2.imwrite('window_type.jpg', new_img)
    #########
    
    ###存储结构体
    win_normal=Data_struct.Window()
    win_normal.set_type(0)
    win_bay=Data_struct.Window()
    win_bay.set_type(1)
    win_balcony=Data_struct.Window()
    win_balcony.set_type(2)
    
    xflip_normal=[]
    xflip_bay=[]
    xflip_balcony=[]
    
    yflip_normal=[]
    yflip_bay=[]
    yflip_balcony=[]
    
    id_normal=[]
    id_bay=[]
    id_balcony=[]
    
    base_position_normal=[]
    base_position_bay=[]
    base_position_balcony=[]
    #Get_owner_wall.Get_owner_wall([mincc[i],minrr[i],x3,minrr[i],0,maxrr[i]-minrr[i]],bear_wall,nonbearwall)
    m = len(list_type)
    for i in range(m):
        if list_type[i]==0:
            if abs(mincc_win[i]-maxcc_win[i])>abs(minrr_win[i]-maxrr_win[i]):
                xflip_normal.append(1)
                yflip_normal.append(0)
            else:
                xflip_normal.append(0)
                yflip_normal.append(1)
            base_position_normal.append((list_line[i][1],list_line[i][0],list_line[i][3],list_line[i][2],list_wid[i],list_wid[i]))
            id_normal.append(Get_owner_wall.Get_owner_wall([list_line[i][1],list_line[i][0],list_line[i][3],list_line[i][2],list_wid[i],list_wid[i]],bear_wall,nonbearwall))
            #base_position_normal.append((list_line[i][0],list_line[i][1],list_line[i][2],list_line[i][3],list_wid[i],list_wid[i]))
        if list_type[i]==1:
            if abs(mincc_win[i]-maxcc_win[i])>abs(minrr_win[i]-maxrr_win[i]):
                xflip_balcony.append(1)
                yflip_balcony.append(0)
            else:
                xflip_balcony.append(0)
                yflip_balcony.append(1)
            base_position_balcony.append((list_line[i][1],list_line[i][0],list_line[i][3],list_line[i][2],list_wid[i],list_wid[i]))
            id_balcony.append(Get_owner_wall.Get_owner_wall([list_line[i][1],list_line[i][0],list_line[i][3],list_line[i][2],list_wid[i],list_wid[i]],bear_wall,nonbearwall))
        if list_type[i]==2:
            if list_dir[i]==1:
                xflip_bay.append(1)
                yflip_bay.append(0)
                base_position_bay.append((list_line[i][1],list_line[i][0],list_line[i][3],list_line[i][2],list_wid[i],0))
                id_bay.append(Get_owner_wall.Get_owner_wall([list_line[i][1],list_line[i][0],list_line[i][3],list_line[i][2],list_wid[i],0],bear_wall,nonbearwall))
            elif list_dir[i]==2:
                xflip_bay.append(1)
                yflip_bay.append(0)
                base_position_bay.append((list_line[i][1],list_line[i][0],list_line[i][3],list_line[i][2],0,list_wid[i]))
                id_bay.append(Get_owner_wall.Get_owner_wall([list_line[i][1],list_line[i][0],list_line[i][3],list_line[i][2],0,list_wid[i]],bear_wall,nonbearwall))
            elif list_dir[i]==3:
                xflip_bay.append(0)
                yflip_bay.append(1)
                base_position_bay.append((list_line[i][1],list_line[i][0],list_line[i][3],list_line[i][2],list_wid[i],0))
                id_bay.append(Get_owner_wall.Get_owner_wall([list_line[i][1],list_line[i][0],list_line[i][3],list_line[i][2],list_wid[i],0],bear_wall,nonbearwall))
            elif list_dir[i]==4:
                xflip_bay.append(0)
                yflip_bay.append(1)
                base_position_bay.append((list_line[i][1],list_line[i][0],list_line[i][3],list_line[i][2],0,list_wid[i]))
                id_bay.append(Get_owner_wall.Get_owner_wall([list_line[i][1],list_line[i][0],list_line[i][3],list_line[i][2],0,list_wid[i]],bear_wall,nonbearwall))
            else:
                print('error: the dir of bay window cannot be zero')
            
    win_normal.add_base_position(base_position_normal)
    win_normal.add_Xflip(xflip_normal)
    win_normal.add_Yflip(yflip_normal)
    win_normal.add_windows_id(id_normal)
    
    win_bay.add_base_position(base_position_bay)
    win_bay.add_Xflip(xflip_bay)
    win_bay.add_Yflip(yflip_bay)
    win_bay.add_windows_id(id_bay)
    
    win_balcony.add_base_position(base_position_balcony)
    win_balcony.add_Xflip(xflip_balcony)
    win_balcony.add_Yflip(yflip_balcony)
    win_balcony.add_windows_id(id_balcony)
#    wins=[]
#    m = len(list_type)
#    for i in range(m):
#        if list_type[i]!=-1:
#            win=Data_struct.Window()
#            f_t=0
#            if abs(mincc_win[i]-maxcc_win[i])>abs(minrr_win[i]-maxrr_win[i]):
#                f_t=0
#            else:
#                f_t=1
#            win.set_orientation(f_t)
#            win.set_wid(list_wid[i])
#            win.set_line(list_line[i])
#            win.set_dir(list_dir[i])
#            win.set_position(mincc_win[i],minrr_win[i],maxcc_win[i],minrr_win[i],maxcc_win[i],maxrr_win[i],mincc_win[i],maxrr_win[i])
#            if list_type[i]==1:
#                win.set_type(2)
#            if list_type[i]==2:
#                win.set_type(1)
#            if list_type[i]==0:
#                win.set_type(0)
#            wins.append(win)
    return win_normal,win_bay,win_balcony,new_img