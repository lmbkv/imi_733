#discrimination_threshold_select.py
from sklearn.metrics import accuracy_score
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression, RidgeClassifier, SGDClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from yellowbrick.pipeline import VisualPipeline

from yellowbrick.classifier import DiscriminationThreshold

from sklearn.externals import joblib


def selectDiscr():
	data_path = "labeled_data.csv"
	data = pd.read_csv(data_path)

	# We create the preprocessing pipelines for both numeric and categorical data.
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

	viz = DiscriminationThreshold(LogisticRegression())

	clf = VisualPipeline(steps=[('preprocessor', preprocessor),
	                      #('classifier', LogisticRegression(solver='lbfgs')),
	                      ('viz', viz)])

	X = data.drop('label', axis=1)
	y = data['label']

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

	model = clf.fit(X_train, y_train)
	model.poof()


if __name__ == "__main__":
	selectDiscr()