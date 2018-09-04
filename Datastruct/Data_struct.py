'''
name        图片名字；
ruler_list  标尺的列表,列表中一个class,ruler_list[0]为标尺(class);附：近期版本暂时不区分上下左右标尺;
wall_list   墙的列表,列表中两个class,分别是wall_list[0]为承重墙(class),wall_list[1]为非承重墙(class);
door_list   门的列表,列表中三个class,分别是door_list[0]为普通门(class),door_list[1]为双开门(class),door_list[2]为推拉门(class);
window_list 窗户的列表,列表中三个class,分别是window_list[0]为普通窗户(class),window_list[1]为飘窗(class),window_list[2]为阳台(class);
wall_list   墙的列表,列表中两个class,分别是wall_list[0]为承重墙(class),wall_list[1]为非承重墙(class);
flue_list   暂时维持原状的定义(甲方还没提出相应的要求);

附:add_函数中全部用的append的操作相当于每次放入一个相应的class！！！！！！

以后主轴都这样给：[x1,y1,x2,y2,dis1,dis2]
1.如果是横着的，那么y1=y2,如果是竖着的,x1=x2,不要出现相差几个像素的情况
2. (x1,y1)(x2,y2)这两个点，靠上和靠左的在前
3. dis1是上宽度或者左宽度，dis2是下或右宽度
'''
class Layout():
    def __init__(self, name): # name为此结构对应的图片名
        self.name = name
        self.ruler_list = [] # 该图片的标尺列表
        self.wall_list = [] # 该图片的墙列表
        self.door_list = [] # 该图片的门列表
        self.window_list = [] # 该图片的窗户列表
        self.dooropening_list = [] # 该图片的门洞列表
        self.flue_list = [] # 该图片的烟道列表     
        
    def add_ruler(self, ruler_):
        self.ruler_list.append(ruler_)
        
    def add_wall(self, wall_):
        self.wall_list.append(wall_)
        
    def add_door(self, door_):
        self.door_list.append(door_)
        
    def add_window(self, window_):
        self.window_list.append(window_)
        
    def add_dooropening(self, dooropening_):
        self.dooropening_list.append(dooropening_)
        
    def add_flue(self, flue_):
        if isinstance(flue_, list):
            self.flue_list.extend(flue_)
        else:
            self.flue_list.append(flue_)
    
    def out_doors(self):
        return self.door_list
    
    def out_walls(self):
        return self.wall_list
    
    def out_windows(self):
        return self.window_list
    
    def out_ruler(self):
        return self.ruler_list
    
    def out_dooropening(self):
        return self.dooropening_list
    
    def out_flues(self):
        return self.flue_list



'''
只检测上标尺的最长的那根标尺以及上面的数字;
__data_dic               记录标尺信息;
__data_dic['proportion'] 标尺每毫米所含有的像素数量;
__data_dic['scale'] 标尺每个像素对应的毫米数;
'''
class Ruler():
    def __init__(self):
        self.__data_dic = {}
        
    def proportion(self, pro): 
        self.__data_dic['proportion'] = pro
        
    def scale(self, sc): 
        self.__data_dic['scale'] = sc  
        
    def out_proportion(self):
        return self.__data_dic['proportion']
    
    def out_scale(self):
        return self.__data_dic['scale']

'''
__type           该class存储的墙的类别(0:承重墙; 1:非承重墙);
__contour        该class存储的所有该类别墙的轮廓,比如：__contour[0]表示第一块墙的轮廓(轮廓的定义方式如下：temp[i][j][k][l],即：__contour[0]=temp[i][j][k][l]这种形式),__contour[1]表示第二块墙的轮廓,以此类推;其中,
                 temp[i][j][k][l]中i表示第几个轮廓,j表示第i个轮廓第j个点,temp[i][j][0][0]表示x坐标，temp[i][j][0][1]表示y坐标;
__wall_division  把__contour中对应的每一块墙都分割以后得到的结果，比如：__wall_division[0]表示第一块墙的轮廓分割结果(即：__wall_division[0]=[a,b,c,d,dis1,dis2]这种形式,其中,(a,b)为主轴点1,(c,d)为主轴点2,
                 dis1和dis2分别为线段两侧距离),__wall_division[1]表示第二块墙的轮廓的分割,以此类推;
__wall_id        墙的id;(同一块墙体已经合并);

附:add_函数中全部用的=的操作,也就是说只要让参数temp列表和相应的列表结构一致即可！！！！！！
'''

class Wall(object):
    def __init__(self):
        self.__contour = []
        self.__wall_division = []
        self.__type = -1
        self.__wall_id = []
        
    def set_type(self, tp):
        self.__type = tp
        
    def add_wall_division(self, temp):
        self.__wall_division = temp
    
    def add_wall_id(self, temp):
        self.__wall_id = temp
        
    def add_contour(self, temp):
        self.__contour = temp
        
    def out_type(self):
        return self.__type
    
    def out_contour(self):
        return self.__contour
    
    def out_wall_division(self):
        return self.__wall_division 
    
    def out_wall_id(self):
        return self.__wall_id


'''
__type          该class存储的门的类别(0:普通门; 1:双开门; 2:推拉门);附：在毛坯房中只有普通门的识别;
__base_position 该class存储的所有该类别的门,比如：__base_position[0]表示第一扇门,(即：__base_position[0]=[a,b,c,d,dis1,dis2]这种形式,其中,(a,b)为主轴点1,(c,d)为主轴点2,dis1和dis2分别为线段两侧距离),
                __base_position[1]表示第二扇门,以此类推;
__Xflip         __base_position对应的门基于原来门原型的X轴翻折情况(0:表示未翻折; 1:表示翻折),比如:__Xflip[i]=1,表示__base_position[i]这扇门是基于门原型X轴翻折;附：在毛坯房中Xflip未定义设置为-1;
__Yflip         __base_position对应的门基于原来门原型的Y轴翻折情况(0:表示未翻折; 1:表示翻折),比如:__Yflip[i]=1,表示__base_position[i]这扇门是基于门原型Y轴翻折;附：在毛坯房中Yflip未定义设置为-1;
__door_id        标记门属于的墙体,比如:如果__door_id[i]= j说明第i扇门属于第j块墙;

附:add_函数中全部用的=的操作,也就是说只要让参数temp列表和相应的列表结构一致即可！！！！！！
'''
class Door():
    def __init__(self):
        self.__type = -1
        self.__Xflip = []
        self.__Yflip = []
        self.__base_position = []
        self.__door_id = []
        
    def set_type(self, tp):
        self.__type = tp
    
    def add_base_position(self, temp):
        self.__base_position = temp
        
    def add_Xflip(self, temp):
        self.__Xflip = temp
        
    def add_Yflip(self, temp):
        self.__Yflip = temp

    def add_door_id(self, temp):
        self.__door_id = temp
        
    def out_type(self):
        return self.__type
    
    def out_Xflip(self):
        return self.__Xflip
    
    def out_Yflip(self):
        return self.__Yflip    
    
    def out_base_position(self):
        return self.__base_position

    def out_door_id(self):
        return self.__door_id


'''
__type          该class存储的窗户的类别(0:普通窗; 1:飘窗; 2:阳台);
__base_position 该class存储的所有该类别的窗户,比如：__base_position[0]表示第一扇窗户,(即：__base_position[0]=[a,b,c,d,dis1,dis2]这种形式,其中,(a,b)为主轴点1,(c,d)为主轴点2,dis1和dis2分别为线段两侧距离),
                __base_position[1]表示第二扇窗户,以此类推;
__Window_shape  窗户形状的定义,比如:__Window_shape[i]表示第i个窗户的形状;具体的会以图的方式给出;
__Xflip         __base_position对应的窗户基于原来窗户原型的X轴翻折情况(0:表示未翻折; 1:表示翻折),比如:__Xflip[i]=1,表示__base_position[i]这扇窗户是基于窗户原型X轴翻折;
__Yflip         __base_position对应的窗户基于原来窗户原型的Y轴翻折情况(0:表示未翻折; 1:表示翻折),比如:__Yflip[i]=1,表示__base_position[i]这扇窗户是基于窗户原型Y轴翻折;
__windows_id    标记窗户属于的墙体,比如:如果__windows_id[i]= j说明第i扇窗户属于第j块墙;

附:add_函数中全部用的=的操作,也就是说只要让参数temp列表和相应的列表结构一致即可！！！！！！
'''
class Window():
    def __init__(self):
        self.__type = -1
        self.__Xflip = []
        self.__Yflip = []     
        self.__base_position = []
        self.__windows_id = []
    
    def set_type(self, tp):
        self.__type = tp
        
    def add_base_position(self, temp):
        self.__base_position = temp  
        
    def add_Xflip(self, temp):
        self.__Xflip = temp
        
    def add_Yflip(self, temp):
        self.__Yflip = temp

    def add_windows_id(self, temp):
        self.__windows_id = temp
        
    def out_type(self):
        return self.__type
    
    def out_Xflip(self):
        return self.__Xflip
  
    def out_Yflip(self):
        return self.__Yflip
    
    def out_base_position(self):
        return self.__base_position

    def out_windows_id(self):
        return self.__windows_id



class Flue(object):
    def __init__(self):
        self.__position = [] # 烟道的位置（左上角位置）
        self.__length = -1 # 烟道的长度（指水平方向的长）
        self.__width = -1 # 烟道的宽度（指竖直方向的长）
   
    
    def set_position(self, x_min, y_min): # 烟道的坐标（左上角位置）
        self.__position.extend([x_min, y_min])
    
    def set_length(self, leng): # 设置烟道的长
        self.__length = leng
	
    def set_width(self, wid): # 设置烟道的宽度
        self.__width = wid
    
    def out_position(self): # 返回烟道的位置
        return self.__position
    
    def out_length(self): # 返回烟道的长度
        return self.__length
    
    def out_width(self): # 返回烟道的宽度
        return self.__width
