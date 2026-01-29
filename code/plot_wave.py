#!/usr/bin/env python3

import argparse

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

OUTPUT_PREFIX = "wave"


def plot_sine_wave(df: pd.DataFrame, lambd=20):
    plt.figure(dpi=300, figsize=(10,6))

    plt.plot(
        df,
        label="sinusoid load"
    )

    lambd_index = (df["0"] >= lambd).idxmax()

    df_max = df["0"].max()
    df_min = df.iloc[lambd_index:]["0"].min()

    # plot lambda
    plt.axhline(y=lambd, color="C1",linestyle="--", label="lambda")
    plt.axhline(y=df_max, color="C2",linestyle="--", label="maximum load")
    plt.axhline(y=df_min, color="C3", linestyle="--", label="minimum load")


    plt.legend(ncols=2)
    plt.yticks([0, 5, 10, 15, 20, 25, 30, 35, 40])
    plt.ylabel("Number of instances")
    plt.xticks([])
    plt.xlabel("Duration")
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_PREFIX}.png")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ds", help="Experiment result dirs", type=str)

    args = parser.parse_args()

    swm = pd.read_csv(args.ds)

    plt.rcParams.update({"font.size": 20})

    plot_sine_wave(swm)


if __name__ == "__main__":
    main()
