# -*- coding: UTF-8 -*-
from ImageReader import ImageReader;
import numpy as np
import tensorflow as tf;
from PIL import Image;

# 批处理，数据设为100
batch_size = 100;
image_size = 28 * 28;

class NeuralNetwork(object):
    def __init__(self):
        self.input = tf.placeholder("float", [None, image_size]);
        self.weight = tf.Variable(tf.zeros([image_size,10]), "weight")
        self.bias = tf.Variable(tf.zeros([10]), "bias")
        self.output = tf.nn.softmax(tf.matmul(self.input, self.weight) + self.bias)
        self.sess = tf.Session();

    def load_train_images(self):
        reader = ImageReader();
        train_images = reader.load_images("mnist_data/train-images.idx3-ubyte");
        train_labels = reader.load_labels("mnist_data/train-labels.idx1-ubyte");
        train_images /= 255.0;

        return train_images, train_labels;

    def load_test_images(self):
        reader = ImageReader();
        test_images = reader.load_images("mnist_data/t10k-images.idx3-ubyte");
        test_labels = reader.load_labels("mnist_data/t10k-labels.idx1-ubyte");
        test_images /= 255.0;
        
        return test_images, test_labels;

    def train(self):
        train_images, train_labels = self.load_train_images();
        dataset_size,length = train_images.shape;
        #target 是真实值
        target = tf.placeholder("float", [None,10])
        
	    #cross_entorpy is a good cost function for softmax
        cross_entropy = -tf.reduce_sum(target * tf.log(self.output)) 
        train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
    
        labels = np.zeros((dataset_size, 10));
        for i in range(dataset_size):
            labels[i][int(train_labels[i])] = 1;
        
        self.sess.run(tf.global_variables_initializer())
        for i in range(0 , dataset_size, batch_size):
            batch_xs, batch_ys = train_images[i : i + batch_size] ,  labels[i : i + batch_size] ;
            self.sess.run(train_step, feed_dict={self.input: batch_xs, target : batch_ys})
 
    def predict_by_matrix(self, image_matrix):
        prediction = tf.argmax(self.output , 1);
        predict_value = prediction.eval(feed_dict = {self.input: image_matrix }, session = self.sess );
        return predict_value[0];

    def predict(self, imageSource):
        reader = ImageReader();
        im = Image.open(imageSource);
        print im.size;
        assert im.size == (28, 28);
        # convert image to uint8 gray image
        im = im.convert("L") 
        data = np.matrix(im.getdata(),dtype='float')/255.0;
        return self.predict_by_matrix(data);

    def get_accuracy_rate(self):
        test_images, test_labels = self.load_test_images();
        test_images_num = test_images.shape[0]; 
        accuracy = 0;

        prediction = tf.argmax(self.output , 1);
        for i in range(test_images_num):
            #此处没有用self.predict(test_images[i])的原因是函数的调用大大降低了运行速度。
            #predict_value = self.predict_by_matrix(np.mat(test_images[i]));
            predict_value = prediction.eval(feed_dict = {self.input: np.mat(test_images[i])}, session = self.sess);
            
            #predict_value是一个只含有一个数据的list，比如[1],[2],[0]
            if (predict_value[0] == int(test_labels[i])):
                accuracy = accuracy + 1;
            #print "predict: ", predict_value[0], " real: " , test_labels[i];
        return  float(accuracy) / test_images_num;

if __name__ == '__main__':
    nn = NeuralNetwork();
    nn.train();
    
    print nn.predict("test.bmp");
    accuracy_rate = nn.get_accuracy_rate();
    print "accuracy rate: " ,  accuracy_rate * 100 , "%";
