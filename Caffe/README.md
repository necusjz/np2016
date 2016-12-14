Caffe的优势是能够方便地使用图片进行训练和测试，缺点不够灵活。
caffe的安装：
1、安装基本依赖
sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler
sudo apt-get install --no-install-recommends libboost-all-dev
由于ubuntu的库有各种依赖关系，apt－get可能无法解决，建议使用aptitude，会给出多个解决方案，实测可行！sudo aptitude install ...
2、若不使用gpu，可以跳过安装cuda！（而且好像16.04已经带有cuda8）
3、安装ATLAS
sudo apt-get install libatlas-base-dev

4、下载caffe
git clone https://github.com/BVLC/caffe.git

5、修改Makefile.config
cd caffe
cp Makefile.config.example Makefile.config 
gedit Makefile.config
将# cpu_only := 1的注释去掉，找到并修改为：
INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include /usr/include/hdf5/serial
LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib /usr/lib/i386-linux-gnu/hdf5/serial

6、编译安装
make all
make test
make runtest

到此caffe安装已经完成！
若有需要用到python或matlab接口的，先设置好Makefile.config中的路径，再另外编译：
make pycaffe
make matcaffe

添加python环境变量，方便以后imoprt caffe，打开/etc/profile末尾添加：
PYTHONPATH=/xxx/xxx/caffe/python:$PYTHONPATH

另外pycaffe的接口暴露在caff目录下的python文件夹，只需要import caffe就可以直接调用。
matcaffe接口官网有介绍。

使用caffe进行mnist手写数字网络训练和识别：
1、下载数据集：
./data/mnist/get_mnist.sh
./examples/mnist/create_mnist.sh

2、定义神经网络（caffe已定义）：
/examples/mnist/lenet_train_test.prototxt

3、定义配置文件（caffe已定义）：
/examples/mnist/lenet_solver.prototxt

4、训练：
./examples/mnist/train_lenet.sh

训练完成后在/examples/mnist/下会有训练好的模型：lenet_iter_10000.caffemodel
可直接用于我们的手写识别系统

使用pycaffe进行识别（集成到A1中，但还没实现实时训练）：

python -m SimpleHTTPServer 3000
python server.py

其中改写了ocr.js生成一张帆布的图片以作为网络的输入，server.py调用caffe_predict.py进行识别。
caffe_predict.py的代码思路是：
1、以网络结构（.prototxt）、模型（.caffemodel）、均值文件（.npy）构建完整网络
2、图片预处理设置
3、加载图片
4、处理图片
5、向前传播
6、输出结果
