=======
# 血常规检验报告OCR


##test.py的使用方法


####运行环境
运行需要opencv、numpy、tesseract、pytesseract

```

# 安装numpy,
sudo apt-get install python-numpy # http://www.numpy.org/

# 安装opencv
sudo apt-get install python-opencv # http://opencv.org/

##安装tesseract
sudo apt-get install tesseract-ocr

##安装pytesseract
sudo pip install pytesseract

```


####运行

```
cd  BloodTestReportOCR
python test.py
python getinfo_sample.py
python ocr.py
```

 - 运行过程中会显示图像处理的中间结果，每次弹出图片之后按任意键继续

 - 最后会生成一个名为convert.jpg的图片和一个名为data0.jpg的图片，其中包含“白细胞计数”的数值

##getinfo.py
getinfo.py把上述算法打包成了函数。

函数原型为
```
getinfo(path, times, param)
```
path是bloodtestreport2.jpg的路径，times则是读取数据的数量。
param是一些算法的参数，不设置的话填入getinfo.defalut即可。

原图在BloodTestReportOCR/origin_pics/ 文件夹下，剪切出来的图片在BloodTestReportOCR/temp_pics/ 文件夹下

函数输出为data0.jpg,data1.jpg......等一系列图片，分别是白细胞计数，中性粒细胞记数等的数值的图片。

##关于param
参数的形式为[p1, p2, p3 ,p4 ,p5]。
p1,p2,p3,p4,p5都是整型，其中p1必须是奇数。

p1是高斯模糊的参数，p2和p3是canny边缘检测的高低阈值，p4和p5是和筛选有关的乘数。

如果化验报告单放在桌子上时，有的边缘会稍微翘起，产生比较明显的阴影，这种阴影有可能被识别出来，导致定位失败。
解决的方法是调整p2和p3，来将阴影线筛选掉。但是如果将p2和p3调的比较高，就会导致其他图里的黑线也被筛选掉了。
参数的选择是一个问题。
我在getinfo.default中设置的是一个较低的阈值，p2=70,p3=30，这个阈值不会屏蔽阴影线。
如果改为p2=70,p3=50则可以屏蔽，但是会导致其他图片识别困难。

就现在来看，得到较好结果的前提主要有三个
 - 化验单尽量平整
 - 图片中应该包含全部的三条黑线
 - 图片尽量不要包含化验单的边缘，如果有的话，请尽量避开有阴影的边缘。

##getinfo_sample.py
这是一个调用getinfo.py的范例

##ocr.py
将temp_pics文件夹下的图片识别到temp_nums文件下


# A2.5 Web 端上传图片到服务器，存入mongodb并获取oid
## 实现图片上传到服务器并写入mongodb
### Requirements
 - python 2.7
 - Flask
 - mongoDB
 - pymongo

### Flask web框架安装
安装[Flask](http://flask.pocoo.org/docs/0.11/quickstart/)
```
pip install Flask
```
### Mongodb 安装
安装[mongoDB](https://docs.mongodb.com/manual/installation/)
```
// ubuntu 16.04
echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
// ubuntu 14.04
echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list

//国外repo直接安装太慢，因此这里把你的Ubuntu软件源更换为aliyun或者中科大的。
//将上面的 http://repo.mongodb.org 更换为 http://mirrors.aliyun.com/mongodb
echo "deb http://mirrors.aliyun.com/mongodb/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list

sudo apt-get update
sudo apt-get install -y mongodb-org
sudo service mongodb started
sudo mongo

```

#### 参考
 - [官网](https://docs.mongodb.com/manual/installation/)
 - [install-mongodb-on-ubuntu-16.04](https://www.howtoforge.com/tutorial/install-mongodb-on-ubuntu-16.04/)

#### 国外镜像安装过慢的方法
 - [Ubuntu16.04使用阿里云镜像安装Mongodb](http://www.linuxdiyf.com/linux/26151.html)

### Mongodb的python客户端开发
安装[python driver](https://docs.mongodb.com/getting-started/python/client/)
```
pip install pymongo
```
fast tutorial
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

# CRUD
# create
# 1. create a connection
client = MongoClient("mongodb://localhost:27017")
#default connect to mongodb://localhost:27017
#client = MongoClient()

# 2. access database objects, remote database object assign to local db
db = client.test
#db = client['test'] dictionary-style

# 3. access collection objects
coll = db.restaurants
#coll = db['restaurants']



# update
from datetime import datetime
'''Python
The operation returns an InsertOneResult object, 
which includes an attribute inserted_id that contains the _id of the inserted document. 
Access the inserted_id attribute:

result = coll.insert_one(
	{
		"address": {
            "street": "2 Avenue",
            "zipcode": "10075",
            "building": "1480",
            "coord": [-73.9557413, 40.7720266]
        },
        "borough": "Manhattan",
        "cuisine": "Italian",
        "grades": [
            {
                "date": datetime.strptime("2014-10-01", "%Y-%m-%d"),
                "grade": "A",
                "score": 11
            },
            {
                "date": datetime.strptime("2014-01-16", "%Y-%m-%d"),
                "grade": "B",
                "score": 17
            }
        ],
        "name": "Vella",
        "restaurant_id": "41704620"

	}
)
print(result.inserted_id)
'''

# read
# query by a top level field
cursor = db.restaurants.find({"borough": "Manhattan"})
for document in cursor:
	print(document)

# query by a field in an embedded document,use dot notation
cursor = db.restaurants.find({"address.zipcode": "10075"})
for document in cursor:
	print(document)
```