# 血常规检验报告OCR


##test.py的使用方法


####运行环境
运行需要opencv和numpy

```

# 安装numpy,
sudo apt-get install python-numpy # http://www.numpy.org/

# 安装opencv
sudo apt-get install python-opencv # http://opencv.org/

```


####运行

```
cd  BloodTestReportOCR
python test.py
python getinfo_sample.py
```

 - 运行过程中会显示图像处理的中间结果，每次弹出图片之后按任意键继续

 - 最后会生成一个名为convert.jpg的图片和一个名为data0.jpg的图片，其中包含“白细胞计数”的数值

##getinfo.py
getinfo.py把上述算法打包成了函数。

函数原型为
```
getinfo(path, times, param)
```
path是bloodtestreport2.jpg的路径，times则是读取数据的数量。
param是一些算法的参数，不设置的话填入getinfo.defalut即可

原图在BloodTestReportOCR/origin_pics/ 文件夹下，剪切出来的图片在BloodTestReportOCR/temp_pics/(源图片名)/ 文件夹下

函数输出为data0.jpg,data1.jpg......等一系列图片，分别是白细胞计数，中性粒细胞记数等的数值的图片。

##getinfo_sample.py
这是一个调用getinfo.py的范例