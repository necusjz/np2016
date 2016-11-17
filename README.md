# 对血常规检验报告的OCR识别、深度学习与分析

* 将血常规检验报告的图片识别出年龄、性别及血常规检验的各项数据
    * 图片上传页面，提交的结果是图片存储到了mongodb数据库得到一个OID
    * 图片识别得到一个json数据存储到了mongodb数据库得到一个OID，json数据如https://coding.net/u/mengning/p/np2016/git/blob/master/BloodTestReportOCR/bloodtestdata.json
           * 自动截取目标区域
           * 预处理，比如增加对比度、锐化
           * 识别
    * 识别结果页面，上部是原始图片，下部是一个显示识别数据的表格，以便对照识别结果
* 学习血常规检验的各项数据及对应的年龄性别
* 根据血常规检验的各项数据预测年龄和性别

## Links

* 2016年秋-网络程序设计http://teamtrac.ustcsz.edu.cn/wiki/NP2016
* 一些有趣的深度学习项目https://coding.net/u/mengning/p/np2016/topic/209943