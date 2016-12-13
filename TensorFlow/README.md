# Tensorflow框架下的mnist手写字符识别
- 两层BP神经网络，输入层和输出层
- 学习率0.01
- 训练数据集是60000个28x28的ubyte手写字符数据，测试数据集是10000个28x28的ubyte手写字符数据
- 输出层用softmax函数做分类器，损失函数是cross entropy
- 批处理大小为100

### 环境配置
系统: ubuntu 14.04 / ubuntu 16.04 

    # 下载mnist数据集，并把数据集放到TensorFlow下的mnist_data文件夹内  
    https://pan.baidu.com/s/1bBI0Ku 
    
    # 安装pip，如果安装过了，则跳过此步
    sudo apt-get install python-pip

    # 安装numpy，如果安装了，则跳过此步
    sudo apt-get install python-numpy
    
    # 安装PIL，如果安装过了，则跳过此步
    sudo apt-get install python-imaging
    
    # 安装Tensorflow
    pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.12.0rc0-cp27-none-linux_x86_64.whl

### 运行
    python mnist.py

### 解释
1. ImageReader.py 
   ImageReader.py封装了一个可以读取mnist ubyte数据集的类。load_images用于读取训练数据或测试数据，load_labels用于读取标签数据
2. mnist.py 
   load_train_images用于读取并返回训练数据和标签数据，load_test_images用于读取并返回测试数据和标签数据。train函数用于训练，predict读取的是一个图片，用于预测一个28x28的手写字符数据，predict_by_matrix读取的是一个size为1 x 784的矩阵，并返回一个预测值。