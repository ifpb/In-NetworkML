#!/usr/bin/env python3
import pandas as pd
import argparse
import matplotlib.pyplot as plt

def shift_timestamp(df, offset):
    for i in range(len(df['timestamp'])):
        df.at[i, 'timestamp'] -= offset

def plot_figure(dataset1, dataset2, metric='cpu_total', scenario='undefined'):
    plt.plot(dataset1['timestamp'], dataset1[metric], 'r', label="Without ML")
    plt.plot(dataset2['timestamp'], dataset2[metric], 'b', label="With ML")
    plt.ylabel(metric)
    plt.xlabel('time (microsseconds)')
    plt.title(f'Switch {metric} for {scenario}')
    plt.legend()
    plt.savefig('sw_metrics.png')
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset1", help="First dataset to be extracted (NO ML)")
    parser.add_argument("dataset2", help="Second dataset to be extracted (WITH ML)")
    parser.add_argument("-m", "--metric", help="Metric to be compared in both datasets")
    parser.add_argument("-s", "--scenario", help="Scenario in which the datasets were generated")
    


    args = parser.parse_args()
    df1 = pd.read_csv(args.dataset1)
    df2 = pd.read_csv(args.dataset2)
    metric = args.metric if args.metric else 'cpu_total'
    scenario = args.scenario if args.scenario else 'undefined'

    shift_timestamp(df1, df1['timestamp'][0])
    shift_timestamp(df2, df2['timestamp'][0])

    plot_figure(df1, df2, metric, scenario)
    print(df1)

if __name__ == '__main__':
    main()
