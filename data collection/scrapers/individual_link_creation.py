import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

df = pd.read_csv("main_shoppig_page.csv", usecols=['Shopping List','Link'])

# READING THE BUZZFEED SHOPPING PAGE SITE AND CREATING A CSV FILE FOR EACH LINK IN THE FILE

for index, row in df.iterrows():
    print(index, row['Shopping List'], row['Link'])
    
    outdir = "/home/aroun/Documents/Sem2/Project/Final/Buzzfeed/Links Folder/"
    
    if(index == 136):
        sindex = str(index)

        response = requests.get(row['Link'])

        outname = row['Shopping List'][:10]+".txt"
    
        fullname = os.path.join(outdir, outname)    

        if not os.path.exists(outdir):
            os.mkdir(outdir)

        f = open(fullname,"w")

        f.write((response.text))
        
    else:
    
        response = requests.get(row['Link'])
        
        outname = row['Shopping List']+".txt"

        fullname = os.path.join(outdir, outname)    

        if not os.path.exists(outdir):
            os.mkdir(outdir)

        f = open(fullname,"w")

        f.write((response.text))


