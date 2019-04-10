import re
import os
import pandas as pd
from amazon_sec import read_reviews, get_date
from amazon_sec import is_valid_file
import argparse
import os
import csv
import io
from datetime import datetime



path = "/home/aroun/Documents/Sem2/Project/Final/Predictions/"
write_path = "/home/aroun/Documents/Sem2/Project/Final/Predictions/Combined_File/"

fn =  (x for x in os.listdir(path) if( '.~' not in x and 'Combined_File' not in x and 'Intermediate_File' not in x))

df = pd.DataFrame()


# # The following code was partially adapated from Abe Flansburg (https://github.com/aflansburg)

# COMBINING ALL THE PREDICTION FILES

for filename in fn:
	print(filename)
	full_path = path+filename
	print(full_path)
	dt = pd.read_csv(full_path)
	frames = [df,dt]
	df = pd.concat(frames)


df = df[(df.predict==1)][['asin']]

fullname = os.path.join(write_path, "this.csv")
    
if not os.path.exists(write_path):
	os.mkdir(write_path)
	    
df.to_csv(fullname,header=None,index=False)
print('combined file created')


# READING THE COMBINED FILE TO GET THE DETAILS FROM AMAZON


read_path = "/home/aroun/Documents/Sem2/Project/Final/Predictions/Combined_File/"

write_path = "/home/aroun/Documents/Sem2/Project/Final/Predictions/Intermediate_File/"



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

    # date = get_date(inputFile)

    # article_date = date.split(',')[0]+','+date.split(',')[1]


    field_names = ['asin', 'product_title', 'rating', 'review_title', 'variation', 'review_text', 'review-links', 'review-date', 'verified','category','image_link']

    expanded_reviews = []


    for product_reviews in data:
        _asin = product_reviews['asin']
        _title = product_reviews['title']
        _data = product_reviews['data']

        for _d in _data:
            expanded_reviews.append([_asin, _title, _d[0], _d[1], _d[2], _d[3], _d[4], _d[5], _d[6], _d[7],_d[8]])



    if not os.path.exists(write_path):
            os.mkdir(write_path)

    outfile = write_path+filename+'.csv'            

    with io.open(outfile, 'w', encoding="utf-8", newline='') as dataFile:
        writer = csv.writer(dataFile, delimiter=',')

        writer.writerow(field_names)
        for e in expanded_reviews:
            writer.writerow(e)

        print(f'Intermediate File written')



# NOW WORKING ON MAKKING AN HTML FILE

html_text = """ <!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {
  box-sizing: border-box;
}

/* Add a gray background color with some padding */
body {
  font-family: Arial;
  padding: 20px;
  background: #f1f1f1;
}

/* Header/Blog Title */
.header {
  padding: 30px;
  font-size: 40px;
  text-align: center;
  background: white;
}

/* Create two unequal columns that floats next to each other */
/* Left column */
.leftcolumn {   
  float: center;
  width: 60%;
}

/* Right column */
.rightcolumn {
  float: left;
  width: 25%;
  padding-left: 20px;
}

/* Fake image */
.fakeimg {
  background-color: #aaa;
  width: 100%;
  padding: 20px;
}

/* Add a card effect for articles */
.card {
   background-color: white;
   padding: 20px;
   margin-top: 20px;
}

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}

/* Footer */
.footer {
  padding: 20px;
  text-align: center;
  background: #ddd;
  margin-top: 20px;
}

/* Responsive layout - when the screen is less than 800px wide, make the two columns stack on top of each other instead of next to each other */
@media screen and (max-width: 800px) {
  .leftcolumn, .rightcolumn {   
    width: 100%;
    padding: 0;
  }
}
</style>
</head>
<body>
"""



html_text = html_text + """ <div class="header">
  <h2>Top cute things you can buy right now</h2>
</div>

<div class="row">
  <div class="leftcolumn">
    <div class="card">
      <h2>Great shoes for a good price</h2>
      <h5>Clothing, Shoes, Jewelry, Women, Shoes, Flats </h5>
      
      <img src="https://images-na.ssl-images-amazon.com/images/I/813wcgtgTFL._UY575_.jpg"> 
      <h3><p>Cute, comfy, I got a 9, I usually wear 9.5 a little snug at first, but I broke them in in no time, and now they are very comfortable. Most of all I enjoy wearing this shoe, it is soft, flexible, light feeling, and comfortable. I'm very happy with the color, style, and comfort of these shoes and would consider buying another pair in a different color..</p></h3>
    </div>
    <div class="card">
      <h2>Arrived with wrinkles, gifts for kids, we shall see</h2>
      <h5>Toys, Games, Baby, Toddler, Toys, Activity, Play, Centers</h5>
      <img src="https://images-na.ssl-images-amazon.com/images/I/51GMQFLIkNL._SX569_.jpg">
      <h3><p>Still, for the size,price, and to use it is overall a good buy and a good alternative to feeling bad about using a more expensive one. I guess this isn't okay product, I feel like I could have gone to local stores for the same price and gotten better quality. I thought I ordered the pink one, but got a brown one</p></h3>
    </div>

    <div class="card">
      <h2>Very cute, big mug, durable to washing </h2>
      <h5>Home, Kitchen, Kitchen, Dining, Dining, Entertaining, Novelty, Drinkware, Coffee, Mugs</h5>
      
      <img src="https://images-na.ssl-images-amazon.com/images/I/61h7qAfFkwL._SX569_.jpg"> 
      <h3><p>This is the new favorite because the mug stays cool while the drink gets hot in the microwave (and the little cat!). "Jessie" was a wonderful, smart and beautiful cat and we added a brother for her soon, another Black cat. I bought this mug for my sister who’s other (less adorable) cat mug broke.</p></h3>
    </div>

    <div class="card">
      <h2>Cute, fun, storage solution </h2>
      <h5>Home, Kitchen, Bath, Bathroom, Accessories, Holders, Dispensers, Toothbrush, Holders</h5>
      
      <img src="https://images-na.ssl-images-amazon.com/images/I/31TiMdQ2tvL.jpg"> 
      <h3><p>I bought this to go in our shower, it does hold two toothbrushes (which is why I bought it), but it didn't stick to our tile. Nice and sturdy, and mine is packed with two toothbrushes, a full size Sensodyne, a tongue scraper and floss picks. I wish I understood the strange magic that hold this to the wall of my shower, but it works, its amazing.</p></h3>
    </div>

    <div class="card">
      <h2>Too cute!</h2>
      <h5>Toys, Games, Stuffed, Animals, Plush, Toys</h5>
      
      <img src="https://images-na.ssl-images-amazon.com/images/I/81Z0ZD-0P2L._SX679_.jpg"> 
      <h3><p>This size is more small accent pillow(for a chair ) than floor pillow(like the full sized ones). It's a perfect size, not too big and not too small, just right. The 'cheese' part of the pillow is like a orange velvet.I do think it's a little pricy, but I couldn't resist.</p></h3>
    </div>

  </div>
</div>


</body>
</html>

"""