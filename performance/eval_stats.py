import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

###READ CSV AND PREPROCESS DATA###
df = pd.read_csv("stats_project.csv", sep=',')
df = df.loc[df['NAME']!='NAME']
df = df.replace({'%':''}, regex=True)
df['MEM USAGE / LIMIT'] = df['MEM USAGE / LIMIT'].str.split('M').str[0]
df['MEM USAGE / LIMIT'] = df['MEM USAGE / LIMIT'].str.split('B').str[0]
df[['CPU %', 'MEM USAGE / LIMIT', 'MEM %']] = df[['CPU %', 'MEM USAGE / LIMIT', 'MEM %']].apply(pd.to_numeric)

###SPLIT DATA###
group = df.groupby('NAME')
redis = group.get_group('redis')
chain = group.get_group('chain')
worker1 = group.get_group('local_worker1_1')
worker2 = group.get_group('local_worker2_1')
worker3 = group.get_group('local_worker3_1')

###ADD TIME STAMPS TO THE DATAFRAME###
redis['TIME'] = np.arange(0,len(redis)/2,0.5)
chain['TIME'] = np.arange(0,len(chain)/2,0.5)
worker1['TIME'] = np.arange(0,len(worker1)/2,0.5)
worker2['TIME'] = np.arange(0,len(worker2)/2,0.5)
worker3['TIME'] = np.arange(0,len(worker3)/2,0.5)

redis.plot(kind='scatter',x='TIME',y='CPU %',color='red')
plt.show()


