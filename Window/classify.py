from Window import window
from Datastruct import Data_struct

def list_sum(list_a, beg, end):
    res=0
    while beg<=end:
        res+=list_a[beg]
        beg+=1
    return res

def classify(init_img,Ruler,single_door,sliding_door,thres2):
    img_two_rect_win, img_two_piao_win, mincc_win, minrr_win, maxcc_win, maxrr_win, mincc_two_piao, minrr_two_piao, maxcc_two_piao, maxrr_two_piao = window.Windows_detect(init_img.copy(), Ruler.out_scale(), single_door)
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
        
    for i in range(len(list_slidingdoor)):
        tmp=list_slidingdoor[i]
        minrr_slidingdoor.append(tmp[1])#y坐标
        mincc_slidingdoor.append(tmp[0])#x坐标
        maxrr_slidingdoor.append(tmp[3])#y坐标
        maxcc_slidingdoor.append(tmp[2])#x坐标
        
    list_type=[]
    list_line=[]
    list_dir=[]
    list_wid=[]
    for i in range(len(mincc_win)):
        flag=0
        if abs(mincc_win[i]-maxcc_win[i])>abs(minrr_win[i]-maxrr_win[i]):
            dir_win=1
        else:
            dir_win=0
        for j in range(0,len(mincc_slidingdoor)):
            if abs(mincc_slidingdoor[j]-maxcc_slidingdoor[j])>abs(minrr_slidingdoor[j]-maxrr_slidingdoor[j]):
                dir_sdoor=1
            else:
                dir_sdoor=0
            if dir_win==1 and dir_sdoor==1 and abs((mincc_win[i]+maxcc_win[i])/2-(mincc_slidingdoor[j]+maxcc_slidingdoor[j])/2)<abs(mincc_slidingdoor[j]-maxcc_slidingdoor[j])/4 and abs((minrr_win[i]+maxrr_win[i])/2-(minrr_slidingdoor[j]+maxrr_slidingdoor[j])/2)<thres2:
                mincc_win[i]=min(mincc_win[i],mincc_slidingdoor[j])
                maxcc_win[i]=max(maxcc_win[i],maxcc_slidingdoor[j])
                minrr_win[i]=min(minrr_win[i],minrr_slidingdoor[j])
                maxrr_win[i]=max(maxrr_win[i],maxrr_slidingdoor[j])
                flag=1
                
            if dir_win==0 and dir_sdoor==0 and abs((minrr_win[i]+maxrr_win[i])/2-(minrr_slidingdoor[j]+maxrr_slidingdoor[j])/2)<abs(minrr_slidingdoor[j]-maxrr_slidingdoor[j])/4 and abs((mincc_win[i]+maxcc_win[i])/2-(mincc_slidingdoor[j]+maxcc_slidingdoor[j])/2)<thres2:
                mincc_win[i]=min(mincc_win[i],mincc_slidingdoor[j])
                maxcc_win[i]=max(maxcc_win[i],maxcc_slidingdoor[j])
                minrr_win[i]=min(minrr_win[i],minrr_slidingdoor[j])
                maxrr_win[i]=max(maxrr_win[i],maxrr_slidingdoor[j])
                flag=1
        
        if abs(mincc_win[i]-maxcc_win[i])>abs(minrr_win[i]-maxrr_win[i]):
            line=(int((minrr_win[i]+maxrr_win[i])/2),mincc_win[i]-1,int((minrr_win[i]+maxrr_win[i])/2),maxcc_win[i])
            l_dir=0
            l_wid=int(abs(minrr_win[i]-maxrr_win[i])/2)
        else:
            line=(minrr_win[i]-1,int((mincc_win[i]+maxcc_win[i])/2),maxrr_win[i],int((mincc_win[i]+maxcc_win[i])/2))
            l_dir=0
            l_wid=int(abs(mincc_win[i]-maxcc_win[i])/2)
            
        list_type.append(flag)
        list_line.append(line)
        list_dir.append(l_dir)
        list_wid.append(l_wid)
    
    for i in range(len(minrr_two_piao)):
        if abs(mincc_win[i]-maxcc_win[i])>abs(minrr_win[i]-maxrr_win[i]):
            dir_win=1
        else:
            dir_win=0
        
        tmp_img=init_img[minrr_win[i]:maxrr_win[i]+1,mincc_win[i]:maxcc_win[i]+1]/255
        if dir_win==1:
            sum_t_img=np.sum(tmp_img,axis=1)
            list_sum_img = sum_t_img.tolist()
            if list_sum(list_sum_img,0,int((len(list_sum_img)-1)/2)) < list_sum(list_sum_img,int(len(list_sum_img)/2),len(list_sum_img)-1):
                l_dir=1
                l_wid=abs(num_line-(minrr_win[i]-1))
            else:
                l_dir=2
                l_wid=abs(num_line-maxrr_win[i])
        else:
            
    
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
    
    for i in range():
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
    return win_normal,win_bay,win_balcony,new_img