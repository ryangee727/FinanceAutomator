#!/usr/bin/env python
import os, sys
import pandas as pd
# Adds the sources directory to Python Path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.conscious_spending_plan import ConsciousSpendingPlan
from utils.bank_export_retriever import BankExportRetriever


bank_exports = BankExportRetriever('../data/').get_bank_exports()
merged = pd.concat(bank_exports, ignore_index=True)

csp = ConsciousSpendingPlan()
csp.add_next_months_worksheet()
csp.import_df(merged)
# print(csp.export_df())


# from sklearn.datasets import load_iris
# from sklearn.linear_model import LogisticRegression
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn import metrics
# from sklearn.model_selection import train_test_split
#
# iris = load_iris()
#
# X = iris.data
# y = iris.target
#
# print(X)
# print(y)
#
# logreg = LogisticRegression()
# logreg.fit(X,y)
#
# y_predict = logreg.predict(X)
# print(len(y_predict))
#
# test = metrics.accuracy_score(y, y_predict)
# print(test)
#
# knn = KNeighborsClassifier(n_neighbors=5)
# knn.fit(X,y)
# y_predict = knn.predict(X)
# test = metrics.accuracy_score(y, y_predict)
# print(test)
#
# knn = KNeighborsClassifier(n_neighbors=8)
# knn.fit(X,y)
# y_predict = knn.predict(X)
# test = metrics.accuracy_score(y, y_predict)
# print(test)
#
#
# #Train Test Split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=4)
#
# print(X_train.shape)
# print(X_test.shape)
#
# logreg = LogisticRegression()
# logreg.fit(X_train, y_train)
# y_predict = logreg.predict(X_test)
# print(metrics.accuracy_score(y_test, y_predict))
#
# scores = []
# for n in range(1,26):
#     knn = KNeighborsClassifier(n_neighbors=n)
#     knn.fit(X_train, y_train)
#     y_predict = knn.predict(X_test)
#     scores.append(metrics.accuracy_score(y_test, y_predict))
#
# print(scores)