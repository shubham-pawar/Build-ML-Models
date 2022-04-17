from sklearn import datasets
from sklearn import tree
from sklearn import metrics
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier

#fetch dataset from OPENML
banknote = datasets.fetch_openml(data_id=1462)

#print Feature Names, Data and Target
print("Feature Names\n " ,banknote.feature_names)
print("Data\n ",banknote.data)
print("Target\n ",banknote.target)

#Decision tree with default parameters

mytree = tree.DecisionTreeClassifier(criterion="entropy")

#Training
mytree.fit(banknote.data,banknote.target)  

#Print learned Tree:
#print(tree.export_text(mytree))

#Making Predictions
predictions = mytree.predict(banknote.data)

print("\n",predictions)

metrics.accuracy_score(banknote.target, predictions)

#Evaluation
print("Evaluation for Category 1\n")
print("f1_score ", metrics.f1_score(banknote.target, predictions, pos_label="1"))
print("precision_score ", metrics.precision_score(banknote.target, predictions, pos_label="1"))
print("recall_score ", metrics.recall_score(banknote.target, predictions, pos_label="1"))
print("\n")
print("Evaluation for Category 2\n")
print("f1_score ", metrics.f1_score(banknote.target, predictions, pos_label="2"))
print("precision_score ", metrics.precision_score(banknote.target, predictions, pos_label="2"))
print("recall_score ", metrics.recall_score(banknote.target, predictions, pos_label="2"))
print("\n")

#Using Cross-Validation

dtc = tree.DecisionTreeClassifier(criterion="entropy")
cv = model_selection.cross_validate(dtc, banknote.data, banknote.target, scoring="roc_auc", cv=10)
print("Mean Test score for default Decision Tree ", cv["test_score"].mean())
print("\n")
cv = model_selection.cross_validate(dtc, banknote.data, banknote.target, scoring=["accuracy","roc_auc"], cv=10)
print("\n The mean test roc_auc for Decision tree with default parameters ",cv["test_roc_auc"].mean())


#Decision tree with tuned min_samples_leaf using GridSearchCV 
a = tree.DecisionTreeClassifier(min_samples_leaf=10)
#help(tree.DecisionTreeClassifier)
parameters=[{"min_samples_leaf":[2,4,6,8,10]}]
print("\n")

#GridSearchCV
dtc = tree.DecisionTreeClassifier(criterion="entropy")
tuned_dtc = model_selection.GridSearchCV(dtc, parameters, scoring="roc_auc", cv=10)
cv = model_selection.cross_validate(tuned_dtc, banknote.data, banknote.target, scoring="roc_auc", cv=10, return_train_score=True)
print("The new improved score is ", cv["test_score"].mean())

tuned_dtc.fit(banknote.data, banknote.target)
print("\n")
print("Best parameter-> ", tuned_dtc.best_params_)
print("\n")
cv = model_selection.cross_validate(tuned_dtc, banknote.data, banknote.target, scoring=["accuracy", "roc_auc"], cv=10, return_train_score=True)
print("\n The mean test roc_auc for Decision tree with tuned min_samples_leaf using GridSearchCV", cv["test_roc_auc"].mean())

#Random Forest
rf = RandomForestClassifier()
rf.fit(banknote.data,banknote.target)
cv_rf = model_selection.cross_validate(rf, banknote.data, banknote.target, scoring="roc_auc", cv=10)
cv = model_selection.cross_validate(rf, banknote.data, banknote.target, scoring=["accuracy","roc_auc"], cv=10)
print("\n The mean test roc_auc for Random Forest is shown below: ")
print(cv["test_roc_auc"].mean())

#Bagged decision tree
bagged_dtc = BaggingClassifier()
bagged_dtc.fit(banknote.data, banknote.target)
cv_bagged_dtc = model_selection.cross_validate(bagged_dtc, banknote.data, banknote.target, scoring="roc_auc", cv=10)
cv = model_selection.cross_validate(bagged_dtc, banknote.data, banknote.target, scoring=["accuracy","roc_auc"], cv=10)
print("\n The mean test roc_auc for Bagging is shown below: ")
print(cv["test_roc_auc"].mean())

#AdaBoosted decision tree
ada_dtc = AdaBoostClassifier()
ada_dtc.fit(banknote.data, banknote.target)
cv_ada_dtc = model_selection.cross_validate(ada_dtc, banknote.data, banknote.target, scoring="roc_auc", cv=10)
cv = model_selection.cross_validate(ada_dtc, banknote.data, banknote.target, scoring=["accuracy","roc_auc"], cv=10)
print("\n The mean test roc_auc for Adaboosted tree is shown below: ")
print(cv["test_roc_auc"].mean())
