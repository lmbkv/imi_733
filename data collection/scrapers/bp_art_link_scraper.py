#bestproducts article links scraper

from selenium import webdriver
import time
import csv
import io

driver = webdriver.Chrome('/home/aalymbek/Desktop/chrome/chromedriver')
driver.get('https://www.bestproducts.com/tech/')
#driver.get('https://www.bestproducts.com/beauty/')
#driver.get('https://www.bestproducts.com/home/')
#driver.get('https://www.bestproducts.com/parenting/')



art_links = []

def get_art_links():
	count = 0
	i=1

	while True:
		if(count<100):
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			l = driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div[' +str(i)+ ']/a')
			if len(l) != 0:
				link = l[0].get_attribute('href')
				print(i, link)
				art_links.append(link)
			time.sleep(4)
			i= i+1
			count=count+1
		else:
			count=0
			with io.open("out.txt", 'w') as dataFile:
				#writer = csv.writer(dataFile)
				for e in art_links:
				#print(art_links)
					dataFile.write(e+"\n")

	print(art_links)
       
            
get_art_links()
