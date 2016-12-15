# -*- coding: utf-8 -*-
"""
scikit-learn 0.18.1
matplotlib 1.5.3
numpy 1.11.1
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import  GradientBoostingRegressor


def draw(labels, prediction):
    """
    绘制折线图比较结果
    :param labels: 1维numpy数组
    :param prediction: 1维numpy数组
    :return:
    """
    result = []
    for i in range(labels.shape[0]):
        result.append([labels[i], prediction[i]])

    # 将年龄按照大小排序
    result = sorted(result, key=lambda x: x[0])
    labels = [row[0] for row in result]
    prediction = [row[1] for row in result]

    plt.plot(labels, label='labels')
    plt.plot(prediction, label='predict')
    plt.legend(loc='upper left')
    plt.show()


# 评估测试集
def evalue(clf, X_test, y_test):
    pd = clf.predict(X_test)
    
    delta = [x1 - x2 for (x1, x2) in zip(y_test, pd)]
    correct_indices = [x for x in delta if abs(x) < 10]
    precision = float(len(correct_indices)) / len(pd)
    
    print 'Precision is: ' + str(precision)
    score = clf.score(X_test, y_test)
    print 'Coefficient R^2 is: ' + str(score)
    draw(y_test, pd)


# 数据集已合并, 去掉了标签行
# sex预处理: 男是1, 女是0
class_names = ['id','sex','age','WBC','RBC','HGB','HCT','MCV',
              'MCH','MCHC','RDW','PLT','MPV','PCT','PDW','LYM',
              'LYM%','MON','MON%','NEU','NEU%','EOS','EOS%','BAS',
              'BAS%','ALY','ALY%','LIC','LIC%']

data = pd.read_csv('data.csv', names=class_names)

# 去掉有缺失维度的数据
data = data.replace(to_replace='?', value=np.nan)
data = data.dropna(how='any')

# 去掉id, 分裂标签
selected_names = [x for x in class_names if (x != 'age' and x != 'id' and x != 'sex')]
X_data = data[selected_names].as_matrix()
y_data = data['age'].as_matrix()

# 按4:1分裂训练集/测试集
X_train, X_test, y_train, y_test = \
    train_test_split(X_data, y_data, test_size=0.20, random_state=0)

# 数据标准化
ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)

# 随机森林
clf = RandomForestRegressor(max_features=None, n_estimators=20, max_depth=None)
clf.fit(X_train, y_train)

# 评估特征
importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]
print("Feature ranking:")

for f in range(X_train.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

model = SelectFromModel(clf, threshold=0.10, prefit=True)
X_train_new = model.transform(X_train)
X_test_new = model.transform(X_test)
print X_train_new.shape, X_test_new.shape

# 使用提取的特征重新训练
clf.fit(X_train_new, y_train)
# 评估训练集效果
print '评估训练集效果'
evalue(clf, X_train_new, y_train)
# 评估测试集效果
print '评估测试集效果'
evalue(clf, X_test_new, y_test)
