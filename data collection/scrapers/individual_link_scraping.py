import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import numpy
import csv


#OPENING THE HTML PAGES OF EACH SHOPPING LIST AND THEN GETTING THE DATE, PRODUCT TITLE, LINK TO THE PRODUCT, AND PRODUCT DESCRIPTION

finArray = numpy.empty(shape=(100,4), dtype=object)

fincounter = 0

path = "/home/aroun/Documents/Sem2/Project/Final/Buzzfeed/Links Folder"

for filename in os.listdir(path):
    
    finArray = numpy.empty(shape=(100,4), dtype=object)

    fincounter = 0

    print(filename)
    
    full_name = path+"/"+filename
    url = open(full_name,"r")

    data = url.read()

    soup = BeautifulSoup(data, 'html.parser')

#     print(soup.prettify())
    
    for x in soup.find_all('time'):
        # print(x.text)
        datetime = x.text.strip().replace("\n","")
    
    
    for x in soup.find_all(class_="subbuzz-image"):
        
        # print(x) 

        if(x.h3 != None and x.select_one("figure > div:nth-of-type(2) > div:nth-of-type(2)") != None and x.select_one("h3 > span:nth-of-type(2) > a") != None):
            finArray[fincounter][0] = datetime
            # print(x.h3.text)
            finArray[fincounter][1] = x.h3.text.strip().replace("\n","")
            # print(x.select_one("figure > div:nth-of-type(2) > div:nth-of-type(2)").text.strip())
            finArray[fincounter][2] = x.select_one("figure > div:nth-of-type(2) > div:nth-of-type(2)").text.strip().replace("\n","")
            # print(x.select_one("h3 > span:nth-of-type(2) > a")['href'])
            finArray[fincounter][3] = x.select_one("h3 > span:nth-of-type(2) > a")['href']
            
#         print(x.figure.div.div:nth-of-type(2).div.p.text)

            fincounter = fincounter+1
    
    temparr = ['date time','name','description','link']

    finArray3 = numpy.vstack([temparr,finArray])

    df = pd.DataFrame(finArray3)
    
    outdir = "./"+"CSV Folder"
    
    fullname = os.path.join(outdir, filename+".csv")
    
    if not os.path.exists(outdir):
            os.mkdir(outdir)
    
    df.to_csv(fullname,header=None,index=False)

    