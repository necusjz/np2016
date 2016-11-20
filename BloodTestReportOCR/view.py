#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import bson.binary
from cStringIO import StringIO



app = Flask(__name__)
# 读取配置文件
app.config.from_object('config')
# 连接数据库，并获取数据库对象
db = MongoClient(app.config['DB_HOST'], app.config['DB_PORT']).test
filenames = []

def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def save_file(f):
	content = StringIO(f.read())
	c = dict(content=bson.binary.Binary(content.getvalue()))
	db.files.save(c)
	return c['_id']


@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template("upload.html")

@app.route('/upload', methods=['POST'])
def upload():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return render_template("error.html", errormessage="No file part")
		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return render_template("error.html", errormessage="No selected file")
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			#print(filename)
			# 保存到mongodb
			fid = save_file(file)
			print(fid)
			filenames.append(filename)
			return render_template("result.html", filenames=filenames)
	return render_template("error.html", errormessage="No POST methods")

