
# 血常规检验报告OCR



## 运行环境

```
# 安装numpy,
sudo apt-get install python-numpy # http://www.numpy.org/
# 安装opencv
sudo apt-get install python-opencv # http://opencv.org/

##安装OCR和预处理相关依赖
sudo apt-get install tesseract-ocr
sudo pip install pytesseract
sudo apt-get install python-tk
sudo pip install pillow

# 安装Flask框架、mongo
sudo pip install Flask
sudo apt-get install mongodb # 如果找不到可以先sudo apt-get update
sudo service mongodb started
sudo pip install pymongo
```

## 运行

```
cd  BloodTestReportOCR
python view.py # upload图像,在浏览器打开http://yourip:8080
python test.py # 自动剪切 & 识别
```

## autocut.py

autocut.py把上述算法打包成了函数。

函数原型为
```
autocut(path, times, param)
```
path是bloodtestreport2.jpg的路径，times则是读取数据的数量。
param是一些算法的参数，不设置的话填入getinfo.defalut即可。

原图在BloodTestReportOCR/origin_pics/ 文件夹下，剪切出来的图片在BloodTestReportOCR/temp_pics/ 文件夹下

函数输出为data0.jpg,data1.jpg......等一系列图片，分别是白细胞计数，中性粒细胞记数等的数值的图片。

#### 关于param

参数的形式为[p1, p2, p3 ,p4 ,p5]。
p1,p2,p3,p4,p5都是整型，其中p1必须是奇数。

p1是高斯模糊的参数，p2和p3是canny边缘检测的高低阈值，p4和p5是和筛选有关的乘数。

如果化验报告单放在桌子上时，有的边缘会稍微翘起，产生比较明显的阴影，这种阴影有可能被识别出来，导致定位失败。
解决的方法是调整p2和p3，来将阴影线筛选掉。但是如果将p2和p3调的比较高，就会导致其他图里的黑线也被筛选掉了。
参数的选择是一个问题。
我在getinfo.default中设置的是一个较低的阈值，p2=70,p3=30，这个阈值不会屏蔽阴影线。
如果改为p2=70,p3=50则可以屏蔽，但是会导致其他图片识别困难。

就现在来看，得到较好结果的前提主要有三个
 - 化验单尽量平整
 - 图片中应该包含全部的三条黑线
 - 图片尽量不要包含化验单的边缘，如果有的话，请尽量避开有阴影的边缘。


## ocr.py

识别temp_pics文件夹下的数字图片和中文图片，将结果分别存入digitdata.csv和chidata.csv
（识别中文时候前边的数字干扰很大，不知道可不可以不用数字）

#### imgproc.py 
将识别的图像进行处理二值化等操作，提高识别率
包括对中文和数字的处理

#### digits
将该文件替换Tesseract-OCR\tessdata\configs中的digits

## view.py 

Web 端上传图片到服务器，存入mongodb并获取oid

