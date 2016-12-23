*Caffe的优势是能够方便地使用图片进行训练和测试，缺点是不够灵活。*
##caffe的安装：
**1、安装基本依赖**

```
sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler
```

```
sudo apt-get install --no-install-recommends libboost-all-dev
```

	由于ubuntu的库有各种依赖关系，apt－get可能无法解决，建议使用aptitude，会给出多个解决方案，实测可行！
	sudo aptitude install ...

**2、若不使用gpu，可以跳过安装cuda！（而且好像16.04已经带有cuda8）**

**3、安装ATLAS**

```
sudo apt-get install libatlas-base-dev
```

**4、下载caffe**

```
git clone https://github.com/BVLC/caffe.git
```

**5、修改Makefile.config**

```
cd caffe
cp Makefile.config.example Makefile.config 
gedit Makefile.config
```

将# cpu_only := 1的注释去掉，找到并修改为：

```
INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include /usr/include/hdf5/serial
LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib /usr/lib/i386-linux-gnu/hdf5/serial
```

**6、编译安装**

```
make all
make test
make runtest
```

到此caffe安装已经完成！
若有需要用到python或matlab接口的，先设置好Makefile.config中的路径，再另外编译：

```
make pycaffe
make matcaffe
```

添加python环境变量，方便以后imoprt caffe，打开/etc/bash.bashrc末尾添加：

```
PYTHONPATH=/xxx/xxx/caffe/python:$PYTHONPATH
```

	另外pycaffe的接口暴露在caff目录下的python文件夹，只需要import caffe就可以直接调用。matcaffe接口官网有介绍。

##使用caffe进行mnist手写数字网络训练和识别：
**1、下载数据集：**

```
./data/mnist/get_mnist.sh
./examples/mnist/create_mnist.sh
```

**2、定义神经网络（caffe已定义）：**

```
/examples/mnist/lenet_train_test.prototxt
```

**3、定义配置文件（caffe已定义）：**

```
/examples/mnist/lenet_solver.prototxt
```

**4、训练：**

```
./examples/mnist/train_lenet.sh
```

	训练完成后在/examples/mnist/下会有训练好的模型：lenet_iter_10000.caffemodel可直接用于我们的手写识别系统

##使用pycaffe进行识别：

```
python -m SimpleHTTPServer 3000
python server.py
```

	其中改写了ocr.js生成一张帆布的图片以作为网络的输入，server.py调用caffe_predict.py进行识别。

caffe_predict.py的代码过程是：

**1、以网络结构（.prototxt）、模型（.caffemodel）和均值文件（.npy）构建完整网络**

**2、图片预处理设置**

**3、加载图片**

**4、处理图片**

**5、向前传播**

**6、输出结果**


**关于均值文件的生成：**

```
sudo build/tools/compute_image_mean examples/mnist/mnist_train_lmdb examples/mnist/mean.binaryproto
```
	得到mean.binaryproto，但pycaffe要求使用npy格式的均值文件，需要进行转化，使用convert_mean.py:

```
python convert_mean.py mean.binaryproto mean.npy
```
**关于使用pycaffe训练：**

	需要根据训练集配置好lenet_solver.prototxt和lenet_train.protxt里面的参数，因为没有发现适当的pycaffe接口，需要手工运行脚本把图片转换成lmdb格式，
	再运行train.py进行训练，见train.txt、create_lmdb.sh和train.py。
	注意脚本create_lmdb.sh中的路径需要修改。
	train.txt中存放的是训练文件列表和标签。

将train.txt中的文件转换为lmdb文件：
```
sh create_lmdb.sh
```
训练数据,生成模型：
```
python train.py
```
##prototxt网络模型绘制成可视化图片

draw_net.py可以将网络模型由prototxt变成一张图片，draw_net.py存放在caffe根目录下python文件夹中。

绘制网络模型前，先安装两个库：ＧraphViz和pydot

**1.安装ＧraphViz**

Graphviz的是一款图形绘制工具，用来被python程序调用绘制图片

    sudo apt-get install GraphViz

**2.安装pydot**

pydot是python的支持画图的库

    sudo pip install pydot

**3.编译pycaffe**

    make pycaffe

完成上面三个步骤之后，就可以绘制网络模型了，draw_net.py执行的时候带三个参数

第一个参数：网络模型的prototxt文件

第二个参数：保存的图片路径及名字

第二个参数：–rankdir=x , x 有四种选项，分别是LR, RL, TB, BT 。用来表示网络的方向，分别是从左到右，从右到左，从上到小，从下到上。默认为ＬＲ。

**绘制Lenet模型**

在caffe根目录下

    python python/draw_net.py examples/mnist/lenet_train_test.prototxt ./lenet_train_test.jpg --rankdir=BT

绘制完成后将会生成lenet_train_test.jpg
