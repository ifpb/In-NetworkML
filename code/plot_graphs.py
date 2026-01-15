#!/usr/bin/env python3

import argparse
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from colors import label_color


def extract_iperf(inputfile):
    with open(f"{inputfile}iperf.json") as f:
        lines = f.readlines()
        try:
            obj = json.loads("".join(lines))
        except json.JSONDecodeError:
            obj = json.loads("".join(lines[:-11]))
        lst = [x["sum"]["bits_per_second"] / 1e6 for x in obj["intervals"]]
    return lst


def plot_iperf(data, path):
    # plt.figure(figsize=(12, 6))
    plt.figure()
    sns.kdeplot(
        data["ML"],
        cumulative=True,
        linewidth=2,
        color=label_color["ml"]["color"],
        label=label_color["ml"]["name"],
    )
    sns.kdeplot(
        data["Sem ML"],
        cumulative=True,
        linewidth=2,
        color=label_color["wml"]["color"],
        label=label_color["wml"]["name"],
    )
    plt.ylabel("Density")
    plt.xlabel("Throughput (mbps)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{path}/iperf_kde_vazao_density.png", dpi=300, bbox_inches="tight")

    plt.figure()
    sns.lineplot(
        data["ML"].rolling(10).mean(),
        linewidth=2,
        color=label_color["ml"]["color"],
        label=label_color["ml"]["name"],
    )
    sns.lineplot(
        data["Sem ML"].rolling(10).mean(),
        linewidth=2,
        color=label_color["wml"]["color"],
        label=label_color["wml"]["name"],
    )
    plt.ylabel("Throughput (mbps)")
    plt.xlabel("Runtime (s)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{path}/iperf_vazao_tempo.png", dpi=300, bbox_inches="tight")


def main(args):
    data = pd.DataFrame()
    ml = extract_iperf(args.i[0])
    sml = extract_iperf(args.i[1])
    # print(len(ml), len(sml))
    qtd_linhas = min(len(ml), len(sml)) - 1
    data["ML"] = ml[:qtd_linhas]
    data["Sem ML"] = sml[:qtd_linhas]
    plt.rcParams.update({"font.size": 20})
    plot_iperf(data, "./")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", nargs="+", required=True, help="Path to metrics")

    args = parser.parse_args()

    main(args)
