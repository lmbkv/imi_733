# make_predictions.py
# make predictions about products
from sklearn.linear_model import LogisticRegression

import numpy as np
import pandas as pd

from sklearn.externals import joblib

def makePredictions():
	#load the model
	filename = 'model_products.sav'

	loaded_model = joblib.load(filename)

	file = "products_for_prediction.csv"
	Xnew = pd.read_csv(file)

	# define one new instance
	#Xnew = [[-0.79415228, 2.10495117]]
	# make a prediction
	ynew = loaded_model.predict(Xnew)
	ynew_prob = loaded_model.predict_proba(Xnew)
	#print("X=%s, Predicted=%s" % (Xnew[0], ynew[0]))
	Xnew['predict'] = ynew
	Xnew['not_featured_prob'] = ynew_prob[:,0]
	Xnew['featured_prob'] = ynew_prob[:,1]
	Xnew.to_csv("predictions.csv")

	print(Xnew)
	#print(ynew_prob)


if __name__ == "__main__":
	makePredictions()
