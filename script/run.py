#!/usr/bin/env python
import os, sys
import pandas as pd
import argparse

# Adds the sources directory to Python Path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.conscious_spending_plan import ConsciousSpendingPlan
from utils.a_r_expenses import ARExpenses
from utils.bank_export_retriever import BankExportRetriever


parser = argparse.ArgumentParser(description='A CSV to Google Doc ETL that automates Monthly Finance Workflow.')
parser.add_argument('--step2', dest='step2', action='store_true',
                    help='Activates Step 2 of Workflow (After Manually Entering Shared Expenses)')
parser.add_argument('--skip_next_month', dest='skip_next_month', action='store_true',
                    help='Do not add a new worksheet for the next month.')
args = parser.parse_args()

csp = ConsciousSpendingPlan()
if not args.step2:
    print("Starting Step 1...")
    bank_exports = BankExportRetriever('../data/').get_bank_exports()
    merged = pd.concat(bank_exports, ignore_index=True)
    if not args.skip_next_month:
        csp.add_next_months_worksheet()
    csp.import_df(merged)
elif args.step2:
    print("Starting Step 2...")
    csp.update_worksheet_with_split_shared()
    ARExpenses = ARExpenses()
    ARExpenses.import_df(csp.export_shared_only_df())
    ARExpenses.add_next_months_worksheet()
print("Finished!")


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