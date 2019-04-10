
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def baseline():
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

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

	#Getting baseline accuracy
	majority_class = y_train.mode()[0]
	prediction = np.full(shape=y_train.shape, 
	                     fill_value=majority_class)

	print(accuracy_score(y_train, prediction))

	#Calculated baseline accuracy - 0.6058648111332008

if __name__ == "__main__":
	baseline()