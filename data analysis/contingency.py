import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
import numpy as np
import scipy

path = "/home/aroun/Documents/Sem2/Project/Final/Buzzfeed/Buzzfeed_Reviews_Folder/"

fn =  (x for x in os.listdir(path) if '.~' not in x)

df = pd.DataFrame()
count = 0

for filename in fn:
    try:
        count = count + 1

        full_path = path+filename
        print(filename)

        dt = pd.read_csv(full_path)

        frames = [df, dt]

        df = pd.concat(frames)

        if count == 3:
            break
    
        
    except Exception:
        print()


comment_count_per_day_df = df.groupby(['asin','days']).size().to_frame('comment_count').reset_index()

comment_count_per_day_df = comment_count_per_day_df[(comment_count_per_day_df.days>=-10)&(comment_count_per_day_df.days<=10)].reset_index()

unique_asin = comment_count_per_day_df['asin'].unique()

comment_count_per_day_df_2 = comment_count_per_day_df.groupby(['asin'])[['comment_count']].mean()

mer_df = pd.merge(comment_count_per_day_df, comment_count_per_day_df_2, on='asin').reset_index()

def comm_checker(x,y):
    if x >= y:
        return 1
    else:
        return 0

def day_checker(x):
    if x >= 0:
        return 1
    else:
        return 0

mer_df['comm_check'] = mer_df.apply(lambda row: comm_checker(row['comment_count_x'], row['comment_count_y']), axis=1)

mer_df['day_check'] = mer_df.apply(lambda row: day_checker(row['days']), axis=1)

val_cont = pd.crosstab(mer_df.day_check, mer_df.comm_check, margins=False)

y = scipy.stats.chi2_contingency(val_cont)
print(val_cont)
print("\nchi2 value : ", y[0])
print("p values : ", y[1])
print("degree of freedom : ", y[2])
