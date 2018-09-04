# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 11:24:20 2018

@author: LuYixing
2018.7.4 demo_v36
    此文件实现毛坯房中将Layout数据转化为json格式
    已实现的有：
        CORNER：id由uuid1()随机生成
        WALL（普通墙 usage1，承重墙 usage2）：id使用uuid3()根据原始wall id生成
        DOOR（普通门 type2）：id由uuid1()随机生成，所属墙id由uuid3()根据原始wall id生成
        WINDOW（普通窗 type10，飘窗 type11，未将阳台纳入）：id由uuid1()随机生成，所属墙id由uuid3()根据原始wall id生成


2018.7.4 decoration_demo_v11
    在毛坯房基础上添加 门（双开门、推拉门，xflip、flip）
    考虑ruler识别出的比例pro，在wall、door、window得到position的列表后对其进行transPositionByPro转化为实际坐标

2018.7.4 demo_v37
    考虑ruler识别出的比例pro，在wall、door、window得到position的列表后对其进行transPositionByPro转化为实际坐标

2018.8.29
    在识别毛坯房中添加双开门和推拉门，并将推拉门的flip统一设置为0
    发现问题：有的图片中双开门的id比flip和postition的数量少 导致后面填入信息时出错

"""
#from Datastruct import Data_struct
import json
import math
import uuid
namespace = uuid.NAMESPACE_URL

#主函数
def toJson(Layout,filename):
    pro=Layout.out_ruler()[0].out_proportion()
    #待完成的dict              
    rooms_dict = []
    wallOpenings_dict = []
    electricities_dict = []
    pillars_dict = []
    fluePipes_dict = []
    rulers_dict = []
    textLabels_dict = []

    IsCombine=False#是否将被门洞分开的墙合并，此处默认为false

    #墙的list及原始id 和 承重墙和非承重墙数目
    list_wall,list_wall_id,NumBearWall,NumNonBearWall=getWallList(Layout,IsCombine,pro)
    
    #由wall得到的corner及 guid生成的随机id
    corner_list,corner_list_id=getCornerList(list_wall)

    #填入Corner
    corners_dict=fillCornerDict(corner_list,corner_list_id)

    #填入Wall
    walls_dict=fillWallDict(list_wall,list_wall_id,corner_list,corner_list_id,NumBearWall,NumNonBearWall)
    
    #填入Door
    wallOpenings_dict=fillDoorDict(Layout,wallOpenings_dict,pro)

    #填入Window
    wallOpenings_dict=fillWindowsDict(Layout,wallOpenings_dict,pro)
    
    #得到所有需要输出的DICT
    Dict=getDict(corners_dict,rooms_dict,walls_dict,wallOpenings_dict,electricities_dict,pillars_dict,fluePipes_dict,rulers_dict,textLabels_dict)

    #将Dict转化为Json，并写入文件
    tran_write(Dict,filename)

#将Dict转化为Json，并写入文件
def tran_write(Dict,filename):
    json_str = json.dumps(Dict,indent=4, ensure_ascii=False)
    #print (json_str)
    with open(filename,'w') as f:
        f.write(json_str)

#得到包含所有交点的corner_list,及相应的id
def getCornerList(list_wall):
    corner_list = []
    corner_list_id = []
    for index in range(len(list_wall)):
        wall=list_wall[index]
        x1 = wall[0]        
        y1 = wall[1]
        if (x1,y1) not in corner_list:
            corner_list.append((x1,y1))
            corner_list_id.append(uuid.uuid1())
        x2 = wall[2]
        y2 = wall[3]
        if (x2,y2) not in corner_list:
            corner_list.append((x2,y2))
            corner_list_id.append(uuid.uuid1())
    #print('length of corner = ',len(corner_list))
    return corner_list,corner_list_id

#获取墙的list，及原始id，和承重墙非承重墙数目
def getWallList(Layout,IsCombine,pro):
    walls = Layout.out_walls()
    #得到墙（数据结构：Wall）
    bearwall=walls[0]#得到承重墙
    non_bearwall=walls[1]#得到非承重墙
    #得到墙list
    bearwall_list=bearwall.out_wall_division()
    non_bearwall_list=non_bearwall.out_wall_division()
    wall_list=bearwall_list+non_bearwall_list
    #得到实际坐标
    wall_list=transPositionByPro(pro,wall_list)
    #得到数目
    NumBearWall=len(bearwall_list)
    NumNonBearWall=len(non_bearwall_list)
    #得到墙id list
    bearwall_id_list=bearwall.out_wall_id()
    non_bearwall_id_list=non_bearwall.out_wall_id()
    wall_id_list=bearwall_id_list+non_bearwall_id_list
    
    #将被门洞分开的墙合并
    if IsCombine == True:
        wall_list=CombineWall(wall_list,wall_id_list)

    return wall_list,wall_id_list,NumBearWall,NumNonBearWall

#填入Corner
def fillCornerDict(corner_list,corner_list_id):
    corners_dict=[]  
    for index in range(len(corner_list)):
        x = float(corner_list[index][0])
        y = float(corner_list[index][1])
        corner = {
                     'ID': str(corner_list_id[index]),
                     'X': x,
                     'Y': y
                 }
        corners_dict.append(corner)
    return corners_dict

#填入Wall
#此处list_wall_id为原始id
#根据cornerlist及找到corner的index，进而从corner_list_id中获得之前生成的guid
#根据NumBearWall和NumNonBearWall 判断承重墙还是非承重墙
def fillWallDict(list_wall,list_wall_id,corner_list,corner_list_id,NumBearWall,NumNonBearWall):
    walls_dict=[]
    for index in range(len(list_wall)):
        wall = list_wall[index]
        wall_id=list_wall_id[index]
        x1 = wall[0]        
        y1 = wall[1]
        x2 = wall[2]
        y2 = wall[3]
        #找到对应corner的id
        Index_Start=corner_list.index((x1,y1))
        Index_End=corner_list.index((x2,y2))
        ID_Index_Start=corner_list_id[Index_Start]
        ID_Index_End=corner_list_id[Index_End]

        left_dist=float(wall[4])
        right_dist=float(wall[5])

        #根据主轴决定是否调换左右宽度
        #tranRightLeftThick(x1,y1,x2,y2,left_dist,right_dist);
        if(x1==x2):
            left_dist,right_dist=right_dist,left_dist

        if index < NumBearWall:
            walltype=2
        else:
            walltype=1
        wall = {
            'ID': str(uuid.uuid3(namespace,str(wall_id))),
            'StartCorner': str(ID_Index_Start),
            'EndCorner': str(ID_Index_End),
            'LeftThick': left_dist,
            'RightThick': right_dist,
            'Height': 'NOT_DEFINE',
            'ArcWall': {
                'IsArc': 'NOT_DEFINE',
                'PositionOnArc': {
                    'X': 'NOT_DEFINE',
                    'Y': 'NOT_DEFINE'
                    }
                },
            'Usage': walltype,
        }
        walls_dict.append(wall)
    return walls_dict

#此处为原来要求：毛坯房只识别普通门，不考虑flip
'''   
#填入Door
#此处只有普通门（type 2）
def fillDoorDict(Layout,wallOpenings_dict,pro):
    doors = Layout.out_doors()
    #得到普通门
    Doors=doors[0]
    #得到信息
    Doors_type=Doors.out_type()
    Doors_id=Doors.out_door_id()
    #Xflip_list=Doors.out_Xflip()
    #Yflip_list=Doors.out_Yflip()
    Doors_position_list=Doors.out_base_position()
    #得到实际坐标
    Doors_position_list=transPositionByPro(pro,Doors_position_list)

    for index in range(len(Doors_position_list)):
        door = Doors_position_list[index]
        #获取中轴坐标
        x1 = door[0]        
        y1 = door[1]
        x2 = door[2]
        y2 = door[3]
        #获取长度
        width=mydist(x1,y1,x2,y2)
        #获取中点
        x=(x1+x2)/2
        y=(y1+y2)/2
        #获取厚度
        left_dist=float(door[4])
        right_dist=float(door[5])

        #根据主轴决定是否调换左右宽度
        #tranRightLeftThick(x1,y1,x2,y2,left_dist,right_dist);
        if(x1==x2):
            left_dist,right_dist=right_dist,left_dist

        #获取是否反转
        #xflip=Xflip_list[index]
        #yflip=Yflip_list[index]
        xflip=-1
        yflip=-1
        #获取类型
        if Doors_type == 0:
            doortype = 2
        else:
            doortype = -1
        #获取所属墙id
        doorid=Doors_id[index]
        if doorid != -1:
            ownerwallid=str(uuid.uuid3(namespace,str(doorid)))
        else:
            ownerwallid="NOT_FOUND"



        #填入
        door = {
			'ID': str(uuid.uuid1()),
			'XFlip': xflip,
			'YFlip': yflip,
			'Location': {
				'X': x,
				'Y': y,
				'Z': 'NOT_DEFINE'
			},
			'LeftThick': left_dist,
			'RightThick': right_dist,
			'Width': width,
			'Height': 'NOT_DEFINE',
			'OwnerWallID': ownerwallid,
			'Type': doortype,
			'ArcInfo': {
				'ArchHeight': 'NOT_DEFINE'
			},
			'ModelID': "",
			'MatID': ""
		}
        wallOpenings_dict.append(door)
    return wallOpenings_dict
'''

#更新时间 2018.8.29
#此处为更新后要求：毛坯房考虑双开门及推拉门
#填入Door
#普通门（type 2）,双开门（type 3），推拉门（type 4）
def fillDoorDict(Layout,wallOpenings_dict,pro):
    doors = Layout.out_doors()
    #得到普通门
    Regular_Doors=doors[0]
    #得到普通门信息
    Regular_Doors_id=Regular_Doors.out_door_id()
    Regular_Doors_xflip=Regular_Doors.out_Xflip()
    Regular_Doors_yflip=Regular_Doors.out_Yflip()
    Regular_Doors_position=Regular_Doors.out_base_position()
    Regular_Doors_num=len(Regular_Doors_position)
    Regular_Doors_type=[2]*Regular_Doors_num

    #得到双开门
    Double_Doors=doors[1]
    #得到双开门信息
    Double_Doors_id=Double_Doors.out_door_id()
    Double_Doors_xflip=Double_Doors.out_Xflip()
    Double_Doors_yflip=Double_Doors.out_Yflip()
    Double_Doors_position=Double_Doors.out_base_position()
    Double_Doors_num=len(Double_Doors_position)
    Double_Doors_type=[3]*Double_Doors_num
    '''
    print('双开门')
    print('id',Double_Doors_id)
    print('flip',len(Double_Doors_xflip),len(Double_Doors_yflip))
    print('position',len(Double_Doors_position))
    '''

    #得到推拉门
    PullPush_Doors=doors[2]
    #得到推拉门信息
    PullPush_Doors_id=PullPush_Doors.out_door_id()
    PullPush_Doors_xflip=PullPush_Doors.out_Xflip()
    PullPush_Doors_yflip=PullPush_Doors.out_Yflip()
    PullPush_Doors_position=PullPush_Doors.out_base_position()
    PullPush_Doors_num=len(PullPush_Doors_position)
    PullPush_Doors_type=[4]*PullPush_Doors_num


    #汇总
    Id=Regular_Doors_id+Double_Doors_id+PullPush_Doors_id
    Xflip=Regular_Doors_xflip+Double_Doors_xflip+PullPush_Doors_xflip
    Yflip=Regular_Doors_yflip+Double_Doors_yflip+PullPush_Doors_yflip
    Position=Regular_Doors_position+Double_Doors_position+PullPush_Doors_position#得到实际坐标
    Position=transPositionByPro(pro,Position)
    Type=Regular_Doors_type+Double_Doors_type+PullPush_Doors_type



    for index in range(len(Position)):
        door = Position[index]
        #获取中轴坐标
        x1 = door[0]        
        y1 = door[1]
        x2 = door[2]
        y2 = door[3]
        #获取长度
        width=mydist(x1,y1,x2,y2)
        #获取中点
        x=(x1+x2)/2
        y=(y1+y2)/2
        #获取厚度
        left_dist=float(door[4])
        right_dist=float(door[5])


        #根据主轴决定是否调换左右宽度
        #tranRightLeftThick(x1,y1,x2,y2,left_dist,right_dist);
        if(x1==x2):
            left_dist,right_dist=right_dist,left_dist
               
        #获取类型
        doortype=Type[index]
        
        #获取是否反转
        #将推拉门所有flip设置为0
        if doortype == 4:
            xflip=0
            yflip=0
        else:
            xflip=Xflip[index]
            yflip=Yflip[index]

        #获取所属墙id
        doorid=Id[index]
        if doorid != -1:
            ownerwallid=str(uuid.uuid3(namespace,str(doorid)))
        else:
            ownerwallid="NOT_FOUND"
            


        #填入
        door = {
            'ID': str(uuid.uuid1()),
            'XFlip': xflip,
            'YFlip': yflip,
            'Location': {
                'X': x,
                'Y': y,
                'Z': 'NOT_DEFINE'
            },
            'LeftThick': left_dist,
            'RightThick': right_dist,
            'Width': width,
            'Height': 'NOT_DEFINE',
            'OwnerWallID': ownerwallid,
            'Type': doortype,
            'ArcInfo': {
                'ArchHeight': 'NOT_DEFINE'
            },
            'ModelID': "",
            'MatID': ""
        }
        wallOpenings_dict.append(door)
    return wallOpenings_dict


#填入Wall
#普通窗（type 10），飘窗（type 11），将阳台排除
def fillWindowsDict(Layout,wallOpenings_dict,pro):
    windows=Layout.out_windows()
    Regular_windows=windows[0]#普通窗
    Bay_windows=windows[1]#飘窗
    Balcony_windows=windows[2]#阳台

    #此处不考虑阳台
    #得到position
    Regular_position=Regular_windows.out_base_position()
    Bay_position=Bay_windows.out_base_position()
    Balcony_position=Balcony_windows.out_base_position()
    Position=Regular_position+Bay_position
    #得到实际坐标
    Position=transPositionByPro(pro,Position)
    #得到id
    Regular_id=Regular_windows.out_windows_id()
    Bay_id=Bay_windows.out_windows_id()
    Balcony_id=Balcony_windows.out_windows_id()
    Id=Regular_id+Bay_id
    #得到Xflip
    Regular_Xflip=Regular_windows.out_Xflip()
    Bay_Xflip=Bay_windows.out_Xflip()
    Balcony_Xflip=Balcony_windows.out_Xflip()
    Xflip=Regular_Xflip+Bay_Xflip
    #得到Yflip
    Regular_Yflip=Regular_windows.out_Yflip()
    Bay_Yflip=Bay_windows.out_Yflip()
    Balcony_Yflip=Balcony_windows.out_Yflip()
    Yflip=Regular_Yflip+Bay_Yflip
    #得到数目
    Regular_num=len(Regular_id)
    Bay_num=len(Bay_id)
    Balcony_num=len(Balcony_id)
    Num=Regular_num+Bay_num+Balcony_num
    #构造type
    Regular_type=[10]*Regular_num
    Bay_type=[11]*Bay_num
    Balcony_type=[-1]*Balcony_num
    Type=Regular_type+Bay_type+Balcony_type


    for index in range(len(Position)):
        window = Position[index]
        #获取中轴坐标
        x1 = window[0]        
        y1 = window[1]
        x2 = window[2]
        y2 = window[3]
        #获取长度
        width=mydist(x1,y1,x2,y2)
        #获取中点
        x=(x1+x2)/2
        y=(y1+y2)/2
        #获取厚度
        left_dist=float(window[4])
        right_dist=float(window[5])

        #根据主轴决定是否调换左右宽度
        #tranRightLeftThick(x1,y1,x2,y2,left_dist,right_dist);
        if(x1==x2):
            left_dist,right_dist=right_dist,left_dist
        
        #获取是否反转
        xflip=Xflip[index]
        yflip=Yflip[index]
        #获取类型
        wintype=Type[index]
        #获取所属墙id
        wallid=Id[index]
        if wallid != -1:
            ownerwallid=str(uuid.uuid3(namespace,str(wallid)))
        else:
            ownerwallid="NOT_FOUND"


        if wintype != -1:#排除阳台
            #填入
            window = {
                'ID': str(uuid.uuid1()),
                'XFlip': xflip,
                'YFlip': yflip,
                'Location': {
                    'X': x,
                    'Y': y,
                    'Z': 'NOT_DEFINE'
                },
                'LeftThick': left_dist,
                'RightThick': right_dist,
                'Width': width,
                'Height': 'NOT_DEFINE',
                'OwnerWallID': ownerwallid,
                'Type': wintype,
                'ArcInfo': {
                    'ArchHeight': 'NOT_DEFINE'
                },
                'ModelID': "",
                'MatID': ""
            }
            wallOpenings_dict.append(window)
    return wallOpenings_dict

#得到所有需要输出的DICT
def getDict(corners_dict,rooms_dict,walls_dict,wallOpenings_dict,electricities_dict,pillars_dict,fluePipes_dict,rulers_dict,textLabels_dict):
    Dict = {'Corners':corners_dict,
        'Rooms':rooms_dict,
        'Walls':walls_dict,
        'WallOpenings':wallOpenings_dict,
        'Electricities':electricities_dict,
        'Pillars':pillars_dict,
        'FluePipes':fluePipes_dict,
        'Rulers':rulers_dict,
        'TextLabels':textLabels_dict
        }
    return Dict

#计算两点距离                    
def mydist(x1,y1,x2,y2):
    return math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))

#根据主轴是水平还是竖直决定是否调换right left thick
def tranRightLeftThick(x1,y1,x2,y2,leftthick,rightthick):
    if(x1==x2):#此时为竖直主轴
        temp=leftthick;
        leftthick=rightthick;
        rightthick=temp;
    



#返回proportion后的坐标或距离
def transPositionByPro(pro,position):
    result=[]
    for index in range(len(position)):
        result_temp=[]
        temp=position[index]
        for index2 in range(len(temp)):
            result_temp.append(temp[index2]/pro)
        result.append(result_temp)
    return result

############无用代码############

#改变wall list，合并被门洞分开的两个wall
#如果需要合并的墙type、thick不同 如何处理
def CombineWall(list_wall,wall_id_list):
    WALL_ID=[]
    for index in range(len(list_wall)):
        wall=list_wall[index]
        wallid=wall_id_list[index]
        if wallid not in WALL_ID:
            WALL_ID.append(wallid)
        else:
            pre_index=WALL_ID.index(wallid)
            pre_wall=list_wall[pre_index]
            #得到坐标
            pre_x1 = pre_wall[0]        
            pre_y1 = pre_wall[1]
            pre_x2 = pre_wall[2]
            pre_y2 = pre_wall[3]
            x1 = wall[0]        
            y1 = wall[1]
            x2 = wall[2]
            y2 = wall[3]
            #在第二段中找离第一段最远的点
            maxx1,maxy1,point1=findfarest(pre_x1,pre_y1,x1,y1,x2,y2)
            maxx2,maxy2,point2=findfarest(x1,y1,pre_x1,pre_y1,pre_x2,pre_y2)
            #修改原wall list坐标
            list_wall[pre_index][0]=maxx1
            list_wall[pre_index][1]=maxy1
            list_wall[pre_index][2]=maxx2
            list_wall[pre_index][3]=maxy2                   
    return list_wall
        
#找到(x1,y1)(x2,y2)中离(x,y)最远的点
def findfarest(x,y,x1,y1,x2,y2):
    dist1=mydist(x,y,x1,y1)
    dist2=mydist(x,y,x2,y2)
    maxdist=max(dist1,dist2)
    if maxdist == dist1:
        return x1,y1,1
    else:
        return x2,y2,2
 