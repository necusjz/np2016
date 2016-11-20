# 血常规检验报告OCR

## 实现图片文件上传到服务器的功能

### Requirements
 - python 2.7
 - Flask

&emsp;&emsp;安装[Flask](http://flask.pocoo.org/docs/0.11/quickstart/)
```
pip install Flask
```

### Deploy
```
export FLASK_APP=view.py
//optional
export FLASK_DEBUG=1 

flask run
// or python -m flask run

```
&emsp;&emsp;访问localhost:5000

## 实现图片上传到服务器并写入mongodb
### Requirements
 - python 2.7
 - Flask
 - mongoDB
 - pymongo

&emsp;&emsp;安装[mongoDB](https://docs.mongodb.com/manual/installation/)

#### 参考
 - [官网](https://docs.mongodb.com/manual/installation/)
 - [install-mongodb-on-ubuntu-16.04](https://www.howtoforge.com/tutorial/install-mongodb-on-ubuntu-16.04/)

#### 国外镜像安装过慢的方法
 - [Ubuntu16.04使用阿里云镜像安装Mongodb](http://www.linuxdiyf.com/linux/26151.html)

#### python客户端开发
&emsp;&emsp;安装[python driver](https://docs.mongodb.com/getting-started/python/client/)
```
pip install pymongo
```