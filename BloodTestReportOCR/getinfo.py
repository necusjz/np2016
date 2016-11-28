# -*- coding: UTF-8 -*-

import cv2
import numpy as np

def getinfo(path, num):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))

    # 载入图像，灰度化，开闭运算，描绘边缘
    img = cv2.imread(path)
    img_sp = img.shape
    ref_lenth = img_sp[0] * img_sp[1] * 0.25
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gb = cv2.GaussianBlur(img_gray, (15, 15), 0)
    closed = cv2.morphologyEx(img_gb, cv2.MORPH_CLOSE, kernel)
    opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)
    edges = cv2.Canny(opened, 5 , 28)

    # 调用findContours提取轮廓
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
        if distance_arr > ref_lenth:
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
            return dis[0][1], dis[2][1]
        if dis[0][2] is dis[2][1]:
            return dis[0][2], dis[2][2]

    def cross(line1, line2):
        return line1[0]*line2[1]-line1[1]*line2[0]

    # 由三条线来确定表头的位置和表尾的位置
    line_upper, line_lower = findhead(line[2],line[1],line[0])

    # 由表头和表尾确定目标区域的位置
    total_width = line_upper[1]-line_upper[0]
    total_hight = line_lower[0]-line_upper[0]

    # 利用叉乘的不可交换性确定起始点
    cross_prod = cross(total_width, total_hight)
    if cross_prod <0:
        temp = line_upper[1]
        line_upper[1] = line_upper[0]
        line_upper[0] = temp
        temp = line_lower[1]
        line_lower[1] = line_lower[0]
        line_lower[0] = temp

    #设定透视变换的矩阵
    points = np.array([[line_upper[0][0], line_upper[0][1]], [line_upper[1][0], line_upper[1][1]], 
                    [line_lower[0][0], line_lower[0][1]], [line_lower[1][0], line_lower[1][1]]],np.float32)
    standard = np.array([[0,0], [1000, 0], [0, 600], [1000, 600]],np.float32)

    #使用透视变换将表格区域转换为一个1000*600的图
    PerspectiveMatrix = cv2.getPerspectiveTransform(points,standard)
    PerspectiveImg = cv2.warpPerspective(img, PerspectiveMatrix, (1000, 600))
    cv2.imwrite('temp_pics/1.jpg', PerspectiveImg)

    #转换后的图分辨率是已知的，所以直接从这个点开始读数据就可以了
    startpoint = [199, 40]
    skep_lenth = 5
    vertical_lenth = 37
    lateral_lenth = 80

    def getimg(i, x, y):
        region_roi = PerspectiveImg[y+skep_lenth : y+vertical_lenth, x : x+lateral_lenth]
        filename = 'temp_pics/data' + str(i) + '.jpg'
        cv2.imwrite(filename, region_roi)

    #输出图片
    if num <= 13 and num > 0:
        for i in range(num):
            getimg(int(i), startpoint[0], startpoint[1])
            startpoint[1] = startpoint[1] + 40
    elif num > 13:
        for i in range(13):
            getimg(int(i), startpoint[0], startpoint[1])
            startpoint[1] = startpoint[1] + 40
        startpoint = [702, 40]
        for i in range(num-13):
            getimg(int(i+13), startpoint[0], startpoint[1])
            startpoint[1] = startpoint[1] + 40
            
