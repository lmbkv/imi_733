import os
import pandas as pd

#trying to find the percentage change in the number of comments that each product in each category is getting before and after the release of the article

path = "/home/aroun/Documents/Sem2/Project/Final/Buzzfeed/Buzzfeed_Reviews_Folder/"

fn =  (x for x in os.listdir(path) if '.~' not in x)

for filename in fn:
    print(filename)
    full_path = path+filename
    df = pd.read_csv(full_path)

#     display(df)
   #COUNT OF COMMENTS PER DAY
    
#     comment_count_per_day_df = df.groupby('days').size().to_frame('Comment_count').reset_index()
    
#     comment_count_per_day_df.plot.line(figsize=(15,4),grid=False,x='days',y='Comment_count',xlim=(-100,200))
    


df_gp = df.copy()


#counting how many comments each product in each category is getting on each day
df_gp = df_gp.groupby(['asin','days','category']).size().to_frame('counts').reset_index()

#finding the cummulatie sum of the number of comments each day of each product in each category  
df_grouped_asin = df_gp.groupby(by=['asin','days','category']).sum().groupby(level=[0]).cumsum().reset_index()


#finding the unique products
unique_asin = df_grouped_asin['asin'].unique()


#dividing the days into before and after the release of the article
df_before_30 = df_grouped_asin[(df_grouped_asin.days >= -30 ) & (df_grouped_asin.days < 0)]

df_after_30 = df_grouped_asin[(df_grouped_asin.days <= 30 ) & (df_grouped_asin.days >= 0)]

categ_df = df.copy()
# print(categ_df.info())

categ_df = categ_df.drop_duplicates(["asin", "category"])

categ_df = categ_df[['asin','category']]

unique_asin_categ = categ_df.values.tolist()

#finding the min day, zero day (from both df), max day for each asin

min_day_asin = {} #finding the minimum day on which a product has comments in the range of -30 to 0
zero_day_asin_1 = {}  ##finding the Maximum day on which a product has comments in the range of -30 to 0
zero_day_asin_2 = {}#finding the minimum day on which a product has comments in the range of 0 to 30
max_day_asin = {}#finding the maximum day on which a product has comments in the range of 0 to 30


#the cummulative sum of the product on the corresponding min and max days
min_day_csum = {} 
zero_day_csum_1 = {}
zero_day_csum_2 = {}
max_day_csum = {}

nt = []
for x in unique_asin_categ:
    nt.append((x[0],x[1]))
    
for x in nt:
    print(x[0])


for x in nt:
    min_day_asin.update( {x : df_before_30[df_before_30.asin == x[0]]['days'].min()} )
    zero_day_asin_1.update({x : df_before_30[df_before_30.asin == x[0]]['days'].max()})
    zero_day_asin_2.update({x : df_after_30[df_after_30.asin == x[0]]['days'].min()})
    max_day_asin.update({x : df_after_30[df_after_30.asin == x[0]]['days'].max()})



for x,y in min_day_asin.items():
    min_day_csum.update({x : df_before_30[(df_before_30.asin == x[0]) & (df_before_30.days == y)]['counts'].iloc[0]})

for x,y in zero_day_asin_1.items():
    zero_day_csum_1.update({x : df_before_30[(df_before_30.asin == x[0]) & (df_before_30.days == y)]['counts'].iloc[0]})

for x,y in zero_day_asin_2.items():
    try:
        zero_day_csum_2.update({x : df_after_30[(df_after_30.asin == x[0]) & (df_after_30.days == y)]['counts'].iloc[0]})
    except IndexError:
        print()
 
for x,y in max_day_asin.items():
    try:
        max_day_csum.update({x : df_after_30[(df_after_30.asin == x[0]) & (df_after_30.days == y)]['counts'].iloc[0]})
    except IndexError:
        print()


asin_perc_change = {}
nl = []
# for x in unique_asin_categ:
#     nl.append(x[0]+" "+x[1])


for x in nt:
    try:
        p1 = min_day_csum.get(x) # -30
        p2 = zero_day_csum_1.get(x) # 0

        inc1 = p2 - p1 # diff

        perc1 = (inc1/p1)*100 

        total_days1 = zero_day_asin_1.get(x) - min_day_asin.get(x)
        
        perday1 = perc1/total_days1
        
        q1 = zero_day_csum_2.get(x)
        q2 = max_day_csum.get(x)

        inc2 = q2 - q1

        perc2 = (inc2/q1)*100

        total_days2 = max_day_asin.get(x) - zero_day_asin_2.get(x)
        
        perday2 = perc2/total_days2
        
        pinc = perc2 - perc1

        asin_perc_change.update( {x : pinc} )
    except TypeError:
        print()

keyl = []
vall = []

for key,value in asin_perc_change.items():
	
	keyl.append(key)

	vall.append(value)



df_final = pd.DataFrame( { 'key' : keyl, 'value' : vall })

df_final.to_csv('key_value.csv',header=False,index=False)

# for key, value in asin_perc_change.items():
# print(df_final.head(5))
