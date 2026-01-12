#!/usr/bin/env python3
import pandas as pd
import argparse
import matplotlib.pyplot as plt

from colors import label_color

def shift_timestamp(df, offset):
    for i in range(len(df['timestamp'])):
        df.at[i, 'timestamp'] -= offset
        df.at[i, 'timestamp'] /= 1e3

def plot_figure(dataset1, dataset2, metric='time_total'):
    plt.plot(dataset1['timestamp'], dataset1[metric].rolling(20).mean(), label="Without ML", color=label_color["wml"]["color"])
    plt.plot(dataset2['timestamp'], dataset2[metric].rolling(20).mean(), label="With ML", color=label_color["ml"]["color"])
    plt.ylabel("time_total (seconds)")
    plt.xlabel('time (seconds)')
    #plt.title(f'Http {metric}')
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('http_metrics.png')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset1", help="First dataset to be extracted (NO ML)")
    parser.add_argument("dataset2", help="Second dataset to be extracted (WITH ML)")
    parser.add_argument("-m", "--metric", help="Metric to be compared in both datasets")



    args = parser.parse_args()
    df1 = pd.read_csv(args.dataset1)
    df2 = pd.read_csv(args.dataset2)
    metric = args.metric if args.metric else 'time_total'
    scenario = 'web'

    shift_timestamp(df1, df1['timestamp'][0])
    shift_timestamp(df2, df2['timestamp'][0])

    plot_figure(df1, df2, metric)
    print(df1)

if __name__ == '__main__':
    main()
