 
# PaddlePaddle图像分类demo



## 安装PaddlePaddle
# http://www.paddlepaddle.org/doc_cn/build_and_install/install/ubuntu_install.html
```
# 下载安装包
wget https://github.com/PaddlePaddle/Paddle/releases/download/V0.8.0b1/paddle-cpu-0.8.0b1-Linux.deb

# 安装
gdebi paddle-cpu-0.8.0b1-Linux.deb
如果 gdebi 没有安装,则需要使用 sudo apt-get install gdebi, 来安装 gdebi 。
或者使用下面一条命令安装.
dpkg -i paddle-cpu-0.8.0b1-Linux.deb
apt-get install -f
在 dpkg -i 的时候如果报一些依赖未找到的错误是正常的， 在 apt-get install -f 里会继续安装 PaddlePaddle
```

## 下载MNIST数据集
从https://pan.baidu.com/s/1kUNBkyz下载MNIST.rar，解压到data文件夹下
注该数据集将原版MNIST二进制文件中的图片提取出来分别放入train和test文件夹，用户可以自行添加图片到train和test文件夹下，但要修改源码中关于图像大小的参数

## 运行

```
sh preprocess.sh # 调用preprocess.py 预处理
sh train.sh # 调用vgg.py训练，该脚本文件可设置训练模型存放路径和训练线程数等参数
python prediction.py # 预测，注意设置其中模型路径model_path
```

## preprocess.py 

预处理模块，将data文件夹下的图片转换为PaddlePaddle格式
转换后的数据存放在data/batches文件夹下

## vgg.py

训练模块，使用VGG网络训练，该网络在ILSVRC2014的图像分类项目上获第二名
训练后的模型存放在vgg_model/pass-*文件夹下，*表示第几次训练，每训练一次会生成一个模型文件夹，理论上训练次数越多的模型效果越好
注使用CPU训练速度很慢，平均训练一次需要近半小时，目前PaddlePaddle使用CPU训练出来的模型和GPU训练出来的模型不一样，所以用CPU训练只能用CPU预测，用GPU训练只能用GPU预测，而且用GPU预测要安装GPU版的PaddlePaddle和CUDA，cudnn,并且需要NVIDIA显卡支持，所以这里用的是CPU版的

## prediction.py

预测模块，其中image参数为要识别的图像路径

## image_provider.py

实现向PaddlePaddle提供数据的接口，详见image_provider.py注释