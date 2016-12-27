# 利用CAFFE预测病人性别,正确率只有67%，还可以通过优化网络结构进行提升

## 环境配置(Ubuntu 14.04或以上版本)

如果还有模块没有安装，可以使用如下命令安装
```
sudo pip install module_name
```


## 使用
1. 在当前目录下建立两个数据库文件夹，test_data_lmdb，train_data_lmdb

```
mkdir test_data_lmdb train_datalmdb
```
2. 运行data_process.py
```
python data_process.py
```

注意：重复运行create_data_lmdb()并不会覆盖原来的文件，而是会在原文件结尾处继续生成新数据，如
果需要重新调试，可以删除两个文件

相关资料链接：
官网上神经网络搭建实例：
http://nbviewer.ipython.org/github/joyofdata/joyofdata-articles/blob/master/deeplearning-with-caffe/Neural-Networks-with-Caffe-on-the-GPU.ipynb

layer 详解：
http://blog.csdn.net/u011762313/article/details/47361571#sigmoid
