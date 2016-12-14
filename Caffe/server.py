# -*- coding: UTF-8 -*-
import BaseHTTPServer
import json
import numpy as np
import base64
import caffe_predict
#import caffe_train

#服务器端配置
HOST_NAME = 'localhost'
PORT_NUMBER = 9000

class JSONHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """处理接收到的POST请求"""
    def do_POST(self):
        response_code = 200
        response = ""
        var_len = int(self.headers.get('Content-Length'))
        content = self.rfile.read(var_len);
        payload = json.loads(content);

        # 如果是训练请求，训练然后保存训练完的神经网络
        if payload.get('train'):
            try:
                da = base64.b64decode(payload["img"])
		with open("0.jpg", 'wb') as jpg:
                    jpg.write(da)
                #caffe_train.train()
            except:
                response_code = 500
        # 如果是预测请求，返回预测值
        elif payload.get('pred'):
            try:
                da = base64.b64decode(payload["img"])
		with open("0.jpg", 'wb') as jpg:
                    jpg.write(da)
                result = caffe_predict.predict()
                response = {"type":"test", "result":result}
            except:
                response_code = 500
        else:
            response_code = 400

        self.send_response(response_code)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if response:
            self.wfile.write(json.dumps(response))
        return

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer;
    httpd = server_class((HOST_NAME, PORT_NUMBER), JSONHandler)

    try:
        #启动服务器
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    else:
        print "Unexpected server exception occurred."
    finally:
        httpd.server_close()
