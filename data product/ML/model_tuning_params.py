#model_tuning_params.py
#The following code was partially adapted from the blog of Shreyas Jothish (https://github.com/ShreyasJothish)

from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV

from sklearn.feature_selection import SelectKBest, f_classif

from sklearn.externals import joblib

def tuneParams():
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

	# Append classifier to preprocessing pipeline.
	clf = make_pipeline(\
                         preprocessor,
                         SelectKBest(f_classif),
                         LogisticRegression(
                         	))

	X = data.drop('label', axis=1)
	y = data['label']

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

	param_grid = {
	    'logisticregression__C': [.0001, .001, .01, .1, 1.0, 10.0, 100.00, 1000.0, 10000.0], 
	    'logisticregression__penalty': ['l1', 'l2'],
		'logisticregression__max_iter': [10, 50, 100],
	}

	gridsearch = GridSearchCV(clf, param_grid=param_grid, cv=5,
	                         scoring='accuracy', verbose=1)

	gridsearch.fit(X_train, y_train)

	# Best cross validation score
	print('Cross Validation Score:', gridsearch.best_score_)

	# Best parameters which resulted in the best score
	print('Best Parameters:', gridsearch.best_params_)


	#Get the best model and check it against test data set.
	# Predict with X_test features
	y_pred = gridsearch.predict(X_test)

	# Compare predictions to y_test labels
	test_score = accuracy_score(y_test, y_pred)
	print('Accuracy Score on test data set:', test_score)

if __name__ == "__main__":
	tuneParams()