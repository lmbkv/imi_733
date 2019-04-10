# er_categories.py
# The following code was partially adapated from Assignment #2

import re
import operator
from pyspark.sql import SparkSession
from pyspark.sql import SparkSession, functions, types
import pandas as pd

from pyspark import SparkConf, SparkContext
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import udf, lit
import operator
spark = SparkSession.builder.appName('param').getOrCreate()
sc = spark.sparkContext
import sys
from pyspark.sql.functions import explode, split, concat
import os
import csv

class EntityResolution:
	def __init__(self, dataFile1, dataFile2):
		self.df1 = dataFile1
		self.df2 = dataFile2

	def preprocessDF(self, df, cols): 
		#split categories by comma, get rid of other characters
		def split_string(cat):
			line = re.sub('[\&]', '', cat)
			line = list(map(str, line.split(", ")))
			line = list(filter(None, line))
			return line

		df['tokens'] = df['category'].apply(split_string)
		print(type(df))
		return(df)

	def preprocessCats(self, df, cols): 
		#split categories from Amazon Reviews Dataset
		def split_string(cat):
			line = list(map(str, cat.split()))
			line = list(filter(None, line))
			return line
		df['product_category'] = df['product_category'].apply(split_string)
		return(df)

	def filtering(self, df1, df2):
		#filter out unmatching pairs
		df1['review_title'] = df1['review_title'].astype(str)

		reviews_schema = types.StructType([
			types.StructField('review_title', types.StringType()),
			types.StructField('rating', types.FloatType()),
			types.StructField('ind', types.StringType()),
			types.StructField('asin', types.StringType()),
			types.StructField('category', types.StringType()),
			types.StructField('tokens', types.ArrayType(types.StringType())),
	])
		df1 = spark.createDataFrame(df1, schema = reviews_schema)
		df2 = spark.createDataFrame(df2)

		df1.createOrReplaceTempView('df1')
		df2.createOrReplaceTempView('df2')

		#flatten out lists of categories
		df1_flat = df1.select(df1['asin'], functions.explode(df1['tokens']).alias('tokens')) 	
		df2_flat = df2.select(df2['id'], functions.explode(df2['product_category']).alias('product_category'))

		df1_flat.createOrReplaceTempView('df1_flat')
		df2_flat.createOrReplaceTempView('df2_flat')

		#combine categories from products list with categories from amazon reviews dataset
		df_pairs = spark.sql(
		"""SELECT df1_flat.asin as asin, df1_flat.tokens as tokens, df2_flat.id as id, df2_flat.product_category as product_category
			FROM df1_flat, df2_flat
			WHERE df1_flat.tokens = df2_flat.product_category AND df1_flat.tokens != "" AND df2_flat.product_category != "" 
		"""
			)

		df_pairs.createOrReplaceTempView('df_pairs')

		candDF = spark.sql(
		"""SELECT df1.asin as asin, df1.tokens as tokens, df2.id as id, df2.product_category as product_category
			FROM df1
			INNER JOIN df_pairs pairs ON df1.asin = pairs.asin
			INNER JOIN df2 ON pairs.id = df2.id
		"""
			)

		candDF = candDF.dropDuplicates()
		return(candDF)

	def verification(self, candDF, threshold):
		#calculate the similarity
		def jaccCalculate(jk1, jk2):
			inter = len(set.intersection(*[set(jk1), set(jk2)]))
			uni = len(set.union(*[set(jk1), set(jk2)]))
			return inter/float(uni)
		inter_func = functions.udf(jaccCalculate, types.FloatType())
		candDF = candDF.withColumn("intersect", inter_func(candDF["tokens"], candDF["product_category"]))
		candDF.show()
		resultDF = candDF.filter(candDF["intersect"] >= threshold)
		return resultDF

	def jaccardJoin(self, threshold):
		newDF1 = self.preprocessDF(self.df1) 
		newDF2 = self.preprocessCats(self.df2) 		
		candDF = self.filtering(newDF1, newDF2)
		resultDF = self.verification(candDF, threshold)
		return resultDF

if __name__ == "__main__":

	spark = SparkSession.builder.appName('entity resolution').getOrCreate()
	assert spark.version >= '2.3' # make sure we have Spark 2.3+
	spark.sparkContext.setLogLevel('WARN')
	sc = spark.sparkContext

	#read all scraped products
	path = '/scraped/'
	fn =  (x for x in os.listdir(path) if '.~' not in x)

	df_prods = pd.DataFrame()

	for filename in fn:
		full_path = path+filename		
		dt = pd.read_csv(full_path)
		frames = [df_prods, dt]
		df_prods = pd.concat(frames)
		#print(filename)
	#group reviews by product IDs and categories, get number of reviews and average raiting
	reviews = df_prods.groupby(['asin', 'category']).agg({'review_title': 'count', 'rating': 'mean'}) #.unstack(fill_value=0).reset_index().rename_axis(None, axis=1)
	
	reviews['ind'] = reviews.index
	reviews['asin'], reviews['category'] = zip(*reviews.ind)
	product_list = reviews.reset_index(drop=True)

	er = EntityResolution(product_list, categories_data)
	resultDF = er.jaccardJoin(0.001)

	resultDF = resultDF.sort(col("asin").desc())
	resultDF.createOrReplaceTempView('resultDF')

	#get products' categories with only highest similarity
	categories_for_asins = spark.sql(
	"""SELECT a.asin, a.intersect, a.id, a.product_category
		FROM resultDF a
		INNER JOIN (
			SELECT asin, MAX(intersect) inter
			FROM resultDF
			GROUP BY asin
		) b ON a.asin = b.asin AND a.intersect = b.inter
	"""
		)

	categories_for_asins = categories_for_asins.toPandas()
	products_with_cats = product_list.merge(categories_for_asins, on='asin')
	#print(products_with_cats.dtypes)
	products_with_cats = products_with_cats.rename(columns={'review_title':'count_reviews'})
	products_with_cats = products_with_cats[['asin', 'product_category', 'count_reviews', 'rating']]

	products_with_cats.to_csv("products_with_categories.csv")