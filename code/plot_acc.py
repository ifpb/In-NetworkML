#!/usr/bin/env python3
import argparse

import matplotlib.pyplot as plt
import pandas as pd


def shift_timestamp(df, offset):
    for i in range(len(df["timestamp"])):
        df.at[i, "timestamp"] -= offset


def plot_figure(dataset):
    for v in dataset["class"].unique():
        d = dataset[dataset["class"] == v]
        shift_timestamp(d, d["timestamp"].iloc[0])
        plt.plot(d["timestamp"], d["recall"], label=f"Classe {v}")
    plt.ylabel("recall")
    plt.xlabel("Time (microsseconds)")
    plt.title("Recall over time")
    plt.legend()
    plt.savefig("accuracy.png")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", help="dataset")

    args = parser.parse_args()
    df = pd.read_csv(args.dataset)

    plot_figure(df)
    print(df)


if __name__ == "__main__":
    main()
