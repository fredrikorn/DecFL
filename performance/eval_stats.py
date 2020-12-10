import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

###READ CSV AND PREPROCESS DATA###
df_enh1 = pd.read_csv("stats_project1.csv", sep=',')
df_enh1 = df_enh1.loc[df_enh1['NAME']!='NAME']
df_enh1.rename(columns={df_enh1.columns[4]: 'TIME' }, inplace = True)
df_enh1 = df_enh1.replace({'%':''}, regex=True)
df_enh1['MEM USAGE / LIMIT'] = df_enh1['MEM USAGE / LIMIT'].str.split('M').str[0]
df_enh1['MEM USAGE / LIMIT'] = df_enh1['MEM USAGE / LIMIT'].str.split('B').str[0]
df_enh1['TIME'] = df_enh1['TIME'].str[1:]
df_enh1['TIME'] = pd.to_datetime(df_enh1['TIME'], format="%H:%M:%S.%f")
df_enh1['TIME'] = ((df_enh1['TIME']-df_enh1['TIME'].iloc[0]).dt.total_seconds())
df_enh1[['CPU %', 'MEM USAGE / LIMIT', 'MEM %']] = df_enh1[['CPU %', 'MEM USAGE / LIMIT', 'MEM %',]].apply(pd.to_numeric)

df_enh2 = pd.read_csv("stats_project2.csv", sep=',')
df_enh2 = df_enh2.loc[df_enh2['NAME']!='NAME']
df_enh2.rename(columns={df_enh2.columns[4]: 'TIME' }, inplace = True)
df_enh2 = df_enh2.replace({'%':''}, regex=True)
df_enh2['MEM USAGE / LIMIT'] = df_enh2['MEM USAGE / LIMIT'].str.split('M').str[0]
df_enh2['MEM USAGE / LIMIT'] = df_enh2['MEM USAGE / LIMIT'].str.split('B').str[0]
df_enh2['TIME'] = df_enh2['TIME'].str[1:]
df_enh2['TIME'] = pd.to_datetime(df_enh2['TIME'], format="%H:%M:%S.%f")
df_enh2['TIME'] = ((df_enh2['TIME']-df_enh2['TIME'].iloc[0]).dt.total_seconds())
df_enh2[['CPU %', 'MEM USAGE / LIMIT', 'MEM %']] = df_enh2[['CPU %', 'MEM USAGE / LIMIT', 'MEM %',]].apply(pd.to_numeric)

df_enh3 = pd.read_csv("stats_project3.csv", sep=',')
df_enh3 = df_enh3.loc[df_enh3['NAME']!='NAME']
df_enh3.rename(columns={df_enh3.columns[4]: 'TIME' }, inplace = True)
df_enh3 = df_enh3.replace({'%':''}, regex=True)
df_enh3['MEM USAGE / LIMIT'] = df_enh3['MEM USAGE / LIMIT'].str.split('M').str[0]
df_enh3['MEM USAGE / LIMIT'] = df_enh3['MEM USAGE / LIMIT'].str.split('B').str[0]
df_enh3['TIME'] = df_enh3['TIME'].str[1:]
df_enh3['TIME'] = pd.to_datetime(df_enh3['TIME'], format="%H:%M:%S.%f")
df_enh3['TIME'] = ((df_enh3['TIME']-df_enh3['TIME'].iloc[0]).dt.total_seconds())
df_enh3[['CPU %', 'MEM USAGE / LIMIT', 'MEM %']] = df_enh3[['CPU %', 'MEM USAGE / LIMIT', 'MEM %',]].apply(pd.to_numeric)

df_ori1 = pd.read_csv("stats_project1.csv", sep=',')
df_ori1 = df_ori1.loc[df_ori1['NAME']!='NAME']
df_ori1.rename(columns={df_ori1.columns[4]: 'TIME' }, inplace = True)
df_ori1 = df_ori1.replace({'%':''}, regex=True)
df_ori1['MEM USAGE / LIMIT'] = df_ori1['MEM USAGE / LIMIT'].str.split('M').str[0]
df_ori1['MEM USAGE / LIMIT'] = df_ori1['MEM USAGE / LIMIT'].str.split('B').str[0]
df_ori1['TIME'] = df_ori1['TIME'].str[1:]
df_ori1['TIME'] = pd.to_datetime(df_ori1['TIME'], format="%H:%M:%S.%f")
df_ori1['TIME'] = ((df_ori1['TIME']-df_ori1['TIME'].iloc[0]).dt.total_seconds())
df_ori1[['CPU %', 'MEM USAGE / LIMIT', 'MEM %']] = df_ori1[['CPU %', 'MEM USAGE / LIMIT', 'MEM %']].apply(pd.to_numeric)

df_ori2 = pd.read_csv("stats_project2.csv", sep=',')
df_ori2 = df_ori2.loc[df_ori2['NAME']!='NAME']
df_ori2.rename(columns={df_ori2.columns[4]: 'TIME' }, inplace = True)
df_ori2 = df_ori2.replace({'%':''}, regex=True)
df_ori2['MEM USAGE / LIMIT'] = df_ori2['MEM USAGE / LIMIT'].str.split('M').str[0]
df_ori2['MEM USAGE / LIMIT'] = df_ori2['MEM USAGE / LIMIT'].str.split('B').str[0]
df_ori2['TIME'] = df_ori2['TIME'].str[1:]
df_ori2['TIME'] = pd.to_datetime(df_ori2['TIME'], format="%H:%M:%S.%f")
df_ori2['TIME'] = ((df_ori2['TIME']-df_ori2['TIME'].iloc[0]).dt.total_seconds())
df_ori2[['CPU %', 'MEM USAGE / LIMIT', 'MEM %']] = df_ori2[['CPU %', 'MEM USAGE / LIMIT', 'MEM %']].apply(pd.to_numeric)

df_ori3 = pd.read_csv("stats_project3.csv", sep=',')
df_ori3 = df_ori3.loc[df_ori3['NAME']!='NAME']
df_ori3.rename(columns={df_ori3.columns[4]: 'TIME' }, inplace = True)
df_ori3 = df_ori3.replace({'%':''}, regex=True)
df_ori3['MEM USAGE / LIMIT'] = df_ori3['MEM USAGE / LIMIT'].str.split('M').str[0]
df_ori3['MEM USAGE / LIMIT'] = df_ori3['MEM USAGE / LIMIT'].str.split('B').str[0]
df_ori3['TIME'] = df_ori3['TIME'].str[1:]
df_ori3['TIME'] = pd.to_datetime(df_ori3['TIME'], format="%H:%M:%S.%f")
df_ori3['TIME'] = ((df_ori3['TIME']-df_ori3['TIME'].iloc[0]).dt.total_seconds())
df_ori3[['CPU %', 'MEM USAGE / LIMIT', 'MEM %']] = df_ori3[['CPU %', 'MEM USAGE / LIMIT', 'MEM %']].apply(pd.to_numeric)

###SPLIT DATA AND ADD STATS FOR WORKERS###
group = df_enh1.groupby('NAME')
redis_enh1 = group.get_group('redis')
chain_enh1 = group.get_group('chain')
worker1_enh1 = group.get_group('local_worker1_1')
worker2_enh1 = group.get_group('local_worker2_1')
worker3_enh1 = group.get_group('local_worker3_1')
worker4_enh1 = group.get_group('local_worker4_1')
worker5_enh1 = group.get_group('local_worker5_1')

worker1_enh1.index = np.arange(1, len(worker1_enh1)+1)
worker2_enh1.index = np.arange(1, len(worker2_enh1)+1)
worker3_enh1.index = np.arange(1, len(worker3_enh1)+1)
worker4_enh1.index = np.arange(1, len(worker4_enh1)+1)
worker5_enh1.index = np.arange(1, len(worker5_enh1)+1)

group = df_enh2.groupby('NAME')
redis_enh2 = group.get_group('redis')
chain_enh2 = group.get_group('chain')
worker1_enh2 = group.get_group('local_worker1_1')
worker2_enh2 = group.get_group('local_worker2_1')
worker3_enh2 = group.get_group('local_worker3_1')
worker4_enh2 = group.get_group('local_worker4_1')
worker5_enh2 = group.get_group('local_worker5_1')

worker1_enh2.index = np.arange(1, len(worker1_enh2)+1)
worker2_enh2.index = np.arange(1, len(worker2_enh2)+1)
worker3_enh2.index = np.arange(1, len(worker3_enh2)+1)
worker4_enh2.index = np.arange(1, len(worker4_enh2)+1)
worker5_enh2.index = np.arange(1, len(worker5_enh2)+1)

group = df_enh3.groupby('NAME')
redis_enh3 = group.get_group('redis')
chain_enh3 = group.get_group('chain')
worker1_enh3 = group.get_group('local_worker1_1')
worker2_enh3 = group.get_group('local_worker2_1')
worker3_enh3 = group.get_group('local_worker3_1')
worker4_enh3 = group.get_group('local_worker4_1')
worker5_enh3 = group.get_group('local_worker5_1')

worker1_enh3.index = np.arange(1, len(worker1_enh3)+1)
worker2_enh3.index = np.arange(1, len(worker2_enh3)+1)
worker3_enh3.index = np.arange(1, len(worker3_enh3)+1)
worker4_enh3.index = np.arange(1, len(worker4_enh3)+1)
worker5_enh3.index = np.arange(1, len(worker5_enh3)+1)

group = df_ori1.groupby('NAME')
redis_ori1 = group.get_group('redis')
chain_ori1 = group.get_group('chain')
worker1_ori1 = group.get_group('local_worker1_1')
worker2_ori1 = group.get_group('local_worker2_1')
worker3_ori1 = group.get_group('local_worker3_1')
worker4_ori1 = group.get_group('local_worker4_1')
worker5_ori1 = group.get_group('local_worker5_1')

worker1_ori1.index = np.arange(1, len(worker1_ori1)+1)
worker2_ori1.index = np.arange(1, len(worker2_ori1)+1)
worker3_ori1.index = np.arange(1, len(worker3_ori1)+1)
worker4_ori1.index = np.arange(1, len(worker4_ori1)+1)
worker5_ori1.index = np.arange(1, len(worker5_ori1)+1)

group = df_ori2.groupby('NAME')
redis_ori2 = group.get_group('redis')
chain_ori2 = group.get_group('chain')
worker1_ori2 = group.get_group('local_worker1_1')
worker2_ori2 = group.get_group('local_worker2_1')
worker3_ori2 = group.get_group('local_worker3_1')
worker4_ori2 = group.get_group('local_worker4_1')
worker5_ori2 = group.get_group('local_worker5_1')

worker1_ori2.index = np.arange(1, len(worker1_ori2)+1)
worker2_ori2.index = np.arange(1, len(worker2_ori2)+1)
worker3_ori2.index = np.arange(1, len(worker3_ori2)+1)
worker4_ori2.index = np.arange(1, len(worker4_ori2)+1)
worker5_ori2.index = np.arange(1, len(worker5_ori2)+1)

group = df_ori3.groupby('NAME')
redis_ori3 = group.get_group('redis')
chain_ori3 = group.get_group('chain')
worker1_ori3 = group.get_group('local_worker1_1')
worker2_ori3 = group.get_group('local_worker2_1')
worker3_ori3 = group.get_group('local_worker3_1')
worker4_ori3 = group.get_group('local_worker4_1')
worker5_ori3 = group.get_group('local_worker5_1')

worker1_ori3.index = np.arange(1, len(worker1_ori3)+1)
worker2_ori3.index = np.arange(1, len(worker2_ori3)+1)
worker3_ori3.index = np.arange(1, len(worker3_ori3)+1)
worker4_ori3.index = np.arange(1, len(worker4_ori3)+1)
worker5_ori3.index = np.arange(1, len(worker5_ori3)+1)

###MAKE SOME CALCULATIONS###
cpu_enh1 = worker1_enh1['CPU %'] + worker2_enh1['CPU %'] + worker3_enh1['CPU %'] + worker4_enh1['CPU %'] + worker5_enh1['CPU %']
mem_enh1 = worker1_enh1['MEM USAGE / LIMIT'] + worker2_enh1['MEM USAGE / LIMIT'] + worker3_enh1['MEM USAGE / LIMIT'] + worker4_enh1['MEM USAGE / LIMIT'] + worker5_enh1['MEM USAGE / LIMIT']
workers_enh1 = pd.DataFrame(data={'CPU %': cpu_enh1, 'MEM USAGE / LIMIT': mem_enh1, 'TIME': worker1_enh1['TIME']})
workers_enh1['ACCUMULATED CPU %'] = workers_enh1['CPU %'].cumsum()
workers_enh1['ACCUMULATED MEM USAGE'] = workers_enh1['MEM USAGE / LIMIT'].cumsum()

cpu_enh2 = worker1_enh2['CPU %'] + worker2_enh2['CPU %'] + worker3_enh2['CPU %'] + worker4_enh2['CPU %'] + worker5_enh2['CPU %']
mem_enh2 = worker1_enh2['MEM USAGE / LIMIT'] + worker2_enh2['MEM USAGE / LIMIT'] + worker3_enh2['MEM USAGE / LIMIT'] + worker4_enh2['MEM USAGE / LIMIT'] + worker5_enh2['MEM USAGE / LIMIT']
workers_enh2 = pd.DataFrame(data={'CPU %': cpu_enh2, 'MEM USAGE / LIMIT': mem_enh2, 'TIME': worker1_enh2['TIME']})
workers_enh2['ACCUMULATED CPU %'] = workers_enh2['CPU %'].cumsum()
workers_enh2['ACCUMULATED MEM USAGE'] = workers_enh2['MEM USAGE / LIMIT'].cumsum()

cpu_enh3 = worker1_enh3['CPU %'] + worker2_enh3['CPU %'] + worker3_enh3['CPU %'] + worker4_enh3['CPU %'] + worker5_enh3['CPU %']
mem_enh3 = worker1_enh3['MEM USAGE / LIMIT'] + worker2_enh3['MEM USAGE / LIMIT'] + worker3_enh3['MEM USAGE / LIMIT'] + worker4_enh3['MEM USAGE / LIMIT'] + worker5_enh3['MEM USAGE / LIMIT']
workers_enh3 = pd.DataFrame(data={'CPU %': cpu_enh3, 'MEM USAGE / LIMIT': mem_enh3, 'TIME': worker1_enh3['TIME']})
workers_enh3['ACCUMULATED CPU %'] = workers_enh3['CPU %'].cumsum()
workers_enh3['ACCUMULATED MEM USAGE'] = workers_enh3['MEM USAGE / LIMIT'].cumsum()

cpu_ori1 = worker1_ori1['CPU %'] + worker2_ori1['CPU %'] + worker3_ori1['CPU %'] + worker4_ori1['CPU %'] + worker5_ori1['CPU %']
mem_ori1 = worker1_ori1['MEM USAGE / LIMIT'] + worker2_ori1['MEM USAGE / LIMIT'] + worker3_ori1['MEM USAGE / LIMIT'] + worker4_ori1['MEM USAGE / LIMIT'] + worker5_ori1['MEM USAGE / LIMIT']
workers_ori1 = pd.DataFrame(data={'CPU %': cpu_ori1, 'MEM USAGE / LIMIT': mem_ori1, 'TIME': worker1_enh1['TIME']})
workers_ori1['ACCUMULATED CPU %'] = workers_ori1['CPU %'].cumsum()
workers_ori1['ACCUMULATED MEM USAGE'] = workers_ori1['MEM USAGE / LIMIT'].cumsum()

cpu_ori2 = worker1_ori2['CPU %'] + worker2_ori2['CPU %'] + worker3_ori2['CPU %'] + worker4_ori2['CPU %'] + worker5_ori2['CPU %']
mem_ori2 = worker1_ori2['MEM USAGE / LIMIT'] + worker2_ori2['MEM USAGE / LIMIT'] + worker3_ori2['MEM USAGE / LIMIT'] + worker4_ori2['MEM USAGE / LIMIT'] + worker5_ori2['MEM USAGE / LIMIT']
workers_ori2 = pd.DataFrame(data={'CPU %': cpu_ori2, 'MEM USAGE / LIMIT': mem_ori2, 'TIME': worker1_enh2['TIME']})
workers_ori2['ACCUMULATED CPU %'] = workers_ori2['CPU %'].cumsum()
workers_ori2['ACCUMULATED MEM USAGE'] = workers_ori2['MEM USAGE / LIMIT'].cumsum()

cpu_ori3 = worker1_ori3['CPU %'] + worker2_ori3['CPU %'] + worker3_ori3['CPU %'] + worker4_ori3['CPU %'] + worker5_ori3['CPU %']
mem_ori3 = worker1_ori3['MEM USAGE / LIMIT'] + worker2_ori3['MEM USAGE / LIMIT'] + worker3_ori3['MEM USAGE / LIMIT'] + worker4_ori3['MEM USAGE / LIMIT'] + worker5_ori3['MEM USAGE / LIMIT']
workers_ori3 = pd.DataFrame(data={'CPU %': cpu_ori3, 'MEM USAGE / LIMIT': mem_ori3, 'TIME': worker1_enh3['TIME']})
workers_ori3['ACCUMULATED CPU %'] = workers_ori3['CPU %'].cumsum()
workers_ori3['ACCUMULATED MEM USAGE'] = workers_ori3['MEM USAGE / LIMIT'].cumsum()

redis_enh1['ACCUMULATED CPU %'] = redis_enh1['CPU %'].cumsum()
redis_enh2['ACCUMULATED CPU %'] = redis_enh2['CPU %'].cumsum()
redis_enh3['ACCUMULATED CPU %'] = redis_enh3['CPU %'].cumsum()
redis_ori1['ACCUMULATED CPU %'] = redis_ori1['CPU %'].cumsum()
redis_ori2['ACCUMULATED CPU %'] = redis_ori2['CPU %'].cumsum()
redis_ori3['ACCUMULATED CPU %'] = redis_ori3['CPU %'].cumsum()

chain_enh1['ACCUMULATED CPU %'] = chain_enh1['CPU %'].cumsum()
chain_enh2['ACCUMULATED CPU %'] = chain_enh2['CPU %'].cumsum()
chain_enh3['ACCUMULATED CPU %'] = chain_enh3['CPU %'].cumsum()
chain_ori1['ACCUMULATED CPU %'] = chain_ori1['CPU %'].cumsum()
chain_ori2['ACCUMULATED CPU %'] = chain_ori2['CPU %'].cumsum()
chain_ori3['ACCUMULATED CPU %'] = chain_ori3['CPU %'].cumsum()

###CALCULATE MEAN FOR EACH CONTAINER###
redis_enh = pd.concat((redis_enh1, redis_enh2, redis_enh3))
redis_enh = redis_enh.groupby(redis_enh.index)
redis_enh = redis_enh.mean()

redis_ori = pd.concat((redis_ori1, redis_ori2, redis_ori3))
redis_ori = redis_ori.groupby(redis_ori.index)
redis_ori = redis_ori.mean()

chain_enh = pd.concat((chain_enh1, chain_enh2, chain_enh3))
chain_enh = chain_enh.groupby(chain_enh.index)
chain_enh = chain_enh.mean()

chain_ori = pd.concat((chain_ori1, chain_ori2, chain_ori3))
chain_ori = chain_ori.groupby(chain_ori.index)
chain_ori = chain_ori.mean()

workers_enh = pd.concat((workers_enh1, workers_enh2, workers_enh3))
workers_enh = workers_enh.groupby(workers_enh.index)
workers_enh = workers_enh.mean()

workers_ori = pd.concat((workers_ori1, workers_ori2, workers_ori3))
workers_ori = workers_ori.groupby(workers_ori.index)
workers_ori = workers_ori.mean()

print(redis_enh1.head())
print(redis_enh2.head())
print(redis_enh3.head())
print(redis_enh.head())

print(len(redis_enh1))
print(len(redis_enh2))
print(len(redis_enh3))

###PLOT CPU% FOR REDIS###
ax1 = redis_enh.plot(kind='line',x='TIME',y='CPU %',color='red', label='Enhanced implementation')
ax2 = redis_ori.plot(kind='line',x='TIME',y='CPU %',color='blue', label='Original implementation', ax=ax1)
red = mpatches.Patch(color='red', label='Enhanced implementation')
blue = mpatches.Patch(color='blue', label='Original implementation')
plt.legend(handles=[red, blue])
plt.title('Redis CPU%')
plt.xlabel('TIME [s]')
plt.ylabel('CPU %')
plt.show()

###PLOT ACCUMULATED CPU% FOR REDIS###
ax1 = redis_enh.plot(kind='line',x='TIME',y='ACCUMULATED CPU %',color='red', label='Enhanced implementation')
ax2 = redis_ori.plot(kind='line',x='TIME',y='ACCUMULATED CPU %',color='blue', label='Original implementation', ax=ax1)
red = mpatches.Patch(color='red', label='Enhanced implementation')
blue = mpatches.Patch(color='blue', label='Original implementation')
plt.legend(handles=[red, blue])
plt.title('Accumulated Redis CPU%')
plt.xlabel('TIME [s]')
plt.ylabel('CPU %')
plt.show()

###PLOT CPU% FOR CHAIN###
ax1 = chain_enh.plot(kind='line',x='TIME',y='CPU %',color='red', label='Enhanced implementation')
ax2 = chain_ori.plot(kind='line',x='TIME',y='CPU %',color='blue', label='Original implementation', ax=ax1)
red = mpatches.Patch(color='red', label='Enhanced implementation')
blue = mpatches.Patch(color='blue', label='Original implementation')
plt.legend(handles=[red, blue])
plt.title('Chain CPU%')
plt.xlabel('TIME [s]')
plt.ylabel('CPU %')
plt.show()

###PLOT ACCUMULATED CPU% FOR CHAIN###
ax1 = chain_enh.plot(kind='line',x='TIME',y='ACCUMULATED CPU %',color='red', label='Enhanced implementation')
ax2 = chain_ori.plot(kind='line',x='TIME',y='ACCUMULATED CPU %',color='blue', label='Original implementation', ax=ax1)
red = mpatches.Patch(color='red', label='Enhanced implementation')
blue = mpatches.Patch(color='blue', label='Original implementation')
plt.legend(handles=[red, blue])
plt.title('Accumulated Chain CPU%')
plt.xlabel('TIME [s]')
plt.ylabel('CPU %')
plt.show()

###PLOT SUM OF CPU% FOR WORKERS###
ax1 = workers_enh.plot(kind='line',x='TIME',y='CPU %',color='red', label='Enhanced implementation')
ax2 = workers_ori.plot(kind='line',x='TIME',y='CPU %',color='blue', label='Original implementation', ax=ax1)
red = mpatches.Patch(color='red', label='Enhanced implementation')
blue = mpatches.Patch(color='blue', label='Original implementation')
plt.legend(handles=[red, blue])
plt.title('Sum of Workers CPU%')
plt.xlabel('TIME [s]')
plt.ylabel('CPU %')
plt.show()

###PLOT ACCUMULATED SUM OF CPU% FOR WORKERS###
ax1 = workers_enh.plot(kind='line',x='TIME',y='ACCUMULATED CPU %',color='red', label='Enhanced implementation')
ax2 = workers_ori.plot(kind='line',x='TIME',y='ACCUMULATED CPU %',color='blue', label='Original implementation', ax=ax1)
red = mpatches.Patch(color='red', label='Enhanced implementation')
blue = mpatches.Patch(color='blue', label='Original implementation')
plt.legend(handles=[red, blue])
plt.title('Accumulated Sum of Workers CPU%')
plt.xlabel('TIME [s]')
plt.ylabel('CPU %')
plt.show()

###PLOT MEM FOR REDIS###
ax1 = redis_enh.plot(kind='line',x='TIME',y='MEM USAGE / LIMIT',color='red', label='Enhanced implementation')
ax2 = redis_ori.plot(kind='line',x='TIME',y='MEM USAGE / LIMIT',color='blue', label='Original implementation', ax=ax1)
red = mpatches.Patch(color='red', label='Enhanced implementation')
blue = mpatches.Patch(color='blue', label='Original implementation')
plt.legend(handles=[red, blue])
plt.title('Redis Memory Usage')
plt.xlabel('TIME [s]')
plt.ylabel('MEMORY [MiB]')
plt.show()

###PLOT MEM FOR CHAIN###
ax1 = chain_enh.plot(kind='line',x='TIME',y='MEM USAGE / LIMIT',color='red', label='Enhanced implementation')
ax2 = chain_ori.plot(kind='line',x='TIME',y='MEM USAGE / LIMIT',color='blue', label='Original implementation', ax=ax1)
red = mpatches.Patch(color='red', label='Enhanced implementation')
blue = mpatches.Patch(color='blue', label='Original implementation')
plt.legend(handles=[red, blue])
plt.title('Chain Memory Usage')
plt.xlabel('TIME [s]')
plt.ylabel('MEMORY [MiB]')
plt.show()

###PLOT SUM OF MEM FOR WORKERS###
ax1 = workers_enh.plot(kind='line',x='TIME',y='MEM USAGE / LIMIT',color='red', label='Enhanced implementation')
ax2 = workers_ori.plot(kind='line',x='TIME',y='MEM USAGE / LIMIT',color='blue', label='Original implementation', ax=ax1)
red = mpatches.Patch(color='red', label='Enhanced implementation')
blue = mpatches.Patch(color='blue', label='Original implementation')
plt.legend(handles=[red, blue])
plt.title('Sum of Workers Memory Usage')
plt.xlabel('TIME [s]')
plt.ylabel('MEMORY [MiB]')
plt.show()

###PLOT ACCUMULATED SUM OF MEM FOR WORKERS
ax1 = workers_enh.plot(kind='line',x='TIME',y='ACCUMULATED MEM USAGE',color='red', label='Enhanced implementation')
ax2 = workers_ori.plot(kind='line',x='TIME',y='ACCUMULATED MEM USAGE',color='blue', label='Original implementation', ax=ax1)
red = mpatches.Patch(color='red', label='Enhanced implementation')
blue = mpatches.Patch(color='blue', label='Original implementation')
plt.legend(handles=[red, blue])
plt.title('Accumulated Sum of Workers Memory Usage')
plt.xlabel('TIME [s]')
plt.ylabel('MEMORY [MiB]')
plt.show()