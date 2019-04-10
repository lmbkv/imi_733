# model_selection.py
from sklearn.metrics import accuracy_score

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression, RidgeClassifier, SGDClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from yellowbrick.pipeline import VisualPipeline
from yellowbrick.features.importances import FeatureImportances

from sklearn.externals import joblib
from yellowbrick.classifier import ClassificationReport

import matplotlib.pyplot as plt

def modelSelection():
	data_path = "labeled_data.csv"
	data = pd.read_csv(data_path)

	# Preprocessing pipelines for both numeric and categorical data.
	numeric_features = ['count_reviews', 'rating']
	numeric_transformer = Pipeline(steps=[
	    ('imputer', SimpleImputer(strategy='median')),
	    ('scaler', StandardScaler())])

	categorical_features = ['product_category']
	categorical_transformer = Pipeline(steps=[
	    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
	    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

	preprocessor = ColumnTransformer(
	    transformers=[
	        ('num', numeric_transformer, numeric_features),
	        ('cat', categorical_transformer, categorical_features)])

	X = data.drop('label', axis=1)
	y = data['label']
	fig = plt.figure()
	ax = fig.add_subplot()

	#viz_ridge = ClassificationReport(RidgeClassifier(), classes = ['not recommended', 'recommended'], support=True)
	viz_logistic = ClassificationReport(
										LogisticRegression(), 
										#SGDClassifier(),
										#RidgeClassifier(),
										classes = ['not recommended', 'recommended'], 
										support=True)

	#clf_ridge = VisualPipeline(steps=[('preprocessor', preprocessor),
	#                      #('classifier', LogisticRegression(solver='lbfgs')),
	#                      ('viz', viz_ridge)])

	#Visual Pipeline is used to visualize the report
	clf_logistic = VisualPipeline(steps=[('preprocessor', preprocessor),
	                      #('classifier', LogisticRegression(solver='lbfgs')),
	                      ('viz', viz_logistic)])

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

	#model_ridge = clf_ridge.fit(X_train, y_train)
	model_logistic = clf_logistic.fit(X_train, y_train)

	#preds_ridge = clf_ridge.predict(X_test)
	preds_logistic = clf_logistic.predict(X_test)

	#print("RidgeClassifier model score: %.3f" % clf_ridge.score(X_test, y_test))
	print("LogisticRegression model score: %.3f" % clf_logistic.score(X_test, y_test))
	#clf_ridge.poof()
	clf_logistic.poof()

	# Evaluate accuracy
	#print("RidgeClassifier accuracy: ", accuracy_score(y_test, preds_ridge))
	print("LogisticRegression accuracy: ", accuracy_score(y_test, preds_logistic))

	final_predictions = X_test
	final_predictions['target'] = y_test
	final_predictions['prediction'] = preds_logistic

	#print(final_predictions)

	filename = 'model_products.sav'
	joblib.dump(model_logistic, filename)

if __name__ == "__main__":
	modelSelection()