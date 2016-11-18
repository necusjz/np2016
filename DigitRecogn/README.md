# 神经网络实现手写字符识别系统

BP神经网络

损失函数：矩阵求差, 权更新步长0.1

激励函数：sigmoid

保存文件：nn.json

1,安装numpy包

python2

pip install --upgrade pip && pip install numpy

python3

pip3 install --upgrade pip && pip3 install numpy

2,下载图像和标签数据

wget http://labfile.oss.aliyuncs.com/courses/593/data.csv
wget http://labfile.oss.aliyuncs.com/courses/593/dataLabels.csv

3,训练模型

python neural_network_design.py

4,创建服务器

python -m SimpleHTTPServer 3000

5,加载服务器

python server.py

6,访问

localhost:3000


* 实现指导见https://www.shiyanlou.com/courses/593