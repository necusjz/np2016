# -*- coding: utf-8 -*-
"""
pandas 0.18.1
scikit-learn 0.18.1
matplotlib 1.5.3
numpy 1.11.1
"""

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import AdaBoostClassifier


def data_preprocess():
    # 数据集已合并, 去掉了标签行
    # sex预处理: 男是1, 女是0
    class_names = ['id', 'sex', 'age', 'WBC', 'RBC', 'HGB', 'HCT', 'MCV',
                   'MCH', 'MCHC', 'RDW', 'PLT', 'MPV', 'PCT', 'PDW', 'LYM',
                   'LYM%', 'MON', 'MON%', 'NEU', 'NEU%', 'EOS', 'EOS%', 'BAS',
                   'BAS%', 'ALY', 'ALY%', 'LIC', 'LIC%']
    
    data = pd.read_csv('data.csv', names=class_names)
    
    # 去掉id, 分裂标签
    selected_names = [x for x in class_names if (x != 'sex' and x != 'id' and x != 'age')]
    X_data = data[selected_names].as_matrix()
    y_data = data['sex'].as_matrix()
    
    # 按5:1分裂训练集/测试集
    X_train, X_test, y_train, y_test = \
        train_test_split(X_data, y_data, test_size=0.20)
    return X_train, X_test, y_train, y_test


def evalue(clf, X_test, y_test):
    """
    评估模型在测试集上的性能
    :param clf: 模型
    :param X_test: 测试集数据
    :param y_test: 测试集标记
    :return:
    """
    pd = clf.predict(X_test)

    correct_pairs = [(x, y) for (x, y) in zip(y_test, pd) if x == y]
    precision = float(len(correct_pairs)) / len(pd)

    print '准确率为: ' + str(precision)


def feature_select(clf, X_train, y_train, X_test):
    # 预训练
    clf.fit(X_train, y_train)
    
    # 评估特征
    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    print("特征权值分布为: ")
    for f in range(X_train.shape[1]):
        print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))
    
    # 过滤掉权值小于threshold的特征
    model = SelectFromModel(clf, threshold=0.07, prefit=True)
    X_train_new = model.transform(X_train)
    X_test_new = model.transform(X_test)
    print '训练集和测试集的容量以及选择的特征数为: ', X_train_new.shape, X_test_new.shape
    # 返回压缩特征之后的训练集和测试集
    return X_train_new, X_test_new


if __name__ == '__main__':
    # 载入数据
    X_train, X_test, y_train, y_test = data_preprocess()
    # 使用adaboost
    clf = AdaBoostClassifier()
    # 选择特征, 压缩数据
    X_train_compressed, X_test_compressed = feature_select(clf, X_train, y_train, X_test)
    
    # 使用选择的特征重新训练
    clf.fit(X_train_compressed, y_train)
    # 评估模型
    evalue(clf, X_test_compressed, y_test)
