# 血常规检验报告OCR



##test.py的使用方法

###运行环境
运行需要opencv和numpy
```
# 安装numpy
sudo apt-get install python-numpy
# 安装opencv
sudo apt-get install python-opencv
```

###运行
 - 将test.py和bloodtestreport2.jpg放在同一文件夹下
 - 执行
```
python test.py
```
 - 运行过程中会显示图像处理的中间结果，每次弹出图片之后按任意键继续
 - 最后会生成一个名为targrt.jpg的图片，其中包含“白细胞计数”的数值
