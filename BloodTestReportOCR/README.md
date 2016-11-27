# 血常规检验报告OCR




##test.py的使用方法


####运行环境
运行需要opencv和numpy

```

# 安装numpy,
sudo apt-get install python-numpy # http://www.numpy.org/

# 安装opencv
sudo apt-get install python-opencv # http://opencv.org/

# matplotlib
sudo apt-get install tcl8.5 tk8.5   python-tk python-matplotlib # http://matplotlib.org/

```


####运行

 - 将test.py和bloodtestreport2.jpg放在同一文件夹下

 - 执行

```
python test.py # have problem
python getinfo_sample.py # it works
```

 - 运行过程中会显示图像处理的中间结果，每次弹出图片之后按任意键继续

 - 最后会生成一个名为targrt.jpg的图片，其中包含“白细胞计数”的数值

##getinfo.py
getinfo.py把上述算法打包成了函数。

函数原型为
```
getinfo(path, times)
```
path是bloodtestreport2.jpg的路径，times则是读取数据的数量。

函数输出为target0.jpg,target1.jpg......等一系列图片，分别是白细胞计数，中性粒细胞记数等的数值的图片。

我还没做图形旋转的功能。正向的图片截出来的图是正向的，旋转了90度，180度，270度的图片截出来的图也是旋转了90度，180度，270度的。

##getinfo_sample.py
这是一个调用getinfo.py的范例