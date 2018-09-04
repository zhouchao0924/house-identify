# -*- coding: utf-8 -*-
import cv2
import numpy as np

def getLine(gray_src):
    #src = cv2.imread(filename)  
    #gray_src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) 
    #ret,gray_src = cv2.threshold(gray_src,thre,255,cv2.THRESH_BINARY)
   # gray_src = gray2binary(gray_src,60)     
    gray_src = cv2.bitwise_not(gray_src)  
    binary_src = cv2.adaptiveThreshold(gray_src, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
    #提取水平线
    hline = cv2.getStructuringElement(cv2.MORPH_RECT, ((int(gray_src.shape[1]/8)), 1), (-1, -1))  
    
    # 提取垂直线  
    vline = cv2.getStructuringElement(cv2.MORPH_RECT, (1, (int(gray_src.shape[0]/8))), (-1, -1))  
   
    temp = cv2.erode(binary_src, vline)  
    dst1 = cv2.dilate(temp, vline)  
    dst1 = cv2.morphologyEx(binary_src, cv2.MORPH_OPEN, vline)  
    dst1 = cv2.bitwise_not(dst1) 
    
    temp2 = cv2.erode(binary_src, hline)  
    dst2 = cv2.dilate(temp2, hline)
    dst2 = cv2.morphologyEx(binary_src, cv2.MORPH_OPEN, hline)  
    dst2 = cv2.bitwise_not(dst2)
    
    #dst1 = cv2.morphologyEx(binary_src, cv2.MORPH_OPEN, vline)  
    #dst1 = cv2.bitwise_not(dst1)  
    #dst2 = cv2.morphologyEx(binary_src, cv2.MORPH_OPEN, hline)  
    #dst2 = cv2.bitwise_not(dst2)  
    
    return dst1,dst2
    

#返回从上向下，从左到右找到的第一个点的纵坐标
def find_top_left_x(img,a,b,m,n):
    flag=0
    for i in range(a,b):
        for j in range(m,n):
            if img[i,j]==0:
                flag=1
                return j        
        if flag==1:
            break
#返回从下向上，从左到右找到的第一个点的纵坐标
def find_bottom_left_x(img,a,b,m,n):
    flag=0
    for i in range(a,b,-1):
        for j in range(m,n):
            if img[i,j]==0:
                flag=1
                return j 
        if flag==1:
            break
#返回从上向下，从右到左找到的第一个点的纵坐标        
def find_top_right_x(img,a,b,m,n):
    flag=0
    for i in range(a,b):
        for j in range(m,n,-1):
            if img[i,j]==0:
                flag=1
                return j
        if flag==1:
            break
#返回从下向上，从右到左找到的第一个点的纵坐标        
def find_bottom_right_x(img,a,b,m,n):
    flag=0
    for i in range(a,b,-1):
        for j in range(m,n,-1):
            if img[i,j]==0:
                flag=1
                return j
        if flag==1:
            break
#返回上下比例尺的左界限，左右比例尺的右界限       
def find_x_left(img):
    x_left_1=find_top_left_x(img,0,len(img),0,len(img[0]))
    x_left_2=find_bottom_left_x(img,len(img)-1,0,0,len(img[0]))
    return max(min(x_left_1,x_left_2)-15,0)

#返回上下比例尺的右界限，左右比例尺的下界限  
def find_x_right(img):
    x_right_1=find_top_right_x(img,0,len(img),len(img[0])-1,0)
    x_right_2=find_bottom_right_x(img,len(img)-1,0,len(img[0])-1,0)
    return min(max(x_right_1,x_right_2)+15,int(len(img[0])))


        
#得到上比例尺的所有直线起点坐标
def get_top_ruler_line_start(img,x_max,y_max):
    x=[]
    y=[]
    count=0
    for i in range(1,y_max):
        if(count>=1):
            break
        for j in range(1,x_max):
            if (img[i,j]==0):
                y.append(i)
                x.append(j)
                count=count+1
            else:
                continue
            break      
    return x,y

#得到下比例尺的所有直线起点坐标
def get_down_ruler_line_start(img,x_max,y_max):
    x=[]
    y=[]
    count=0
    for i in range(y_max-1,0,-1):
        if(count>=1):
            break        
        for j in range(0,x_max):
            if (img[i,j]==0):
                y.append(i)     
                x.append(j)    
                count=count+1
            else:
                continue
            break      
    return x,y    

def Is_start2(img,i,j):
    sum=0
    for i in range(0,len(img)):
        if(img[i,j]==0):
            sum=sum+1
    if sum>=50:
        return 1
    return 0
        
    
#得到左比例尺的所有直线起点坐标
def get_left_ruler_line_start(img,x_max,y_max):
    x=[]
    y=[]
    count=0    
    for j in range(1,x_max):
        if(count>=1):
            break        
        for i in range(1,y_max):
            if img[i,j]==0:
                y.append(i)     
                x.append(j)
                count=count+1
            else:
                continue
            break      
    return x,y 

#得到右标尺的所有直线起点坐标
def get_right_ruler_line_start(img,x_max,y_max):
    x=[]
    y=[]
    count=0    
    for j in range(x_max-1,1,-1):
        if(count>=1):
            break                
        for i in range(1,y_max):
            if img[i,j]==0:
                y.append(i)     
                x.append(j)
                count=count+1                
            else:
                continue
            break      
    return x,y 


        
#得到上下比例尺的水平直线的y坐标，即下一步需要扫描沿该方向扫描端点
def get_top_down_y(img):
    #image=cv2.imread(filename,0) 
    #ret,image = cv2.threshold(image,thre,255,cv2.THRESH_BINARY)     
    image1,image2=getLine(img)
    #ret,image1 = cv2.threshold(image1,thre,255,cv2.THRESH_BINARY)  
    #ret,image2 = cv2.threshold(image2,thre,255,cv2.THRESH_BINARY)  
    #x_left=find_x_left(image2)
    #x_right=find_x_right(image2)
    #image3=np.rot90(image1)
    #ret,image3 = cv2.threshold(image3,thre,255,cv2.THRESH_BINARY)  
    #image3=gray2binary(image3,60)
    #y_top=find_x_left(image3)
    #y_bottom=find_x_right(image3)
    y_max=int(len(img))
    x_max=int(len(img[0]))
    x1,y1=get_top_ruler_line_start(image2,x_max,y_max)
    x2,y2=get_down_ruler_line_start(image2,x_max,y_max) 
  #  x1,y1=delete_repeat(x1,y1)
  #  x2,y2=delete_repeat(x2,y2) 
    #return x_top,y_top,x_down,y_down
    return y1,y2


#得到左右比例尺中直线的的x坐标，即下一步需要扫描沿该方向扫描端点
def get_left_right_x(img):
    #image=cv2.imread(filename,0) 
    #ret,image = cv2.threshold(image,thre,255,cv2.THRESH_BINARY)     
    image1,image2=getLine(img)
    #ret,image1 = cv2.threshold(image1,thre,255,cv2.THRESH_BINARY)  
    #ret,image2 = cv2.threshold(image2,thre,255,cv2.THRESH_BINARY)  
    #x_left=find_x_left(image2)
    #x_right=find_x_right(image2)
    #image3=np.rot90(image1)
   # ret,image3 = cv2.threshold(image3,thre,255,cv2.THRESH_BINARY)  
    #image3=gray2binary(image3,60)
    #y_top=find_x_left(image3)
    #y_bottom=find_x_right(image3)
    y_max=int(len(img))
    x_max=int(len(img[0]))
    
    x1,y1=get_left_ruler_line_start(image1,x_max,y_max)
    x2,y2=get_right_ruler_line_start(image1,x_max,y_max) 
   # x1,y1=delete_repeat(x1,y1)
   # x2,y2=delete_repeat(x2,y2) 
    return x1,x2


def get_top_y_correct(y,limit):
    for i in range(0,len(y)) :
        if(y[i]>(limit+30)):
            return y[0:i]
    return y
        
        
def get_down_y_correct(y,limit):
    for i in range(0,len(y)) :
        if(y[i]>(limit-30)):
            return y[i:len(y)]
    return y

def get_left_x_correct(x,limit):
    for i in range(0,len(x)) :
        if(x[i]>(limit+30)):
            return x[0:i]  
    return x

def get_right_x_correct(x,limit):
    for i in range(0,len(x)) :
        if(x[i]<(limit-30)):
            return x[0:i]
    return x

def sumPoint1_(img,m,n):
    sumpoint=0
    for i in range(m-1,m-10,-1):
        if img[i,n]==0:
            sumpoint=sumpoint+1
        else:
            break
    for i in range(m+1,m+11):
        if img[i,n]==0:
            sumpoint=sumpoint+1   
        else:
            break
    return sumpoint
#求点上下20个点里0的个数    
def sumPoint(img,m,n):
    sumpoint=0
    for i in range(m-10,m+11):
        if img[i,n]==0:
            sumpoint=sumpoint+1
    return sumpoint

def sumPoint2_(img,m,n):
    sumpoint=0
    for i in range(n-1,n-10,-1):
        if img[m,i]==0:
            sumpoint=sumpoint+1
        else:
            break
    for i in range(n+1,n+10):
        if img[m,i]==0:
            sumpoint=sumpoint+1
        else:
            break   
    return sumpoint
#求点左右20个点里0的个数    
def sumPoint2(img,m,n):
    sumpoint=0
    for i in range(n-10,n+11):
        if img[m,i]==0:
            sumpoint=sumpoint+1
    return sumpoint

#判断是否是水平直线上的端点
def IsPoint(img,m,n):  
    if ((img[m+3,n]==0)):# or (img[m-1,n]==0) ):
        return 1
    else:
        return 0
 #   if (((sumPoint(img,m,n)-sumPoint(img,m,n-1))>=1)and((sumPoint(img,m,n)-sumPoint(img,m,n+1))>=1) and((img[m-1,n]==0) or (img[m+1,n]==0) )):
        
def IsPoint_double(img,m,n):   
    if ((img[m-1,n]==0) or (img[m+2,n]==0) ):
        return 1
    else:
        return 0  
def IsPoint_double2(img,m,n):   
    if ((img[m-2,n]==0) or (img[m+1,n]==0) ):
        return 1
    else:
        return 0  
def IsPoint_double1(img,m,n):   
    if ((sumPoint(img,m,n))>=10):
        return 1
    else:
        return 0 
       
#判断是否是竖直直线上的端点    
def IsPoint2_left(img,m,n):
    if ((img[m,n-2]==0) ):
        return 1
    else:
        return 0
def IsPoint2_right(img,m,n):
    if ((img[m,n+2]==0) ):
        return 1
    else:
        return 0
#if (((sumPoint2(img,m,n)-sumPoint2(img,m-1,n))>=1)and((sumPoint2(img,m,n)-sumPoint2(img,m+1,n))>=1) and((img[m,n-1]==0) or (img[m,n+1]==0) )):
def IsPoint2_double(img,m,n):
    if ((img[m,n-1]==0) or (img[m,n+2]==0) ):
        return 1
    else:
        return 0
def IsPoint2_double2(img,m,n):
    if ((img[m,n-2]==0) or (img[m,n+1]==0) ):
        return 1
    else:
        return 0  

#对数组进行去重排序      
def sort_1(l):  
    if len(l) <= 1:  
        return l  
    mid = l[0]  
    low = [item for item in l if item < mid]  
    high = [item for item in l if item > mid]  
    return sort_1(low) + [mid] + sort_1(high)  

#对数组进行去重排序      
def sort_(l,l_y):  
    news_ids = []
    news_ids_y=[]
    for i in range(len(l)):
        if l[i] not in news_ids:
            news_ids.append(l[i]) 
            news_ids_y.append(l_y[i])
            
    
    #for id in l:  
        #if id not in news_ids:  
            #news_ids.append(id)  
    news_ids.sort()
    return news_ids,news_ids_y


def delete_repeat(a,a_y,thre):
    i=1 
    b=[]
    b_y=[]
    index=[0 for i in range(len(a))]
    while(i<len(a)):
        c=0
        count=0
        while(i<len(a) and a[i]-a[i-1]<=5 and a_y[i]==a_y[i-1]):
            c=c+a[i-1]
            index[i]=1
            index[i-1]=1
            i=i+1
            count=count+1  
        else:
            if(count!=0):
                c=c+a[i-1]
                count=count+1
                b.append(int(c/count))
                b_y.append(a_y[i-1])
            else:
                    i=i+1            
    for i in range(len(a)):
        if index[i]==0:
            b.append(a[i])
            b_y.append(a_y[i])
    return b,b_y

def get_y_len(img,y):
    #img2=img.tolist()
    #yy=img2[y]
    #len_y=yy.count(0)
    y_start=y_end=0
    for i in range(len(img[0])):
        if(img[y,i]==0):
            y_start=i
            break
    for i in range(len(img[0])-1,0,-1):
        if(img[y,i]==0):
            y_end=i
            break
   
    len_y=abs(y_end-y_start)
    return len_y

def get_x_len(img,x):
    #img2=img.tolist()
    #xx=[a[x] for a in img2]
    #len_x=xx.count(0)
    x_start=x_end=0
    for i in range(len(img)):
        if(img[i,x]==0):
            x_start=i
            break
    for i in range(len(img)-1,0,-1):
        if(img[i,x]==0):
            x_end=i
            break
    len_x=abs(x_end-x_start)
    return len_x

def get_top_Point(img,y,thre):
    pointlist=[]
    pointlist_y=[]
    maxlen=get_y_len(img,y[0])
    
    i=0
    while(i<len(y)):
        if (get_y_len(img,y[i])<thre*maxlen):
            break
        elif (i<len(y)-1 and abs(y[i]-y[i+1])==1):
            for j in range(80,len(img[0])-1):
                if IsPoint_double(img,y[i],j):
                    pointlist.append(j)  
                    pointlist_y.append(y[i])                    
            i=i+2            
        else:
            for j in range(80,len(img[0])-1):
                if IsPoint(img,y[i],j):
                    pointlist.append(j)
                    pointlist_y.append(y[i])                   
            i=i+1
                     
    #pointlist,pointlist_y=sort_(pointlist,pointlist_y)
    pointlist,pointlist_y=delete_repeat(pointlist,pointlist_y,5)
    pointlist.sort()
    return pointlist,pointlist_y

def get_down_Point(img,y,thre):
    pointlist=[]
    pointlist_y=[]
    maxlen=get_y_len(img,y[0])
    #如果线条两倍粗
    i=0
    while(i<len(y)):
        if (get_y_len(img,y[i])<thre*maxlen):
            break
        if (i<len(y)-1 and abs(y[i]-y[i+1])==1):
            for j in range(0,len(img[0])-1):
                if IsPoint_double2(img,y[i],j):
                    pointlist.append(j)  
                    pointlist_y.append(y[i])                    
            i=i+2            
        else:
            for j in range(0,len(img[0])-1):
                if IsPoint(img,y[i],j):
                    pointlist.append(j)
                    pointlist_y.append(y[i])                   
            i=i+1
                     
    #pointlist=sort_(pointlist)
    pointlist,pointlist_y=delete_repeat(pointlist,pointlist_y,5)
    #pointlist.sort()
    return pointlist,pointlist_y
         
        
def get_top_startpoint_y(img,y,thre):
    maxlen=get_y_len(img,y[0])
    top_startpoint_y=0
    for i in range(len(y)-1,0,-1):
        if (get_y_len(img,y[i])>=thre*maxlen):
            top_startpoint_y=y[i]
            break
    return top_startpoint_y
            
def get_down_startpoint_y(img,y,thre):
    top_startpoint_y=0
    maxlen=get_y_len(img,y[len(y)-1])
    for i in range(len(y)):
        if (get_y_len(img,y[i])>=thre*maxlen):
            top_startpoint_y=y[i]
            break
    return top_startpoint_y      
    

def get_left_Point(img,x,thre):
    pointlist=[]
    pointlist_x=[]
    maxlen=get_x_len(img,x[0])
    j=0
    while(j<len(x)):
        if (get_x_len(img,x[j])<thre*maxlen):
            break
        elif (j<len(x)-1 and abs(x[j]-x[j+1])==1):#如果线条两倍粗
            for i in range(0,len(img)-1):
                if IsPoint2_double(img,i,x[j]):
                    pointlist.append(i)
                    pointlist_x.append(x[j])
            j=j+2
        else:
            for i in range(0,len(img)-1):
                if IsPoint2_left(img,i,x[j]):
                    pointlist.append(i)
                    pointlist_x.append(x[j])
            j=j+1
    #pointlist=sort_(pointlist)
    pointlist,pointlist_x=delete_repeat(pointlist,pointlist_x,5)
    #pointlist.sort()
    return pointlist,pointlist_x
def get_right_Point(img,x,thre):
    pointlist=[]
    pointlist_x=[]
    maxlen=get_x_len(img,x[0])
    j=0
    while(j<len(x)):
        if (get_x_len(img,x[j])<thre*maxlen):
            break
#            j=j+1
        elif (j<len(x)-1 and abs(x[j]-x[j+1])==1):#如果线条两倍粗
            for i in range(0,len(img)-1):
                if IsPoint2_double2(img,i,x[j]):
                  #  cv2.rectangle(img,(x[j]-10,i-10),(x[j]+10,i+10),(50,40,10),3)
                    pointlist.append(i)
                    pointlist_x.append(x[j])
               # if IsPoint2(img,i,x[j]):
                 #   cv2.rectangle(img,(x[j]-10,i-10),(x[j]+10,i+10),(50,40,10),3)
                #    pointlist.append(i)
            j=j+2
        else:
            for i in range(0,len(img)-1):
                if IsPoint2_right(img,i,x[j]):
                   # cv2.rectangle(img,(x[j]-10,i-10),(x[j]+10,i+10),(50,40,10),3)
                    pointlist.append(i)
                    pointlist_x.append(x[j])
            j=j+1
    #pointlist=sort_(pointlist)
    pointlist,pointlist_x=delete_repeat(pointlist,pointlist_x,5)
    #pointlist.sort()
    return pointlist,pointlist_x

def get_left_startpoint_x(img,x,thre): 
    maxlen=get_x_len(img,x[0])
    left_startpoint_x=0
    for i in range(len(x)-1,0,-1):
        if (get_x_len(img,x[i])>=thre*maxlen):
            left_startpoint_x =x[i]
            break
    return left_startpoint_x 

def get_right_startpoint_x(img,x,thre):
    right_startpoint_x=0
    maxlen=get_x_len(img,x[0])
    for i in range(len(x)-1,0,-1):
        if (get_x_len(img,x[i])>=thre*maxlen):
            right_startpoint_x =x[i]
            break
    return right_startpoint_x 
