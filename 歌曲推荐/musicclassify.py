from sklearn.neighbors import KNeighborsClassifier
import csv
import numpy as np
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

csv_reader = csv.reader(open('./csvData_4.csv', encoding='GB2312'))
class_id_dic = {"流行":1,"轻音乐":2,"电子":3,"民谣":4,"说唱":5,"摇滚":6}
id_class_dic = {1:"流行",2:"轻音乐",3:"电子",4:"民谣",5:"说唱",6:"摇滚"}
no_feature_dic = {}
x1=[]
y1=[]
i=0
for row in csv_reader:
    if i==0:
        i+=1
        continue
    y1.append(eval(row[3]))
    featureList = row[2]
    featureList = eval(featureList)
    #no_feature_dic[featureList]=row[0]
    x1.append(featureList)
x_train = x1[:300]
x_test = x1[301:]
y_train = y1[:300]
y_test = y1[301:]
x_train = np.array(x_train)
y_train = np.array(y_train)
x_test = np.array(x_test)
y_test = np.array(y_test)
y_train = np.resize(y_train,(300,1))
#y_test = np.resize(y_test,(83,1))
#y_train.reshape(y_train.length,1)
#x_train.reshape(x_train.length,1)
knn = KNeighborsClassifier(n_neighbors=15)
knn.fit(x_train, y_train)
#X_sample = np.array([[x2, y2]])   # 设置测试点
y_sample = knn.predict(x_test)   # 获取预测类别
print(y_test)
print("----------")
print(y_sample)
count=0
for i in range(82):
    if(y_test[i]==y_sample[i]):
        count+=1
print(count)
print(round(count/82,4)*100)

clf = svm.SVC(C=2, kernel='poly', gamma=10, decision_function_shape='ovr')
clf.fit(x_train, y_train)
y_predict_svm = clf.predict(x_test)
print('SVM分类器')
# print('Testing Score: %.4f' % clf.score(X_test, y_test))
ACC = accuracy_score(y_test, y_predict_svm)
print('Testing Score: '+str(ACC))

#逻辑回归分类器
#id_class_dic = {1:"流行",2:"轻音乐",3:"电子",4:"民谣",5:"说唱",6:"摇滚"}
x_test=[[0.5780039662039099, 0.5643983662368146, 0.5199125570464195, 0.7164804191344624, 0.5448806561975921, 0.38967349459217226, 0.6307993347845731, -0.637944041332012, 0.5870421572487925, 0.90130635578319, 1.1074734128869606, 0.756401281700219, 1.3026918100135016, 1.594519776647792, -0.12053455432792126, 0.7875843226314931, -0.49058531450555476, 1.2447674946540292, 0.08582722892393571, -0.264727857389338, -1.390288709385519, -0.564113063944051, -1.066095816094858, 0.6991632341458396, 0.6300044873077577, 0.288493650939273]]
x_test = np.array(x_test)
print(x_test.shape)
y_test=[2]
lr = LogisticRegression(max_iter=10000)
lr.fit(x_train, y_train)
print(lr.predict(x_test))
#print(lr.score(x_test, y_test))