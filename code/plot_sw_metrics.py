#!/usr/bin/env python3
import pandas as pd
import argparse
import matplotlib.pyplot as plt

import seaborn as sns

from colors import label_color

def shift_timestamp(df, offset):
    for i in range(len(df['timestamp'])):
        df.at[i, 'timestamp'] -= offset
        df.at[i, 'timestamp'] /= 1e3

def plot_figure(dataset1, dataset2, metric='cpu_total', scenario='undefined'):
    plt.figure(dpi=300)
    # plt.plot(dataset1['timestamp'], dataset1[metric], label="Without ML", color=label_color["wml"]["color"])
    # plt.plot(dataset2['timestamp'], dataset2[metric], label="With ML", color=label_color["ml"]["color"])

    dataset1["type"] = label_color["wml"]["name"]
    dataset2["type"] = label_color["ml"]["name"]

    dataset = pd.concat([dataset1[[metric, "type"]], dataset2[[metric, "type"]]])
    sns.boxplot(dataset, x="type", y=metric, hue="type")
    plt.ylabel(metric)
    plt.xlabel('Time (seconds)')
    #plt.title(f'Switch {metric} for {scenario}')
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.legend()
    plt.savefig(f'sw_metrics_{metric}.png')

def plot_figure_cpu_total(dataset1, dataset2, metric="cpu_total"):
    plt.figure(dpi=300)
    # plt.plot(dataset1['timestamp'], dataset1[metric], label="Without ML", color=label_color["wml"]["color"])
    # plt.plot(dataset2['timestamp'], dataset2[metric], label="With ML", color=label_color["ml"]["color"])

    dataset1["type"] = label_color["wml"]["name"]
    dataset2["type"] = label_color["ml"]["name"]

    dataset = pd.concat([dataset1[[metric, "type"]], dataset2[[metric, "type"]]])
    sns.boxplot(dataset, x="type", y=metric, hue="type")
    plt.ylabel("CPU Usage")
    plt.xlabel('Time (seconds)')
    #plt.title(f'Switch {metric} for {scenario}')
    plt.tight_layout()
    plt.grid(alpha=0.3)
    # plt.legend()
    plt.savefig(f'sw_metrics_{metric}.png')

def plot_figure_mem_used(dataset1, dataset2, metric='mem_used'):
    plt.figure(dpi=300)
    # plt.plot(dataset1['timestamp'], dataset1[metric], label="Without ML", color=label_color["wml"]["color"])
    # plt.plot(dataset2['timestamp'], dataset2[metric], label="With ML", color=label_color["ml"]["color"])

    dataset1["type"] = label_color["wml"]["name"]
    dataset2["type"] = label_color["ml"]["name"]

    # dataset1["mem_used"] = dataset1["mem_used"] / 1024
    # dataset2["mem_used"] = dataset2["mem_used"] / 1024

    dataset = pd.concat([dataset1[[metric, "type"]], dataset2[[metric, "type"]]])
    sns.boxplot(dataset, x="type", y=metric, hue="type")

    plt.yscale("log")

    plt.ylabel("Memory Used (KiB)")
    plt.xlabel('Time (seconds)')
    #plt.title(f'Switch {metric} for {scenario}')
    plt.tight_layout()
    plt.grid(alpha=0.3)
    # plt.legend()
    plt.savefig(f'sw_metrics_{metric}.png')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset1", help="First dataset to be extracted (NO ML)")
    parser.add_argument("dataset2", help="Second dataset to be extracted (WITH ML)")
    # parser.add_argument("-m", "--metric", help="Metric to be compared in both datasets")
    parser.add_argument("-s", "--scenario", help="Scenario in which the datasets were generated")



    args = parser.parse_args()
    df1 = pd.read_csv(args.dataset1)
    df2 = pd.read_csv(args.dataset2)
    # metric = args.metric if args.metric else 'cpu_total'
    scenario = args.scenario if args.scenario else 'undefined'

    shift_timestamp(df1, df1['timestamp'][0])
    shift_timestamp(df2, df2['timestamp'][0])

    plt.rcParams.update({"font.size": 16})
    plot_figure_cpu_total(df1, df2)
    plot_figure_mem_used(df1, df2)
    # plot_figure(df1, df2, "cpu_total", scenario)
    # plot_figure(df1, df2, "mem_used", scenario)
    print(df1)

if __name__ == '__main__':
    main()
