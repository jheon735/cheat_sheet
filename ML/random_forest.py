import numpy as np
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import joblib
from collections import OrderedDict
from sklearn.model_selection import train_test_split

def make_model(train_data, test_data):
    """
    모델 생성 함수
    :param train_data: split_save 함수에서 생성된 형태의 학습자료
    :param test_data: split_save 함수에서 생성된 형태의 학습자료
    :return:
    """
    testdata_pd = pd.DataFrame(test_data, columns=["A", "B", "C"])
    traindata_pd = pd.DataFrame(train_data, columns=["A", "B", "C"])

    # 학습시키려는 변수
    use_list = ["A", "B", "C"]

    # 학습 및 검증 자료 입력
    trdata_pd = traindata_pd[use_list]
    trdata_pd = trdata_pd.dropna()
    trdata_pd = trdata_pd[trdata_pd.Type != -99.]

    ttdata_pd = testdata_pd[use_list]
    ttdata_pd = ttdata_pd.dropna()
    ttdata_pd = ttdata_pd[ttdata_pd.Type != -99.]

    feature_columns = list(trdata_pd.columns.difference(['Type']))

    train_x = trdata_pd[feature_columns]
    train_y = trdata_pd['Type']
    test_x = ttdata_pd[feature_columns]
    test_y = ttdata_pd['Type']

    # 모델 학습
    clf = RandomForestClassifier(n_estimators=estimator_num, max_depth=m_depth, random_state=ran_state, max_features=mfeat) #random forest의 주요 변경 파라미터
    clf.fit(train_x, train_y)
    predict1 = clf.predict(test_x)
    # 모델 저장
    joblib.dump(clf, "model output filename")

    # 모델 결과 저장
    if report_opt:      #결과 저장 여부
        if not os.path.isdir(os.path.dirname(report_fname)):
            os.mkdir(os.path.dirname(report_fname))
        with open(report_fname, 'w') as f:
            cfm = confusion_matrix(test_y, predict1)
            print(cfm, file = f)
            f.write('\n')
            print(classification_report(test_y, predict1, digits=4), file = f)


def rf_test():
    data = pd.DataFrame(test_data, columns=["A", "B", "C"])
    X = data["A"]
    Y = data["B"]
    train_x, test_x, train_y, test_y = train_test_split(X, Y, test_size=0.4, random_state=1412)
    print(train_x.shape, test_x.shape, train_y.shape, test_y.shape)

    clf = RandomForestClassifier(n_estimators=20, max_depth=5, random_state=0)
    clf.fit(train_x, train_y)

    predict1 = clf.predict(test_x)
    print(test_y.value_counts())
    print(accuracy_score(test_y, predict1))
    print(confusion_matrix(test_y, predict1))


if __name__=='__main__':
    train = np.loadtxt('train_data.txt')
    test = np.loadtxt('test_data.txt')
    make_model(train, test)
