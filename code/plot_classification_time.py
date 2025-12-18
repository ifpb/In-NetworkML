#!/usr/bin/env python3
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import datetime
import numpy as np
import seaborn as sns

def time_to_seconds(time):
    pointers = list(map(float, time.split(':')))
    for i, mult in enumerate([360,60,1]):
        pointers[i]*=mult

    return sum(pointers)

def shift_timestamp(df, offset):
    print(offset)
    for i in range(len(df['timestamp'])):
        print(df.at[i, 'timestamp'])
        df.at[i, 'timestamp'] = time_to_seconds(df.at[i,'timestamp'].split('T')[1]) - offset

def insert_classification_time(df):
    ct = []
    for i in range(len(df['ingress_global_timestamp'])):
        ing = df.at[i,'ingress_global_timestamp']
        egr = df.at[i,'egress_global_timestamp'] 
        ct.append(egr-ing)

    return df.assign(classification_time=ct)



def plot_figure(dataset1, dataset2, metric='classfication_time', scenario='undefined'):
    plt.plot(dataset1['timestamp'], dataset1[metric].rolling(25).mean(), 'r', label="Without ML")
    plt.plot(dataset2['timestamp'], dataset2[metric].rolling(25).mean(), 'b', label="With ML")
    plt.ylabel(metric)
    plt.xlabel('time (seconds)')
    plt.title(f'Switch Forwarding time for {scenario}')
    plt.legend()
    plt.savefig('classification_time.png')
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset1", help="First dataset to be extracted (NO ML)")
    parser.add_argument("dataset2", help="Second dataset to be extracted (WITH ML)")
    parser.add_argument("-s", "--scenario", help="Scenario in which the datasets were generated")
    

    args = parser.parse_args()
    df1 = pd.read_csv(args.dataset1)
    df2 = pd.read_csv(args.dataset2)
    metric = 'classification_time'
    scenario = args.scenario if args.scenario else 'undefined'

    shift_timestamp(df1, time_to_seconds(df1['timestamp'][0].split('T')[1]))
    shift_timestamp(df2, time_to_seconds(df2['timestamp'][0].split('T')[1]))

    df1 = insert_classification_time(df1)
    df2 = insert_classification_time(df2)

    plot_figure(df1, df2, metric, scenario)
    print(df1)

if __name__ == '__main__':
    main()
