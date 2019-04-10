import re
import os
import pandas as pd
import heapq  
import nltk

path = "/home/aroun/Documents/Sem2/Project/Final/Predictions/Intermediate_File/"


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



fn =  (x for x in os.listdir(path) if '.~' not in x)

for filename in fn:
    print(filename)
    full_path = path+filename
    df = pd.read_csv(full_path)
    break


nlp_df = df[['asin','review_title','review_text','category','image_link']]

category_df = nlp_df[['asin','category']]
title_df = nlp_df[['asin','review_title']]
comment_df = nlp_df[['asin','review_text']]
image_df = nlp_df[['asin','image_link']]


title_list = title_df.values.tolist()
comment_list = comment_df.values.tolist()
image_list = image_df.drop_duplicates().values.tolist()
category_list = category_df.drop_duplicates().values.tolist()

at = {}


for x in title_list:
    at.update({x[0] : ''})

# d['word'] = [d['word'],'something']

for [x,y] in title_list:
    at.update({x : at[x]+ ' . ' + y})


category_dict = {}

for x in category_list:
    category_dict.update({x[0] : ''})

# d['word'] = [d['word'],'something']

for [x,y] in category_list:
    category_dict.update({x : y})





# THE FOLLOWING NLP TEXT SUMMARIZER WAS PARTIALLY ADAPTED FROM THE BLOG Text Summarization with NLTK in Python BY Usman Malik

title_dict = {}


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
    
    # nltk.download('stopwords')

    stopwords = nltk.corpus.stopwords.words('english')

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
        
    
    sentence_scores = {}  
    for sent in sentence_list:  
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    
    
    summary_sentences = heapq.nlargest(1, sentence_scores, key=sentence_scores.get)
    summary = ''
    summary = ' '.join(summary_sentences)  
      
    title_dict.update( { key : summary } )


at = {}


for x in comment_list:
    at.update({x[0] : ''})

# d['word'] = [d['word'],'something']

for [x,y] in comment_list:
    at.update({x : at[x]+ ' . ' + y})


comment_dict = {}


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
    
    # nltk.download('stopwords')

    stopwords = nltk.corpus.stopwords.words('english')

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
        
    
    sentence_scores = {}  
    for sent in sentence_list:  
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    
    
    summary_sentences = heapq.nlargest(3, sentence_scores, key=sentence_scores.get)
    summary = ''
    summary = ' '.join(summary_sentences)  
      
    comment_dict.update( { key : summary } )




image_dict = {}

for [x,y] in image_list:
	image_dict.update({x : y[3:-3]})



# print(category_dict,image_dict)


html_text = html_text + """ <div class="header">
  <h2>Top cute things you can buy right now</h2>
</div><div class="row">
  <div class="leftcolumn">
"""

for key,value in title_dict.items():
	html_text = html_text + """<div class="card"><h2>""" + value + """</h2>"""
	html_text = html_text + """<h5>"""+category_dict[key]+"""</h5>"""
	html_text = html_text + """<img src=" """+ image_dict[key] +""" ">"""
	html_text = html_text + "<h3><p>" + comment_dict[key] + "</p></h3></div>"



html_text = html_text + """</div>
</div>


</body>
</html>
"""



with open('testy.html', 'w') as file:
    file.write(html_text)