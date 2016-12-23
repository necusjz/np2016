#定义了添加层函数，进行年龄预测作业。通过升维，使不同数输出节点不同，
#以及非常长时间的调参，找到比较好的结果，
#设置2隐藏层。隐藏层节点数按出入节点75%。
#使年龄预测率提高到23%左右，最高25%。
#其典型的bp神经网络模型流程可借鉴。———SA312


import tensorflow as tf
import numpy as np
import csv
import math


label_orign2 = []
data_orign2 = []
sex_orign2 = []
age_orign2 = []

#读预测数据
with open('predict.csv','rb') as precsv2:
	reader2 = csv.reader(precsv2)
	for line2 in reader2:
		
		if reader2.line_num == 1:
			continue 
		label_origntemp2 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]     #升维度
		label_origntemp2.insert(int(math.floor(float(line2[2])/10)),float(math.floor(float(line2[2])/10)))
		label_orign2.append(label_origntemp2)
		data_orign2.append(line2[3:]) 
label_np_arr2 = np.array(label_orign2)
data_np_arr2 = np.array(data_orign2)
sex_np_arr2 = np.array(sex_orign2)

data_len2 = data_np_arr2.shape[1]
data_num2 =  data_np_arr2.shape[0]



label_orign = []
data_orign = []
sex_orign = []
age_orign = []
#读训练数据
with open('train.csv','rb') as precsv:
	reader = csv.reader(precsv)
	for line in reader:
		
		if reader.line_num == 1:
			continue
		label_origntemp = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]      #升维度
		label_origntemp.insert(int(math.floor(float(line[2])/10)),float(math.floor(float(line[2])/10)))
		label_orign.append(label_origntemp)   
		data_orign.append(line[3:])  
label_np_arr = np.array(label_orign)
data_np_arr = np.array(data_orign)
#sex_np_arr = np.array(sex_orign)


data_len = data_np_arr.shape[1]
data_num =  data_np_arr.shape[0]

#添加层函数
def add_layer(inputs,in_size,out_size,activation_function=None):

    Ws = tf.Variable(tf.random_normal([in_size,out_size]))
    bs = tf.Variable(tf.zeros([1,out_size])+0.5)
    
    Wxpb = tf.matmul(inputs,Ws) + bs
  
    if activation_function is None:
        outputs = Wxpb
    else:
        outputs = activation_function(Wxpb)
    return outputs
#比较函数
def compute_accuracy(v_xs,v_ys):
	global prediction
	y_pre = sess.run(prediction,feed_dict={xs:v_xs})
	correct_prediction = tf.equal(tf.argmax(y_pre,1),tf.argmax(v_ys,1))
	accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
	result = sess.run(accuracy,feed_dict={xs:v_xs,ys:v_ys})
	return result
	


xs = tf.placeholder(tf.float32,[None,data_len])
ys = tf.placeholder(tf.float32,[None,10])

#3个隐藏层
l1 = add_layer(xs,data_len,19,activation_function=tf.nn.sigmoid)

l2 = add_layer(l1,19,19,activation_function=tf.nn.sigmoid)

l3 = add_layer(l2,19,19,activation_function=tf.nn.sigmoid)

prediction = add_layer(l3,19,10,activation_function=tf.nn.softmax)




cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys*tf.log(prediction),reduction_indices=[1]))

train_step = tf.train.GradientDescentOptimizer(0.1).minimize(cross_entropy)


init = tf.initialize_all_variables()

saver = tf.train.Saver()
sess = tf.Session()
sess.run(init)

for i in range(10000):
	sess.run(train_step,feed_dict={xs:data_np_arr,ys:label_np_arr.reshape((data_num,10))})
	if i%50 == 0:
		print(compute_accuracy(data_np_arr2,label_np_arr2.reshape((data_num2,10))))

	
