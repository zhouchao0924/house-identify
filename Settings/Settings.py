# -*- coding: utf-8 -*-
"""
Created on Fri Aug 03 15:12:41 2018

@author: 王科涛
"""



'''
threshold 二值化图像的阈值;
'''
threshold = 250


'''
Bearingwall_thre 灰度值图像找出承重墙的阈值,小于Bearingwall_thre的部分被认为是有可能是承重墙的部分;
'''
Bearingwall_thre = 20

'''
Nonbearingwall_thre 灰度值图像找出非承重墙的阈值,小于Nonbearingwall_thre的部分被认为是有可能是非承重墙的部分;
'''
Nonbearingwall_thre = 170

'''
rect_position_min_thre 两层rect窗识别中外接矩形最小阈值;
rect_position_max_area 两层rect窗识别中外接矩形和实际面积最大差距;
rect_two_min_thre      窗户中第一个和第二个矩形长宽比最小值(长的：短的);
rect_two_max_dis       窗户中矩形间最大间隔;
rect_two_max_long      窗户中第二个矩形和第一个矩形两边最大相差间隔;
rect_two_pro           图的比例尺像素：毫米;
rect_two_min_kuan      窗户的最小实际宽度;
rect_two_max_kuan      窗户的最大实际宽度;


piao_position_min_thre 两层piao窗识别中外接矩形最小阈值;
piao_position_max_area 两层piao窗识别中外接矩形和实际面积最大差距(百分比);
piao_two_max_dis       窗户中矩形相邻限制;
piao_two_max_offset    窗户左右宽度之间相差最大值;
piao_two_min_kuan      窗户的最小实际宽度;
piao_two_max_kuan      窗户的最大实际宽度;
'''
rect_position_min_thre = 20000
rect_position_max_area = 10000
rect_two_min_thre = 2.0
rect_two_max_dis = 20
rect_two_max_long = 15
rect_two_min_kuan = 70
rect_two_max_kuan = 300

piao_position_min_thre = 60000
piao_position_max_area = 0.4
piao_two_max_dis = 5
piao_two_max_offset = 10
piao_two_min_kuan = 70
piao_two_max_kuan = 300

judge_win_thres1=1000
judge_win_thres2=3000

'''
sobel_thre 转换成梯度图的阈值
'''
sobel_thre=25

'''
min_rectangle_area   矩形最小面积
max_rectangle_area   矩形最大面积
min_ratio            矩形最小纵横比
max_ratio            矩形最大纵横比
max_lenth            矩形最大长度

min_sliding_ratio    推拉门两个矩形之间的比例最小值
max_sliding_ratio    推拉门两个矩形之间的比例最大值
max_distance         两个细矩形之间的最大距离
min_jiaocuo          两个细矩形至少交错开多少
min_xiangcha         两个细矩形短的那条边的长度最多相差多少
'''
min_rectangle_area = 50
max_rectangle_area = 20000
min_ratio = 0.005
max_ratio = 0.2
max_lenth = 1000
min_sliding_ratio = 0.8
max_sliding_ratio = 1.2
max_distance = 8
min_jiaocuo = 20
min_xiangcha = 5

'''
inner 表示从底座往内部多少个像素开始
outer 表示距离 水平细矩形上下/竖直细矩形左右 多少像素开始搜
double_minsca,double_maxsca 两边找到的点距离底座的距离的比值范围
middle_maxdis_sca 中间找到的点的距离/两边距离的最大值
min_times 底座的长度至少是边的多少倍
middle_dis 中间点距离底座的最大距离
'''
inner = 5
outer = 6
double_minsca = 0.8
double_maxsca = 1.2
middle_maxdis_sca = 0.3
min_times = 1.3
middle_dis = 15
'''
max_error  细矩形和封闭扇形端点连接处的所允许的偏差
inner_dis 表示细矩形端点往里多少个像素
thre 表示距离 水平细矩形上下/竖直细矩形左右 多少像素开始搜
min_sca 门纵横比的下界
max_sca 门纵横比的上界
max_dis 两个水平相邻门y坐标的距离最大值，竖直相邻门x坐标的距离最大值
min_len,max_len:门宽度的最小最大值(实际数值：0.7m-1m)
err 误差
'''
max_error = 10
inner_dis = 2
thre = 6
min_sca = 0.6
max_sca = 1.4
max_dis = 30
min_len = 550
max_len = 1150
err = 130
'''
door_width_min 门的最小宽度
wall_width_min 墙的最小宽度
'''
door_width_min = 300
wall_width_min = 50
'''
max_area_wall_thre 墙的最大面积
wall_width_max_nonbear 非承重墙的最大宽度
wall_width_max_bear 承重墙的最大宽度
seg_length_min 线段的最小像素长度
'''
max_area_wall_thre = 500000
wall_width_max_nonbear = 400
wall_width_max_bear = 650
seg_length_min = 3
'''
sliding_door_width_max 推拉门的最大长度
normal_door_width_max 普通门的最大长度
'''
sliding_door_width_max = 4000
normal_door_width_max = 1500
'''
min_radius_arc 门的最小半径
max_radius_arc 门的最大半径
max_arc_dis    门的弧线与标准弧线的最大距离
max_search_point_dis 寻找黑色点的最大搜索距离
max_points_num 门的弧线与标准弧线最多有几个点没有匹配
max_dis_center 门的圆心的距离
max_search_wall 寻找墙的距离
max_width_wall  墙的最大宽度
min_width_wall  墙的最小宽度
thres_search_wall 判断是否是墙的阈值
thres_is_blank  判断门的底座是否是空白的阈值
thres_black_line 判断是否是黑色线的阈值
'''
min_radius_arc = 540       #实际
max_radius_arc = 1200       #实际
max_arc_dis = 900          #实际
max_search_point_dis = 100  #实际
max_points_num = 120        #实际
max_dis_center = 300       #实际
max_search_wall = 200      #实际
max_width_wall = 400      #实际
min_width_wall = 70      #实际
thres_search_wall = 0.95
thres_is_blank = 0.95
thres_black_line = 0.9
'''
百度OCR的id和key
APP_ID
API_KEY
SECRET_KEY
'''
APP_ID = ['11654935','11654170','11658267','11707427']  
API_KEY = ['CMwnTVkeFHBwi46vYqLWONZM','4ilACRjjzeeAnYGsc2o5gyr3','SdGs7FDmneBVNB9ZtSfpCx60','5salRmGeT15pGWpdimFKkHuY']  
SECRET_KEY = ['0hWxttc57Yu7BdSU0rzLQZKqrRb2y4FC','D7McsE61uhhs9vrldTtkGekGU3NAtm0A','0hWxttc57Yu7BdSU0rzLQZKqrRb2y4FC','0t2FOWcMuzjvmq1VlFBvB0XZqAuGUKAB']  