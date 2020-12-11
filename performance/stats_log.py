import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as collections


WORKER_NUM = sum(1 for line in open('../scenarios/local/trainers'))
SCHEME = "CPU"
STATS_CSV = "stats.csv"
LOG_FILE = "stats.log"

WORKER_NAMES = [f"worker{n}" for n in range(1, WORKER_NUM+1)]
SCHEME_MAP = {"CPU": "CPU %", "Memory": "MEM USAGE"}

AXS_MAP = {n: i for i, n in enumerate(WORKER_NAMES)}
COLOR_MAP = {"TRAINING_ROUND": "yellow", "AGGREGATION_ROUND": "green"}
STYLE_MAP = {"skip": "bo", "ignore": "ro"}

worker_dfs = {}

def preprocess():
    df = pd.read_csv(STATS_CSV, sep=',')
    df = df.loc[df['NAME']!='NAME']
    df.rename(columns={df.columns[4]: 'TIME' }, inplace = True)
    df = df.replace({'%':''}, regex=True)
    df.rename({'MEM USAGE / LIMIT':'MEM USAGE'}, axis=1, inplace=True)
    df['MEM USAGE'] = df['MEM USAGE'].str.split('M').str[0]
    df['MEM USAGE'] = df['MEM USAGE'].str.split('B').str[0]
    df['TIME'] = pd.to_datetime(df['TIME'], format=" %H:%M:%S")
    time_start = df['TIME'].iloc[0]
    df['TIME'] = ((df['TIME']-df['TIME'].iloc[0]).dt.total_seconds())
    df[['CPU %', 'MEM USAGE', 'MEM %']] = df[['CPU %', 'MEM USAGE', 'MEM %',]].apply(pd.to_numeric)
    return df, time_start

def parse_log(time_start):
    consensus_log, round_log = [], []
    with open(LOG_FILE, "r") as f:
        for l in f.readlines():
            if "ROUND" in l:
                round_log.append(l)
            elif "Consensus" in l:
                consensus_log.append(l)

    round_df = pd.DataFrame(map(lambda x: x.split(" "), round_log))[[0,4,6,7]]
    round_df.columns=["worker", "time", "phase", "round"]
    round_df['time'] = pd.to_datetime(round_df['time'], format="%H:%M:%S")
    round_df['time'] = ((round_df['time']-time_start).dt.total_seconds()) + 3600
    round_df['worker'] = round_df['worker'].str.split('m').str[-1]

    consensus_df = pd.DataFrame(map(lambda x: x.split(" "), consensus_log))[[0,5,9]]
    consensus_df.columns=["worker", "time", "type"]
    consensus_df['time'] = pd.to_datetime(consensus_df['time'], format="%H:%M:%S")
    consensus_df['time'] = ((consensus_df['time']-time_start).dt.total_seconds()) + 3600
    consensus_df['worker'] = consensus_df['worker'].str.split('m').str[-1]
    return round_df, consensus_df

def draw_stats(axs, scheme):
    for worker in WORKER_NAMES:
        worker_df = worker_dfs[worker]
        axs[AXS_MAP[worker]].plot(worker_df["TIME"], worker_df[SCHEME_MAP[scheme]])
        axs[AXS_MAP[worker]].get_yaxis().set_ticks([])
        axs[AXS_MAP[worker]].set_ylabel(worker, fontsize=15)
    axs[-1].set_xlabel("time (s)", fontsize=15)

    
def draw_round_span(r_df, axs):
    # generate span list
    round_span = []
    for worker in WORKER_NAMES:
        span_start = 0
        for _, r in r_df[r_df['worker'] == f"{worker}_1"].iterrows():
            round_span.append((worker, span_start, r.time, r["phase"]))
            span_start = r.time
    # draw spans
    for span in round_span:
        axs[AXS_MAP[span[0]]].axvspan(span[1], span[2], label=span[3], facecolor=COLOR_MAP[span[3]], alpha=0.2)

        
def draw_consensus_point(c_df, axs, scheme, target="worker"):
    # generate consensus point
    consensus_point = []
    for _, r in c_df.iterrows():
        worker = r["worker"].split("_")[0]
        worker_df = worker_dfs[worker]
        point = worker_df[worker_df["TIME"] < r.time].iloc[-1]
        skip_type = "skip" if r["type"].startswith("skip") else "ignore"
        consensus_point.append((worker, point["TIME"], point[SCHEME_MAP[scheme]], skip_type))
    # draw points
    for point in consensus_point:
        axs[AXS_MAP[point[0]]].plot(point[1], point[2], STYLE_MAP[point[3]], markersize=12, alpha=0.5)
        
def main():
    df, time_start = preprocess()
    group = df.groupby('NAME')
    chain_df = group.get_group('chain')
    for worker in WORKER_NAMES:
        _worker_df = group.get_group(f'local_{worker}_1')
        _worker_df.index = np.arange(0, len(_worker_df))
        worker_dfs[worker] = _worker_df

    round_df, consensus_df = parse_log(time_start)

    ## WORKER_PLOT
    worker_fig, worker_axs = plt.subplots(WORKER_NUM, 1, figsize=(15, 3*WORKER_NUM), sharex=True)
    worker_fig.subplots_adjust(hspace=0)
    worker_fig.suptitle(f'{SCHEME} usage of workers', fontsize=20, y=0.93)
    draw_stats(worker_axs, SCHEME)
    draw_round_span(round_df, worker_axs)
    draw_consensus_point(consensus_df, worker_axs, SCHEME)
    # plt.show()
    FIG_NOTE = input(f"Give a short name to specify this figure, '{SCHEME}_{WORKER_NUM}workers_[***].jpg': ")
    plt.savefig(f"{SCHEME}_{WORKER_NUM}workers_{FIG_NOTE}.jpg")

    ## CHAIN_PLOT
    chain_fig, chain_ax = plt.subplots(1, 1, figsize=(15, 5))
    chain_ax.plot(chain_df["TIME"], chain_df[SCHEME_MAP[SCHEME]])
    chain_ax.set_xlabel("time (s)", fontsize=15)
    chain_fig.suptitle(f'{SCHEME} usage of chain', fontsize=20, y=0.95)
    # round span
    round_span = []
    span_start = 0
    for i, r in round_df.groupby(["round", "phase"]).min("time").sort_values("time").iterrows():
        round_span.append((span_start, r.time, i[1]))
        span_start = r.time
    for span in round_span:
        chain_ax.axvspan(span[0], span[1], facecolor=COLOR_MAP[span[2]], alpha=0.2)
    # consensus points
    consensus_point = []
    for _, r in consensus_df.iterrows():
        point = chain_df[chain_df["TIME"] < r.time].iloc[-1]
        skip_type = "skip" if r["type"].startswith("skip") else "ignore"
        consensus_point.append((point["TIME"], point[SCHEME_MAP[SCHEME]], skip_type))
    for point in consensus_point:
        chain_ax.plot(point[0], point[1], STYLE_MAP[point[2]], label=point[2], markersize=12, alpha=0.5)
    plt.savefig(f"{SCHEME}_chain_{FIG_NOTE}.jpg")


if __name__ == "__main__":
    main()