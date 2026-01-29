#!/usr/bin/env python3

import argparse

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

OUTPUT_PREFIX = "wave"


def plot_switch_cpu_total(dataset: pd.DataFrame):
    plt.figure(dpi=300)

    sns.lineplot(
        dataset,
        legend=False,
    )

    plt.ylabel("Client number")
    plt.xlabel("Time")
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_PREFIX}.png")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ds", help="Experiment result dirs", type=str)

    args = parser.parse_args()

    swm = pd.read_csv(args.ds)

    plt.rcParams.update({"font.size": 20})

    plot_switch_cpu_total(swm)


if __name__ == "__main__":
    main()
