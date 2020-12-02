import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

###READ CSV AND PREPROCESS DATA###
df_enh = pd.read_csv("stats_project.csv", sep=',')
df_enh = df_enh.loc[df_enh['NAME']!='NAME']
df_enh = df_enh.replace({'%':''}, regex=True)
df_enh['MEM USAGE / LIMIT'] = df_enh['MEM USAGE / LIMIT'].str.split('M').str[0]
df_enh['MEM USAGE / LIMIT'] = df_enh['MEM USAGE / LIMIT'].str.split('B').str[0]
df_enh[['CPU %', 'MEM USAGE / LIMIT', 'MEM %']] = df_enh[['CPU %', 'MEM USAGE / LIMIT', 'MEM %']].apply(pd.to_numeric)

df_ori = pd.read_csv("stats_felix.csv", sep=',')
df_ori = df_ori.loc[df_ori['NAME']!='NAME']
df_ori = df_ori.replace({'%':''}, regex=True)
df_ori['MEM USAGE / LIMIT'] = df_ori['MEM USAGE / LIMIT'].str.split('M').str[0]
df_ori['MEM USAGE / LIMIT'] = df_ori['MEM USAGE / LIMIT'].str.split('B').str[0]
df_ori[['CPU %', 'MEM USAGE / LIMIT', 'MEM %']] = df_ori[['CPU %', 'MEM USAGE / LIMIT', 'MEM %']].apply(pd.to_numeric)

###SPLIT DATA AND ADD STATS FOR WORKERS###
group = df_enh.groupby('NAME')
redis_enh = group.get_group('redis')
chain_enh = group.get_group('chain')
worker1_enh = group.get_group('local_worker1_1')
worker2_enh = group.get_group('local_worker2_1')
worker3_enh = group.get_group('local_worker3_1')

worker1_enh.index = np.arange(1, len(worker1_enh)+1)
worker2_enh.index = np.arange(1, len(worker2_enh)+1)
worker3_enh.index = np.arange(1, len(worker3_enh)+1)

cpu_enh = worker1_enh['CPU %'] + worker2_enh['CPU %'] + worker3_enh['CPU %']
mem_enh = worker1_enh['MEM USAGE / LIMIT'] + worker2_enh['MEM USAGE / LIMIT'] + worker3_enh['MEM USAGE / LIMIT']
workers_enh = pd.DataFrame(data={'CPU %': cpu_enh, 'MEM USAGE / LIMIT': mem_enh})

group = df_ori.groupby('NAME')
redis_ori = group.get_group('redis')
chain_ori = group.get_group('chain')
worker1_ori = group.get_group('local_worker1_1')
worker2_ori = group.get_group('local_worker2_1')
worker3_ori = group.get_group('local_worker3_1')

worker1_ori.index = np.arange(1, len(worker1_ori)+1)
worker2_ori.index = np.arange(1, len(worker2_ori)+1)
worker3_ori.index = np.arange(1, len(worker3_ori)+1)

cpu_ori = worker1_ori['CPU %'] + worker2_ori['CPU %'] + worker3_ori['CPU %']
mem_ori = worker1_ori['MEM USAGE / LIMIT'] + worker2_ori['MEM USAGE / LIMIT'] + worker3_ori['MEM USAGE / LIMIT']
workers_ori = pd.DataFrame(data={'CPU %': cpu_ori, 'MEM USAGE / LIMIT': mem_ori})

###ADD TIME STAMPS TO THE DATAFRAME###
redis_enh['TIME'] = np.arange(0,len(redis_enh)/2,0.5)
chain_enh['TIME'] = np.arange(0,len(chain_enh)/2,0.5)
workers_enh['TIME'] = np.arange(0,len(workers_enh)/2,0.5)

redis_ori['TIME'] = np.arange(0,len(redis_ori)/2,0.5)
chain_ori['TIME'] = np.arange(0,len(chain_ori)/2,0.5)
workers_ori['TIME'] = np.arange(0,len(workers_ori)/2,0.5)

###PLOT CPU% FOR REDIS###
ax1 = redis_enh.plot(kind='scatter',x='TIME',y='CPU %',color='red', label='Enhanced implementation')
ax2 = redis_ori.plot(kind='scatter',x='TIME',y='CPU %',color='blue', label='Original implementation', ax=ax1)
red = mpatches.Patch(color='red', label='Enhanced implementation')
blue = mpatches.Patch(color='blue', label='Original implementation')
plt.legend(handles=[red, blue])
plt.title('Redis CPU%')
plt.show()

###PLOT CPU% FOR CHAIN###
ax1 = chain_enh.plot(kind='scatter',x='TIME',y='CPU %',color='red', label='Enhanced implementation')
ax2 = chain_ori.plot(kind='scatter',x='TIME',y='CPU %',color='blue', label='Original implementation', ax=ax1)
red = mpatches.Patch(color='red', label='Enhanced implementation')
blue = mpatches.Patch(color='blue', label='Original implementation')
plt.legend(handles=[red, blue])
plt.title('Chain CPU%')
plt.show()

###PLOT SUM OF CPU% FOR WORKERS###
ax1 = workers_enh.plot(kind='scatter',x='TIME',y='CPU %',color='red', label='Enhanced implementation')
ax2 = workers_ori.plot(kind='scatter',x='TIME',y='CPU %',color='blue', label='Original implementation', ax=ax1)
red = mpatches.Patch(color='red', label='Enhanced implementation')
blue = mpatches.Patch(color='blue', label='Original implementation')
plt.legend(handles=[red, blue])
plt.title('Sum of Workers CPU%')
plt.show()

###PLOT MEM FOR REDIS###
ax1 = redis_enh.plot(kind='scatter',x='TIME',y='MEM USAGE / LIMIT',color='red', label='Enhanced implementation')
ax2 = redis_ori.plot(kind='scatter',x='TIME',y='MEM USAGE / LIMIT',color='blue', label='Original implementation', ax=ax1)
red = mpatches.Patch(color='red', label='Enhanced implementation')
blue = mpatches.Patch(color='blue', label='Original implementation')
plt.legend(handles=[red, blue])
plt.title('Redis Memory Usage')
plt.show()

###PLOT MEM FOR CHAIN###
ax1 = chain_enh.plot(kind='scatter',x='TIME',y='MEM USAGE / LIMIT',color='red', label='Enhanced implementation')
ax2 = chain_ori.plot(kind='scatter',x='TIME',y='MEM USAGE / LIMIT',color='blue', label='Original implementation', ax=ax1)
red = mpatches.Patch(color='red', label='Enhanced implementation')
blue = mpatches.Patch(color='blue', label='Original implementation')
plt.legend(handles=[red, blue])
plt.title('Chain Memory Usage')
plt.show()

###PLOT SUM OF CPU% FOR WORKERS###
ax1 = workers_enh.plot(kind='scatter',x='TIME',y='MEM USAGE / LIMIT',color='red', label='Enhanced implementation')
ax2 = workers_ori.plot(kind='scatter',x='TIME',y='MEM USAGE / LIMIT',color='blue', label='Original implementation', ax=ax1)
red = mpatches.Patch(color='red', label='Enhanced implementation')
blue = mpatches.Patch(color='blue', label='Original implementation')
plt.legend(handles=[red, blue])
plt.title('Sum of Workers Memory Usage')
plt.show()