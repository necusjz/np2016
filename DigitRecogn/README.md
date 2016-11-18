# 神经网络实现手写字符识别系统

BP神经网络
步长0.1
激励函数 sigmoid
保存文件 nn.json

1,下载图像和标签数据

wget http://labfile.oss.aliyuncs.com/courses/593/data.csv
wget http://labfile.oss.aliyuncs.com/courses/593/dataLabels.csv

2,训练模型

python neural_network_design.py

3,创建服务器

python -m SimpleHTTPServer 3000

4,加载服务器

python server.py

5,访问

localhost:3000


* 实现指导见https://www.shiyanlou.com/courses/593