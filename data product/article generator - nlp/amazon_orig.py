# # The following code was partially adapated from Abe Flansburg (https://github.com/aflansburg)



from amazon_sec import read_reviews, get_date
from amazon_sec import is_valid_file
import argparse
import os
import csv
import io
from datetime import datetime


read_path = "/home/aroun/Documents/Sem2/Project/Final/Buzzfeed/ID_DATES_Folder/"

write_path = "/home/aroun/Documents/Sem2/Project/Final/Buzzfeed/Buzzfeed_Reviews_Folder/"



for filename in os.listdir(read_path):

    inputFile = read_path+filename

    print(inputFile)

    # check for current os
    if os.name == 'posix':
        # osx
        driver_path = '/home/aroun/Documents/chromedriver'
        # driver_path = '/home/aalymbek/Desktop/chrome/chromedriver'
    elif os.name == 'nt':
        # win32
        driver_path = 'C:\chromedriver\chromedriver'
    else:
        print('Unknown operating system!!!')
        exit()

    data = read_reviews(driver_path, inputFile)

    date = get_date(inputFile)

    article_date = date.split(',')[0]+','+date.split(',')[1]


    field_names = ['asin', 'product_title', 'rating', 'review_title', 'variation', 'review_text', 'review-links', 'review-date', 'verified','article-date','days','category']

    expanded_reviews = []



    def days_between(d1, d2):
        d1 = datetime.strptime(d1, "%B %d, %Y")
        d2 = datetime.strptime(d2, "%B %d, %Y")
        return ((d1 - d2).days)

    for product_reviews in data:
        _asin = product_reviews['asin']
        _title = product_reviews['title']
        _data = product_reviews['data']

        for _d in _data:
            expanded_reviews.append([_asin, _title, _d[0], _d[1], _d[2], _d[3], _d[4], _d[5], _d[6],article_date,days_between(_d[5],article_date), _d[7]])



    if not os.path.exists(write_path):
            os.mkdir(write_path)

    outfile = write_path+filename+'.csv'            

    with io.open(outfile, 'w', encoding="utf-8", newline='') as dataFile:
        writer = csv.writer(dataFile, delimiter=',')

        writer.writerow(field_names)
        for e in expanded_reviews:
            writer.writerow(e)

        print(f'Output written')




