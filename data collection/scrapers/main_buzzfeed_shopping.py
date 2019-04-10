import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import os


# DOWNLOAD THE SHOPPING SECTION OF THE BUZZFEED SITE

url = 'https://www.buzzfeed.com/shopping'
r = requests.get(url)
f = open("buzzfeed_shopping.txt","w")
f.write(r.text)


# READING THE NEWLY CREATED FILE

f = open("buzzfeed_shopping.txt","r")
data = f.read()
soup = BeautifulSoup(data, 'html.parser')

#ACCESSING THE DATA



main_array = []

for x in soup.find_all(class_ = 'story-card'):
    if(x.h2 == None and x.a == None):
        continue
    else:
#         print(x.a['href'])
        link = x.a['href']
#         print(x.h2.text.strip())
        heading = x.h2.text.strip()
        main_array.append([heading,link])


temp_arr = ['Shopping List','Link']

labeled_main_array = np.vstack([temp_arr,main_array])

df = pd.DataFrame(labeled_main_array)  #all the data stored here


#################### CREATING A SUB DIRECTORY AND STORING THERE ################################################

outname = 'main_shoppig_page.csv'

outdir = '/home/aroun/Documents/Sem2/Project/Final/Buzzfeed/'
if not os.path.exists(outdir):
    os.mkdir(outdir)

fullname = os.path.join(outdir, outname)    

df.to_csv(fullname,header=None,index=False)

