#!/usr/bin/env python3
import pandas as pd
import argparse
import matplotlib.pyplot as plt

def shift_timestamp(df, offset):
    for i in range(len(df['timestamp'])):
        df.at[i, 'timestamp'] -= offset

def plot_figure(dataset1, dataset2):
    metric = 'flow_completion_time'
    plt.plot(dataset1['timestamp'], dataset1[metric], 'r', label="Without ML")
    plt.plot(dataset2['timestamp'], dataset2[metric], 'b', label="With ML")
    plt.ylabel(metric)
    plt.xlabel('Time (microsseconds)')
    plt.title(f'File Transfer {metric}')
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

    plot_figure(df1, df2)
    print(df1)

if __name__ == '__main__':
    main()
