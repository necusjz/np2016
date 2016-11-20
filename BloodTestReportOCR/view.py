#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename



app = Flask(__name__)
# 读取配置文件
app.config.from_object('config')

filenames = []

def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']




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
			
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			filenames.append(filename)
			return render_template("result.html", filenames=filenames)
	return render_template("error.html", errormessage="No POST methods")

