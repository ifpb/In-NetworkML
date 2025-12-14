#!/usr/bin/env python3
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import numpy as np

def shift_timestamp(df, offset):
    for i in range(len(df['frame'])):
        df.at[i, 'frame'] -= offset


def numerize_speed(df):
    for i in range(len(df['speed'])):
        df.at[i, 'speed'] = np.float64(df.at[i, 'speed'][:-1])

def plot_figure(dataset1, dataset2, metric='fps'):
    plt.plot(dataset1['frame'], dataset1[metric], 'r', label="Without ML")
    plt.plot(dataset2['frame'], dataset2[metric], 'b', label="With ML")
    plt.ylabel(metric)
    plt.xlabel('frame')
    plt.title(f'FFMPEG {metric}')
    plt.legend()
    plt.savefig('ffmpeg_metrics.png')
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset1", help="First dataset to be extracted (NO ML)")
    parser.add_argument("dataset2", help="Second dataset to be extracted (WITH ML)")
    parser.add_argument("-m", "--metric", help="Metric to be compared in both datasets")
    


    args = parser.parse_args()
    df1 = pd.read_csv(args.dataset1)
    df2 = pd.read_csv(args.dataset2)
    metric = args.metric if args.metric else 'fps'

    shift_timestamp(df1, df1['frame'][0])
    shift_timestamp(df2, df2['frame'][0])
    numerize_speed(df1)
    numerize_speed(df2)

    plot_figure(df1, df2, metric)
    print(df1)

if __name__ == '__main__':
    main()
