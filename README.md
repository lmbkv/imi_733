# imi_733
Internet Media Influence

The code for the project is divided into four parts. Namely, Data Collection and Cleaning, Data Integration, Data Analysis and Data Product.

The task of acquiring the data consisted of mainly scraping different websites. So, the folder Data Collection has a subfolder called Scrapers which has all the scrapers which were used to scrape data from Buzzfeed, Amazon, BestProducts and so on.

# Data Collection
main_buzzfeed_shopping.py - is used to scrape the shopping section of the buzzfeed website and create a csv file with Articles and their links

individual_link_creation.py - reads the csv file created by the main_buzzfeed_shopping.py and creates a file for each article containing its html content

individual_link_scraping.py - for each article, reads the html file created by individual_link_creation.py and then outputs a csv file with article data, product name, product description and product link.

amazon_reviews_scraper.py - was used to scrape reviews of products that were not present in the amazon comments dataset. 

amzbs4.py - is a file that has various functions that are invoked in amazon_reviews_scraper.py

bp_art_link_scraper.py - is used to scrape the article links from BestProducts.com website and create a csv file.

bp_art_scraper.py - is used to scrape the product name, date of article, product description and corresponding amazon link of the product from the articles on BestProducts.com 

# Data Integration

er_cateogries.py - Used to find the global categories for each product. We take data that was scraped and categories from amazon dataset and perform entity resolution and output products and corresponding global categories.

er_categories.py - the input to this script was products, categories and corresponding percentage change. Entity resolution was performed to determine the influence percentage change for each category.


# Data Analysis

combined_graph.py - was used to find the combined influence of multiple articles on the review counts of the products

mutiple_line_graphs.py - was used to find the the influcence of multiple articles on the same graph with each line depicting the review count of for the corresponding article.

contingency.py - was used to create a contingeny table to find the correlation between the release date of the article and the number of reviews received before and after that.

nlp_vis.py - was used to visualize the frequencies of the words used in the reviews of various products

percentage_change.py - was used to find the percentage increase in the number of reviews before and after the release of an article

# Data Product 

Has two sub-folders : ML and Article generator - nlp

# ML 

data_preparation_for_training.py - here the data is prepared for training by labeling and combining datasets

baseline_acc.py - the script calculates baseline accuracy that is used as a reference for further optimization

model_selection.py - selecting a best performing model

make_predictions.py - making predictions on newly obtained data with the optimized model

discrimination_threshold_select.py - visualizing the discrimination threshold for binary classification

model_tuning_params.py - script for hyper-parameters tuning

# Article generator - nlp

article_gen.py - reads the predicted data, combines all of them into one file, for all the products that were predicted, the corresponding reviews were scraped and put into an intermediate file.

html_gen.py - reads the intermediate file and makes a an article with auto generated product titles and descriptions

amazon_sec.py & amazon_orig.py - used to scrape data about the products 


