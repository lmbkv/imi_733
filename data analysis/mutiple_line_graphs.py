import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing

path = "/home/aroun/Documents/Sem2/Project/Final/Buzzfeed/Buzzfeed_Reviews_Folder/"

fn =  (x for x in os.listdir(path) if '.~' not in x)

ax = plt.gca()

df = pd.DataFrame()
count = 0

for filename in fn:
    
    count = count + 1
    
    full_path = path+filename
    print(filename)
    
    df = pd.read_csv(full_path)
    
    plt.figure()    
    comment_count_per_day_df = df.groupby('days').size().to_frame('comment_count').reset_index()


    x = comment_count_per_day_df[['comment_count']].values.astype(float)

    min_max_scaler = preprocessing.MinMaxScaler()

    x_scaled = min_max_scaler.fit_transform(x)

    df_normalized = pd.DataFrame(x_scaled)

    comment_count_per_day_df['scaled_count'] = x_scaled



    plot = comment_count_per_day_df.plot.line(figsize=(10,5),grid=False,x='days',color = 'darkred', y='scaled_count',xlim=(-30,30),ax=ax)
    
    plot.set_facecolor("#F2F2F2")

    
    if count > 2:
        break

plot.get_figure().savefig('multiple_line_graphs.pdf', format='pdf')
