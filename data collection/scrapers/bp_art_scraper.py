from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome('/Users/shree/BigDataProg/Project/chromedriver')
amz_links = []
names = []
date = []
desc = []
driver.get('https://www.bestproducts.com/beauty/g2072/beauty-products-based-on-astrological-sign/?slide=1')
content = driver.page_source.encode('utf-8').strip()
soup = BeautifulSoup(content,"html.parser")
prod = soup.findAll('div', {'class': 'product-slide-content'})


links = soup.findAll('a', {'class': 'product-btn-link'})
for link in links:
    amz_links.append(link.get('href'))
    l = link.parent.parent.find("div",{"class":"slideshow-slide-hed"})
    names.append(l.getText())

dt = soup.findAll('time', {'class':'content-info-date'})

for d in dt:
    for name in names:
        date.append(d.getText())


desc_tags = soup.findAll('div', {'class': 'slideshow-slide-dek'})
for tag in desc_tags:
    txt = ''
    p_tags = tag.findAll('p')
    for p in p_tags:
        txt = txt + p.getText()
    desc.append(txt)



art_dt = []
for item in date:
    art_dt.append(item.strip().replace("Updated:","").strip())

tup = list(zip(names,amz_links,art_dt,desc))

df = pd.DataFrame(tup, columns=['Product_name','Amazon_link', 'Article_date', 'Product_desc'])
print(df)
df.to_csv(r'out_art.csv')
#print(names)
