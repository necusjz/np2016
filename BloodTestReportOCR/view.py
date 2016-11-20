#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from flask import Flask, request, Response, render_template
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import bson.binary
from cStringIO import StringIO
from PIL import Image



app = Flask(__name__)
# 读取配置文件
app.config.from_object('config')
# 连接数据库，并获取数据库对象
db = MongoClient(app.config['DB_HOST'], app.config['DB_PORT']).test

def save_file(f):
	content = StringIO(f.read())
	try:
		mime = Image.open(content).format.lower()
		if mime not in app.config['ALLOWED_EXTENSIONS']:
			raise IOError()
	except IOError:
		flask.abort(400)
	c = dict(content=bson.binary.Binary(content.getvalue()),filename=secure_filename(f.filename), mime=mime)
	db.files.save(c)
	return c['_id'], c['filename']


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
		if file:
			# 保存到mongodb
			fid, filename= save_file(file)
			print(fid)
			return render_template("result.html", filename=filename, fileid=fid)
	return render_template("error.html", errormessage="No POST methods")

@app.route('/file/<fid>')
def find_file(fid):
	try:
		file = db.files.find_one(bson.objectid.ObjectId(fid))
		if file is None:
			raise bson.errors.InvalidId()
		return Response(file['content'], mimetype='image/' + file['mime'])
	except bson.errors.InvalidId:
		flask.abort(404)