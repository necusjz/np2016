# -*- coding: UTF-8 -*-

# 判断是否血常规检验报告，输入经过矫正后的报告图像
def isReport(img):
    # add your code here
    return True

# 根据剪裁好的项目名称图片获得该项目的分类号，注意不是检验报告上的编号，是我们存储的编号
num = 0
def getItemNum(img):
    # replace your code
    global num
    if num >= 22:
        num = 0
    ret = num
    num = num + 1
    return ret

# unit test
if __name__ == '__main__':
    import classifier

    img = []
    if classifier.isReport(img) :
        print 'classifier.isReport(img) is True'
    for i in range(33):
        print classifier.getItemNum(img)