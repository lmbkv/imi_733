# data_preparation_for_training.py
import re
import operator
import pandas as pd

from pyathenajdbc import connect

import pandas as pd

def processCategories(line): #split categories to list
		line = list(map(str, line.split("_")))
		line = list(filter(None, line))
		return line


if __name__ == "__main__":
	conn = connect(access_key=ACCESS_KEY,
	               secret_key=AWS_SECRET_ACCESS_KEY,
	               s3_staging_dir='s3://athena-bucket-reviews',
	               region_name='us-east-2',
	               )

	df_false = pd.read_sql("""
		SELECT product_id as asin, product_category, count(review_headline) as count_reviews, avg(star_rating) as rating 
		FROM amazon_reviews_parquet 
		GROUP BY product_id, product_category 
		ORDER BY RANDOM() LIMIT 5000;""", conn)
	df_false['product_category'] = df_false['product_category'].apply(processCategories)

	data_true = "/reviews/products.csv"
	data_true = pd.read_csv(data_true, engine='python')

	data_true['label'] = 1
	data_false['label'] = 0

	data_combined = data_true.append(data_false, ignore_index=False)
	data_combined = data_combined[['asin', 'product_category', 'count_reviews', 'rating', 'label']]

	data_combined.to_csv('labeled_data.csv')
