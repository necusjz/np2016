#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from flask import Flask, request, Response, render_template, jsonify, redirect
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import bson
from cStringIO import StringIO
from PIL import Image
from imageFilter import ImageFilter
import cv2
import numpy
import json
from bson.json_util import dumps



app = Flask(__name__, static_url_path = "")
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
	c = dict(content=bson.binary.Binary(content.getvalue()),filename=secure_filename(f.name), mime=mime)
	db.files.save(c)
	return c['_id'], c['filename']


@app.route('/', methods=['GET', 'POST'])
def index():
	return redirect('/index.html')

@app.route('/upload', methods=['POST'])
def upload():
	if request.method == 'POST':
		if 'imagefile' not in request.files:
			flash('No file part')
			return jsonify({"error": "No file part"})
		imgfile = request.files['imagefile']
		if imgfile.filename == '':
			flash('No selected file')
			return jsonify({"error": "No selected file"})
		if imgfile:
			#pil = StringIO(imgfile)
			#pil = Image.open(pil)
			img = cv2.imdecode(numpy.fromstring(imgfile.read(), numpy.uint8), cv2.CV_LOAD_IMAGE_UNCHANGED)
			isqualified = ImageFilter(image=img).filter()
			if isqualified == None:
				error = 1
			else:
				error = 0
			with open('temp_pics/region.jpg') as f:
				fid, filename= save_file(f)
			print(fid)
			#report_data = ocr.ocr(path)
			#if report_data == None:
			#	return jsonify({"error": "it is not a report"})
			#print report_data
			if 0 == error:
				templates = "<div><img id=\'filtered-report\' src=\'/file/%s\' class=\'file-preview-image\' width=\'100%%\' height=\'512\'></div>"%(fid)
				data = {
					"templates": templates,
				}
			else:
				data = {
					"error": error,
				}
			return jsonify(data)
			#return render_template("result.html", filename=filename, fileid=fid)
	#return render_template("error.html", errormessage="No POST methods")
	return jsonify({"error": "No POST methods"})

'''
	根据图像oid，在mongodb中查询，并返回Binary对象
'''
@app.route('/file/<fid>')
def find_file(fid):
	try:
		file = db.files.find_one(bson.objectid.ObjectId(fid))
		if file is None:
			raise bson.errors.InvalidId()
		return Response(file['content'], mimetype='image/' + file['mime'])
	except bson.errors.InvalidId:
		flask.abort(404)

'''
	根据报告oid，抽取透视过得图像，然后进行OCR，并返回OCR结果
'''
@app.route('/report/<fid>')
def get_report(fid):

	try:
		file = db.files.find_one(bson.objectid.ObjectId(fid))
		if file is None:
			raise bson.errors.InvalidId()
		print(type(file['content']))
		
		img = cv2.imdecode(numpy.fromstring(bson.json_util.loads(dumps(file['content'])), numpy.uint8), cv2.CV_LOAD_IMAGE_UNCHANGED)
		if img is None:
			print "img is None"
			return jsonify({"error": "can't ocr'"})
		report_data = ImageFilter(image=img).ocr(22)
		#print report_data
		if report_data is None:
			print "report_data is None"
			return jsonify({"error": "can't ocr'"})
		return jsonify(report_data)
	except bson.errors.InvalidId:
		flask.abort(404)

if __name__ == '__main__':
    app.run(host=app.config['SERVER_HOST'],port=app.config['SERVER_PORT'])