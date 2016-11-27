# -*- coding: UTF-8 -*-

import cv2
import numpy as np

def getinfo(path, times):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))

    # 载入图像，灰度化，开闭运算，描绘边缘
    img = cv2.imread(path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gb = cv2.GaussianBlur(img_gray, (15, 15), 0)
    closed = cv2.morphologyEx(img_gb, cv2.MORPH_CLOSE, kernel)
    opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)
    edges = cv2.Canny(opened, 5 , 28)

    # 调用findContours建立轮廓之间的关系
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    def getbox(i):
        rect = cv2.minAreaRect(contours[i])
        box = cv2.cv.BoxPoints(rect)
        box = np.int0(box)
        return box

    def distance(box):
        delta1 = box[0]-box[2]
        delta2 = box[1]-box[3]
        distance1 = np.dot(delta1,delta1)
        distance2 = np.dot(delta2,delta2)
        distance_avg = (distance1 + distance2) / 2
        return distance_avg

    # 筛选出对角线足够大的几个轮廓
    found = []
    for i in range(len(contours)):
        box = getbox(i)
        distance_arr = distance(box)
        if distance_arr > 800000:
            found.append([i, box])

    def getline(box):
        if np.dot(box[1]-box[2],box[1]-box[2]) < np.dot(box[0]-box[1],box[0]-box[1]):
            point1 = (box[1] + box[2]) / 2
            point2 = (box[3] + box[0]) / 2
            lenth = np.dot(point1-point2, point1-point2)
            return point1, point2, lenth
        else:
            point1 = (box[0] + box[1]) / 2
            point2 = (box[2] + box[3]) / 2
            lenth = np.dot(point1-point2, point1-point2)
            return point1, point2, lenth

    def cmp(p1, p2):
        delta = p1 - p2
        distance = np.dot(delta, delta)
        if distance < 1000:
            return 1
        else:
            return 0

    def linecmp(l1, l2):
        f_point1 = l1[0]
        f_point2 = l1[1]
        f_lenth = l1[2]
        b_point1 = l2[0]
        b_point2 = l2[1]
        b_lenth = l2[2]
        if cmp(f_point1,b_point1) or cmp(f_point1,b_point2) or cmp(f_point2,b_point1) or cmp(f_point2,b_point2):
            if f_lenth > b_lenth:
                return 1
            else:
                return -1
        else:
            return 0

    def deleteline(line, j):
        lenth = len(line)
        for i in range(lenth):
            if line[i] is j:
                del line[i]
                return

    # 将轮廓变为线
    line = []

    for i in found:
        box = i[1]
        point1, point2, lenth = getline(box)
        line.append([point1, point2, lenth])

    # 把不合适的线删去
    if len(line)>3:
        for i in line:
            for j in line:
                if i is not j:
                    rst = linecmp(i, j)
                    if rst > 0:
                        deleteline(line, j)
                    elif rst < 0:
                        deleteline(line, i)

    def distance_line(i, j):
        dis1 = np.dot(i[0]-j[0], i[0]-j[0])
        dis2 = np.dot(i[0]-j[1], i[0]-j[1])
        dis3 = np.dot(i[1]-j[0], i[1]-j[0])
        dis4 = np.dot(i[1]-j[1], i[1]-j[1])
        return min(dis1, dis2, dis3, dis4)

    def findhead(i, j, k):
        dis = []
        line = []
        max_dis = 0
        dis.append([distance_line(i, j), i, j])
        dis.append([distance_line(j, k), j, k])
        dis.append([distance_line(k, i), k, i])
        dis.sort()
        if dis[0][1] is dis[2][2]:
            return dis[0][2], dis[2][1]
        if dis[0][2] is dis[2][1]:
            return dis[0][1], dis[2][2]

    def cross(line1, line2):
        return line1[0]*line2[1]-line1[1]*line2[0]

    # 由三条线来确定表头的位置和表尾的位置
    line_upper, line_lower = findhead(line[2],line[1],line[0])

    # 由表头和表尾确定目标区域的位置
    total_width = line_upper[1]-line_upper[0]
    total_hight = line_lower[0]-line_upper[0]
    startpoint = line_upper[0]

    # 利用叉乘的不可交换性确定起始点
    cross_prod = cross(total_width, total_hight)
    if cross_prod <0:
        total_width = -total_width
        startpoint = line_upper[1]
    
    #由于透视的问题，读取右边的数据以右轴作为参考
    total_hight_r = line_lower[1]-line_upper[1] 
    startpoint_r = startpoint + total_width / 2

    def getregion(i, startpoint, ref_axis):
        info_region = []
        info_start = total_width / 4.8 + startpoint
        info_region.append(info_start)
        info_ll = ref_axis / 15 + info_start
        info_region.append(info_ll)
        info_rl = total_width / 12 + info_ll
        info_region.append(info_rl)
        info_ru = total_width / 12 + info_start
        info_region.append(info_ru)

        def sort_points(points):
            point_lenth = len(points)
            for i in range(point_lenth):
                for j in range(point_lenth-1):
                    if points[j][0] > points[j+1][0]:
                        temp = points[j+1]
                        points[j+1] = points[j]
                        points[j] = temp
            return points

        def mostclose_lu(points):
            points = sort_points(points)
            if points[0][1]<points[1][1]:
                return points[0], points[1]
            else:
                return points[1], points[0]

        def mostclose_ru(points):
            points = sort_points(points)
            if points[2][1]<points[3][1]:
                return points[2]
            else:
                return points[3]

        # 获取截取区域的左上角，右上角，左下角的坐标，截取图片
        lu_point , ll_point = mostclose_lu(info_region)
        ru_point = mostclose_ru(info_region)
        filename = 'target' + str(i) + '.jpg'

        region_roi = img[int(lu_point[1]):int(ll_point[1]), int(lu_point[0]):int(ru_point[0])]
        cv2.imwrite(filename, region_roi)

        return startpoint + ref_axis / 14

    if times < 14 and times > 0:
        for i in range(int(times)):
            startpoint = getregion(i, startpoint, total_hight)
    elif times >= 14:
        for i in range(13):
            startpoint = getregion(i, startpoint, total_hight)
        startpoint = startpoint_r
        for i in range(int(times)-13):
            startpoint = getregion(i+13, startpoint, total_hight_r)