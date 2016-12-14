var ocrDemo = {
    CANVAS_WIDTH: 200,
    TRANSLATED_WIDTH: 20,
    PIXEL_WIDTH: 10, // TRANSLATED_WIDTH = CANVAS_WIDTH / PIXEL_WIDTH

    // 服务器端参数
    PORT: "9000",
    HOST: "http://localhost",

    // 颜色变量
    BLACK: "#000000",

    onLoadFunction: function() {
        this.resetCanvas();
    },

    resetCanvas: function() {
        var canvas = document.getElementById('canvas');
        var ctx = canvas.getContext('2d');

        ctx.fillStyle = this.BLACK;
        ctx.fillRect(0, 0, this.CANVAS_WIDTH, this.CANVAS_WIDTH);
        var matrixSize = 400;
        

        // 绑定事件操作
        canvas.onmousemove = function(e) { this.onMouseMove(e, ctx, canvas) }.bind(this);
        canvas.onmousedown = function(e) { this.onMouseDown(e, ctx, canvas) }.bind(this);
        canvas.onmouseup = function(e) { this.onMouseUp(e, ctx) }.bind(this);
    },

    onMouseMove: function(e, ctx, canvas) {
        if (!canvas.isDrawing) {
            return;
        }
        this.fillSquare(ctx, e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
    },

    onMouseDown: function(e, ctx, canvas) {
        canvas.isDrawing = true;
        this.fillSquare(ctx, e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
    },

    onMouseUp: function(e) {
        canvas.isDrawing = false;
    },

    fillSquare: function(ctx, x, y) {
        var xPixel = Math.floor(x / this.PIXEL_WIDTH);
        var yPixel = Math.floor(y / this.PIXEL_WIDTH);

        ctx.fillStyle = '#ffffff';
        ctx.fillRect(xPixel * this.PIXEL_WIDTH, yPixel * this.PIXEL_WIDTH, this.PIXEL_WIDTH, this.PIXEL_WIDTH);
    },

    train: function() {
        var digitVal = document.getElementById("digit").value;
        if (!digitVal) {
            alert("Please type and draw a digit value in order to train the network");
            return;
        }
        var mycanvas = document.getElementById('canvas');
        // canvas.toDataURL 返回的是一串Base64编码的URL，当然,浏览器自己肯定支持 
        var img_data = mycanvas.toDataURL("image/jpg");
        //删除字符串前的提示信息 "data:image/jpg;base64,"
        var b64 = img_data.substring(22);

        // 将客服端训练数据集发送给服务器端
        alert("Sending training data to server...");
        var json = {
            img: b64,
            train: true
        };
        this.sendData(json);
    },

    // 发送预测请求
    test: function() {
        var mycanvas = document.getElementById('canvas') 
        // canvas.toDataURL 返回的是一串Base64编码的URL，当然,浏览器自己肯定支持 
        var img_data = mycanvas.toDataURL("image/jpg");
        //删除字符串前的提示信息 "data:image/jpg;base64,"
        var b64 = img_data.substring(22);
        var json = {
            img: b64,
            pred: true
        };
        this.sendData(json);
    },

    // 处理服务器响应
    receiveResponse: function(xmlHttp) {
        if (xmlHttp.status != 200) {
            alert("Server returned status " + xmlHttp.status);
            return;
        }
        var responseJSON = JSON.parse(xmlHttp.responseText);
        if (xmlHttp.responseText && responseJSON.type == "test") {
            alert("The neural network predicts you wrote a \'" + responseJSON.result + '\'');
        }
    },

    onError: function(e) {
        alert("Error occurred while connecting to server: " + e.target.statusText);
    },

    sendData: function(json) {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open('POST', this.HOST + ":" + this.PORT, false);
        xmlHttp.onload = function() { this.receiveResponse(xmlHttp); }.bind(this);
        xmlHttp.onerror = function() { this.onError(xmlHttp) }.bind(this);
        var msg = JSON.stringify(json);
        xmlHttp.setRequestHeader('Content-length', msg.length);
        xmlHttp.setRequestHeader("Connection", "close");
        xmlHttp.send(msg);
    }
}
