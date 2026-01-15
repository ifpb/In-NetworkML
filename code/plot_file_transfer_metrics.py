#!/usr/bin/env python3
import pandas as pd
import argparse
import matplotlib.pyplot as plt

from colors import label_color

def shift_timestamp(df, offset):
    for i in range(len(df['timestamp'])):
        df.at[i, 'timestamp'] -= offset
        df.at[i, 'timestamp'] /= 1e3

def plot_figure(dataset1, dataset2):
    plt.figure(dpi=300)
    metric = 'flow_completion_time'
    plt.plot(dataset1['timestamp'], dataset1[metric].rolling(10).mean(), label=label_color["wml"]["name"], color=label_color["wml"]["color"])
    plt.plot(dataset2['timestamp'], dataset2[metric].rolling(10).mean(), label=label_color["ml"]["name"], color=label_color["ml"]["color"])
    plt.ylabel("Flow Completion Time (seconds)")
    plt.xlabel('Runtime (seconds)')
    #plt.title(f'File Transfer {metric}')
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.legend()
    plt.savefig('file_transfer_metrics.png')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset1", help="First dataset to be extracted (NO ML)")
    parser.add_argument("dataset2", help="Second dataset to be extracted (WITH ML)")

    args = parser.parse_args()
    df1 = pd.read_csv(args.dataset1)
    df2 = pd.read_csv(args.dataset2)

    shift_timestamp(df1, df1['timestamp'][0])
    shift_timestamp(df2, df2['timestamp'][0])

    plt.rcParams.update({"font.size": 20})
    plot_figure(df1, df2)
    print(df1)

if __name__ == '__main__':
    main()
