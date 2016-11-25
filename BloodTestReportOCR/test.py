import cv2
from matplotlib import pyplot as plt
import numpy as np
import math

def show(img):
    cv2.namedWindow("Image")   
    cv2.imshow("Image", img)   
    cv2.waitKey (0)  
    cv2.destroyAllWindows()  

img = cv2.imread('bloodtestreport2.jpg')
show(img)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
show(img_gray)
img_gb = cv2.GaussianBlur(img_gray, (15, 15
), 0)
show(img_gb)
edges = cv2.Canny(img_gb, 5 , 28)
show(edges)

contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

hierarchy = hierarchy[0]

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
    distance_arr = (distance1 + distance2) / 2
    return distance_arr

found = []

draw_img = img.copy()
for i in range(len(contours)):
    box = getbox(i)
    distance_arr = distance(box)
    if distance_arr > 800000:
        found.append([i, box])

for i in found:
    img_dc = img.copy()
    box = i[1]
    cv2.drawContours(img_dc, contours, i[0], (0, 255, 0), 3)
    cv2.drawContours(img_dc,[box], 0, (0,0,255), 2)
    show(img_dc)


def getline(box):
    point1 = (box[1] + box[2]) / 2
    point2 = (box[3] + box[0]) / 2
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

line = []

for i in found:
    box = i[1]
    point1, point2, lenth = getline(box)
    line.append([point1, point2, lenth])

if len(line)>3:
    for i in line:
        for j in line:
            if i[2] != j[2]:
                rst = linecmp(i, j)
                if rst > 0:
                    line.remove(j)
                elif rst < 0:
                    line.remove(i)

for i in line:
    print((i[0][0],i[0][1]),(i[1][0],i[1][1]))

img_line = img.copy()
for i in line:
    cv2.line(img_line,(i[0][0],i[0][1]),(i[1][0],i[1][1]),(0,0,255),5)
    show(img_line)