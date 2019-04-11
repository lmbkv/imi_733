import re
import os
import pandas as pd
import matplotlib.pyplot as plt
import collections
import sys


sys.setrecursionlimit(2000)

path = "/home/aroun/Documents/Sem2/Project/Final/Predictions/Intermediate_File/"


fn =  (x for x in os.listdir(path) if '.~' not in x)

for filename in fn:
    if(filename == '26 Cheap Things To Treat Yourself To Right Now.txt.csv.csv.csv'):
        continue
    print(filename)
    full_path = path+filename
    df = pd.read_csv(full_path)
    break



comment_df = df.drop_duplicates(["asin", "review_text"])

comment_df = comment_df[['asin','review_text']]
# comment_df = comment_df.groupby('asin')
asin_comments = comment_df.values.tolist()

at = {}

for x in asin_comments:
    at.update({x[0] : ''})

# d['word'] = [d['word'],'something']

for [x,y] in asin_comments:
    at.update({x : at[x]+ ' . ' + y})


summary_dict = {}
import heapq  
import nltk

freq_dict = {}


for key,value in at.items():
    article_text = value
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)  
    article_text = re.sub(r'\s+', ' ', article_text)
#     formatted_article_text = article_text
    formatted_article_text = re.sub(r'[^\w\s]','',article_text)  
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
    # nltk.download('punkt')
    sentence_list = nltk.sent_tokenize(article_text)
#     print(sentence_list)
    
#     nltk.download('stopwords')

    stopwords = nltk.corpus.stopwords.words('english')
    formatted_article_text = formatted_article_text.lower()
    word_frequencies = {}  
    for word in nltk.word_tokenize(formatted_article_text):  
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
                
    maximum_frequncy = max(word_frequencies.values())

#     print(word_frequencies)
    
    
    for word in word_frequencies.keys():  
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
     
    
    freq_dict.update( { key : word_frequencies } )


count = 0

for key, value in freq_dict.items():
    count = count + 1
# sorted_dict = OrderedDict(sorted_x)

def quickSort(arr,low,high): 
    if low < high: 
  
        # pi is partitioning index, arr[p] is now 
        # at right place 
        pi = partition(arr,low,high) 
  
        # Separately sort elements before 
        # partition and after partition 
        quickSort(arr, low, pi-1) 
        quickSort(arr, pi+1, high) 



def partition(arr,low,high): 
    i = ( low-1 )         # index of smaller element 
    pivot = arr[high][1]     # pivot 
  
    for j in range(low , high): 
  
        # If current element is smaller than or 
        # equal to pivot 
        if   arr[j][1] <= pivot: 
          
            # increment index of smaller element 
            i = i+1 
            arr[i],arr[j] = arr[j],arr[i] 
  
    arr[i+1],arr[high] = arr[high],arr[i+1] 
    return ( i+1 ) 

        

cl = ['mistyrose','salmon','lightcoral','indianred','brown','firebrick','maroon','darkred']

t = []

for key,value in freq_dict.items():
    t=[]
    for x,y in value.items():
        t.append([x,y])
    quickSort(t,0,len(t)-1)
#     print(key,t[-8:])

# newList = quickSort(t,0,len(t)-1)
# print(t[:10])
    plt.figure()

    
    plot_df = pd.DataFrame(t[-8:],columns=['word','frequency'])
    fig=plot_df.plot.barh(x='word',y='frequency',ylim=(0,1),figsize=(15,4),color=cl)
    plt.savefig(key+".pdf")
