import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def read_file(filename):
    df = pd.read_csv(filename, sep=',')
    df = df.loc[df['NAME']!='NAME']
    df.rename(columns={df.columns[4]: 'TIME' }, inplace = True)
    df = df.replace({'%':''}, regex=True)
    df.rename({'MEM USAGE / LIMIT':'MEM USAGE'}, axis=1, inplace=True)
    df['MEM USAGE'] = df['MEM USAGE'].str.split('M').str[0]
    df['MEM USAGE'] = df['MEM USAGE'].str.split('B').str[0]
    df['TIME'] = df['TIME'].str[1:]
    df['TIME'] = pd.to_datetime(df['TIME'], format="%H:%M:%S.%f")
    df['TIME'] = ((df['TIME']-df['TIME'].iloc[0]).dt.total_seconds())
    df[['CPU %', 'MEM USAGE', 'MEM %']] = df[['CPU %', 'MEM USAGE', 'MEM %',]].apply(pd.to_numeric)
    return df

def split_data(df):
    group = df.groupby('NAME')
    redis = group.get_group('redis')
    chain = group.get_group('chain')
    worker1 = group.get_group('local_worker1_1')
    worker2 = group.get_group('local_worker2_1')
    worker3 = group.get_group('local_worker3_1')
    worker4 = group.get_group('local_worker4_1')
    worker5 = group.get_group('local_worker5_1')

    worker1.index = np.arange(1, len(worker1)+1)
    worker2.index = np.arange(1, len(worker2)+1)
    worker3.index = np.arange(1, len(worker3)+1)
    worker4.index = np.arange(1, len(worker4)+1)
    worker5.index = np.arange(1, len(worker5)+1)
    return redis, chain, worker1, worker2, worker3, worker4, worker5

def workers_calc(worker1, worker2, worker3, worker4, worker5):
    cpu = worker1['CPU %'] + worker2['CPU %'] + worker3['CPU %'] + worker4['CPU %'] + worker5['CPU %']
    mem = worker1['MEM USAGE'] + worker2['MEM USAGE'] + worker3['MEM USAGE'] + worker4['MEM USAGE'] + worker5['MEM USAGE']
    workers = pd.DataFrame(data={'CPU %': cpu, 'MEM USAGE': mem, 'TIME': worker1['TIME']})
    return workers

def accumulated_cpu_mem(df):
    df['ACCUMULATED CPU %'] = df['CPU %'].cumsum()
    df['ACCUMULATED MEM USAGE'] = df['MEM USAGE'].cumsum()
    return df

def container_mean(container1, container2, container3):
    container = pd.concat((container1, container2, container3))
    container = container.groupby(container.index)
    container = container.mean()
    return container

def time_sort(df1, df2):

    df = pd.DataFrame(columns=['CPU %', 'MEM USAGE', 'TIME'])

    i = 0
    j = 0
    i_bool = True
    j_bool = True
    while i_bool or j_bool:

        if (df1['TIME'].iloc[i] <= df2['TIME'].iloc[j] or j_bool is False) and i_bool is True:

            df = df.append({'CPU %' : df1['CPU %'].iloc[i], 'MEM USAGE' : df1['MEM USAGE'].iloc[i], 'TIME' : df1['TIME'].iloc[i]}, ignore_index=True)
            if i == len(df1)-1:
                i_bool = False
            else:
                i += 1

        elif (df2['TIME'].iloc[j] < df1['TIME'].iloc[i] or i_bool is False) and j_bool is True:

            df = df.append({'CPU %' : df2['CPU %'].iloc[j], 'MEM USAGE' : df2['MEM USAGE'].iloc[j], 'TIME' : df2['TIME'].iloc[j]}, ignore_index=True)
            if j == len(df2)-1:
                j_bool = False
            else:
                j += 1
        else:
            break

    return df

def two_line_plot(df_enh, df_ori, y_value, title):

    ax1 = df_enh.plot(kind='line',x='TIME',y=y_value,color='red', label='Enhanced implementation')
    ax2 = df_ori.plot(kind='line',x='TIME',y=y_value,color='blue', label='Original implementation', ax=ax1)
    red = mpatches.Patch(color='red', label='Enhanced implementation')
    blue = mpatches.Patch(color='blue', label='Original implementation')
    plt.legend(handles=[red, blue])
    plt.title(title)
    plt.xlabel('TIME [s]')

    if y_value == 'CPU %': 
        plt.ylabel(y_value)
    else :
        plt.ylabel('MEMORY [MiB]')
    
    plt.show()

def six_line_plot(df_enh1, df_enh2, df_enh3, df_ori1, df_ori2, df_ori3, y_value, title):

    ax1 = df_enh1.plot(kind='line',x='TIME',y=y_value,color='red', label='Enhanced implementation')
    ax2 = df_enh2.plot(kind='line',x='TIME',y=y_value,color='red', label='Original implementation', ax=ax1)
    ax3 = df_enh3.plot(kind='line',x='TIME',y=y_value,color='red', label='Original implementation', ax=ax1)
    ax4 = df_ori1.plot(kind='line',x='TIME',y=y_value,color='blue', label='Original implementation', ax=ax1)
    ax5 = df_ori2.plot(kind='line',x='TIME',y=y_value,color='blue', label='Original implementation', ax=ax1)
    ax6 = df_ori3.plot(kind='line',x='TIME',y=y_value,color='blue', label='Original implementation', ax=ax1)
    red = mpatches.Patch(color='red', label='Enhanced implementation')
    blue = mpatches.Patch(color='blue', label='Original implementation')
    plt.legend(handles=[red, blue])
    plt.title(title)
    plt.xlabel('TIME [s]')

    if y_value == 'CPU %': 
        plt.ylabel(y_value)
    else :
        plt.ylabel('MEMORY [MiB]')

    plt.show()

def main():

    ###READ CSV###
    df_enh1 = read_file('stats_project1.csv')
    df_enh2 = read_file('stats_project2.csv')
    df_enh3 = read_file('stats_project3.csv')
    df_ori1 = read_file('stats_felix1.csv')
    df_ori2 = read_file('stats_felix2.csv')
    df_ori3 = read_file('stats_felix3.csv')

    ###SPLIT THE DATA###
    redis_enh1, chain_enh1, worker1_enh1, worker2_enh1, worker3_enh1, worker4_enh1, worker5_enh1 = split_data(df_enh1)
    redis_enh2, chain_enh2, worker1_enh2, worker2_enh2, worker3_enh2, worker4_enh2, worker5_enh2 = split_data(df_enh2)
    redis_enh3, chain_enh3, worker1_enh3, worker2_enh3, worker3_enh3, worker4_enh3, worker5_enh3 = split_data(df_enh3)
    redis_ori1, chain_ori1, worker1_ori1, worker2_ori1, worker3_ori1, worker4_ori1, worker5_ori1 = split_data(df_ori1)
    redis_ori2, chain_ori2, worker1_ori2, worker2_ori2, worker3_ori2, worker4_ori2, worker5_ori2 = split_data(df_ori2)
    redis_ori3, chain_ori3, worker1_ori3, worker2_ori3, worker3_ori3, worker4_ori3, worker5_ori3 = split_data(df_ori3)

    ###MAKE CALCULATIONS FOR WORKERS###
    workers_enh1 = workers_calc(worker1_enh1, worker2_enh1, worker3_enh1, worker4_enh1, worker5_enh1)
    workers_enh2 = workers_calc(worker1_enh2, worker2_enh2, worker3_enh2, worker4_enh2, worker5_enh2)
    workers_enh3 = workers_calc(worker1_enh3, worker2_enh3, worker3_enh3, worker4_enh3, worker5_enh3)
    workers_ori1 = workers_calc(worker1_ori1, worker2_ori1, worker3_ori1, worker4_ori1, worker5_ori1)
    workers_ori2 = workers_calc(worker1_ori2, worker2_ori2, worker3_ori2, worker4_ori2, worker5_ori2)
    workers_ori3 = workers_calc(worker1_ori3, worker2_ori3, worker3_ori3, worker4_ori3, worker5_ori3)

    ###MERGE CPU% FOR REDIS IN ONE DATAFRAME AND CALCULATE ACCUMULATED CPU%###
    redis_enh = time_sort(redis_enh1, redis_enh2)
    redis_enh = time_sort(redis_enh, redis_enh3)
    redis_enh = accumulated_cpu_mem(redis_enh)

    redis_ori = time_sort(redis_ori1, redis_ori2)
    redis_ori = time_sort(redis_ori, redis_ori3)
    redis_ori = accumulated_cpu_mem(redis_ori)

    ###MERGE CPU% FOR CHAIN IN ONE DATAFRAME AND CALCULATE ACCUMULATED CPU%###
    chain_enh = time_sort(chain_enh1, chain_enh2)
    chain_enh = time_sort(chain_enh, chain_enh3)
    chain_enh = accumulated_cpu_mem(chain_enh)

    chain_ori = time_sort(chain_ori1, chain_ori2)
    chain_ori = time_sort(chain_ori, chain_ori3)
    chain_ori = accumulated_cpu_mem(chain_ori)

    ###MERGE WORKERS IN ONE DATAFRAME AND CALCULATE ACCUMULATED CPU% AND MEM###
    workers_enh = time_sort(workers_enh1, workers_enh2)
    workers_enh = time_sort(workers_enh, workers_enh3)
    print(workers_enh.head())
    workers_enh = accumulated_cpu_mem(workers_enh)
    print(workers_enh.head())

    workers_ori = time_sort(workers_ori1, workers_ori2)
    workers_ori = time_sort(workers_ori, workers_ori3)
    workers_ori = accumulated_cpu_mem(workers_ori)

    ###PLOT CPU% FOR ONE FOR REDIS###
    two_line_plot(redis_enh1, redis_ori1, 'CPU %', 'CPU% for Redis(one simulation)')

    ###PLOT CPU% FOR ALL THREE SIMULATIONS FOR REDIS###
    six_line_plot(redis_enh1, redis_enh2, redis_enh3, redis_ori1, redis_ori2, redis_ori3, 'CPU %', 'Redis CPU % (six workers)')

    ###PLOT ACCUMULATED CPU% FOR REDIS###
    two_line_plot(redis_enh, redis_ori, 'ACCUMULATED CPU %', 'Accumulated CPU% for Redis (three simulations)')

    ###PLOT CPU% FOR CHAIN###
    two_line_plot(chain_enh1, chain_ori1, 'CPU %', 'CPU% for Chain (one simulation)')

    ###PLOT ACCUMULATED CPU% FOR CHAIN###
    two_line_plot(chain_enh, chain_ori, 'ACCUMULATED CPU %', 'Accumulated CPU% for Chain (three simulations)')

    ###PLOT SUM OF CPU% FOR WORKERS###
    two_line_plot(workers_enh1, workers_ori1, 'CPU %', 'Sum of Worker CPU % (one simulation)')

    ###PLOT ACCUMULATED SUM OF CPU% FOR WORKERS###
    two_line_plot(workers_enh, workers_ori, 'ACCUMULATED CPU %', 'Accumulated Sum of Workers (three simulations)')

    ###PLOT MEM FOR REDIS###
    two_line_plot(redis_enh1, redis_ori1, 'MEM USAGE', 'Memory Usage for Redis(one simulation)')

    ###PLOT ACCUMULATED MEM FOR REDIS###
    two_line_plot(redis_enh, redis_ori, 'ACCUMULATED MEM USAGE', 'Accumulated Memory Usage for Redis (three simulations)')

    ###PLOT MEM FOR CHAIN###
    two_line_plot(chain_enh1, chain_ori1, 'MEM USAGE', 'Memory Usage for Chain (one simulation)')

    ###PLOT ACCUMULATED MEM FOR CHAIN###
    two_line_plot(chain_enh, chain_ori, 'ACCUMULATED MEM USAGE', 'Accumulated Memory Usage for Chain (three simulations)')

    ###PLOT SUM OF MEM FOR WORKERS###
    two_line_plot(workers_enh1, workers_ori1, 'MEM USAGE', 'Sum of Workers Memory Usage (one simulation)')

    ###PLOT SUM OF ACCUMULATED MEM FOR WORKERS###
    two_line_plot(workers_enh, workers_ori, 'ACCUMULATED MEM USAGE', 'Accumulated Sum of Workers Memory Usage (three simulations)')

if __name__ == "__main__":
    main()