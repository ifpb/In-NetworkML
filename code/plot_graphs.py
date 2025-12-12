#!/usr/bin/env python3

import json
import argparse

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def extract_iperf(inputfile):
    with open(f"{inputfile}iperf.json") as f:
        obj = json.load(f)
        lst = [x["sum"]["bits_per_second"] / 1e6 for x in obj["intervals"]]
    return lst

def plot_iperf(data, path):
    plt.figure(figsize=(12, 6))
    #sns.kdeplot(data, cumulative=True, linewidth=2) #label=data.columns)
    sns.lineplot(data.rolling(10).mean(), linewidth=2) #label=data.columns)
    #plt.xlabel('Tempo (s)')
    #plt.fill_between(data["ML"].index, data["ML"].rolling(1).mean(), alpha=0.2)
    plt.xlabel('Vazão (mbps)')
    #plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{path}/bits_per_second.png", dpi=300, bbox_inches='tight')


def main(args):
    data = pd.DataFrame()
    ml = extract_iperf(args.i[0])
    sml = extract_iperf(args.i[1])
    print(len(ml), len(sml))
    data["ML"] = ml
    data["Sem ML"] = sml
    plot_iperf(data, "./")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", nargs="+", required=True, help="Path to metrics")

    args = parser.parse_args()
    
    main(args)
