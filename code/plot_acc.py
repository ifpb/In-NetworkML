#!/usr/bin/env python3
import argparse

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from colors import label_color


def shift_timestamp(df, offset):
    for i in range(len(df["timestamp"])):
        df.at[i, "timestamp"] -= offset


def plot_data(ax, data):
    classe = data["class"].unique()[0]
    ax.plot(data["timestamp"], data["precision"], label="Precision")
    ax.plot(data["timestamp"], data["recall"], label="Recall")
    ax.set_title(f"Classe {classe}")
    ax.set_xlabel("Time (seconds)")
    ax.legend()
    ax.grid()


def plot_figure(dataset):
    fig = plt.figure()

    grid = 231
    for v in dataset["class"].unique():
        ax = plt.subplot(grid)
        grid+=1
        d = dataset[dataset["class"] == v].reset_index(drop=True)
        shift_timestamp(d, d["timestamp"][0])
        plot_data(ax, d)

    ax = plt.subplot(212)
    shift_timestamp(dataset, dataset["timestamp"][0])
    ax.plot(dataset["accuracy"], label="Accuracy")
    ax.set_ylabel("Accuracy")
    ax.set_xlabel("Time (microsseconds)")
    ax.set_title("Accuracy over time")
    ax.legend()
    ax.grid()

    plt.tight_layout()
    plt.savefig("accuracy.png")

def plot_a(dataset):
    plt.figure(dpi=300)
    for v in dataset["class"].unique():
        d = dataset[dataset["class"] == v].reset_index(drop=True)
        shift_timestamp(d, d["timestamp"][0])
        plt.plot(d["timestamp"], d["recall"], label=label_color[str(v)]["name"], color=label_color[str(v)]["color"])

    #plt.axhline(y=dataset["recall"].mean(), color="tab:orange", linestyle="--", label="Média")
    plt.ylabel("Recall")
    plt.xlabel("Time (Seconds)")
    plt.tight_layout()
    plt.legend()
    plt.grid(alpha=0.3)

    plt.savefig("accuracy.png")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", help="dataset")

    args = parser.parse_args()
    df = pd.read_csv(args.dataset)

    plt.rcParams.update({"font.size": 16})
    plot_a(df)
    print(df)


if __name__ == "__main__":
    main()
