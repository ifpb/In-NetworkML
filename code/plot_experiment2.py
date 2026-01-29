#!/usr/bin/env python3

import argparse

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

OUTPUT_PREFIX = "experiment2"


def plot_switch_cpu_total(dataset: pd.DataFrame):
    plt.figure(dpi=300)

    sns.boxplot(
        dataset,
        x="complexity",
        y="cpu_total",
        hue="complexity",
        palette="tab10",
        legend=False,
    )

    plt.ylabel("CPU Usage")
    plt.xlabel("Model complexity")
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_PREFIX}_cpu_usage.png")


def plot_switch_mem_used(dataset: pd.DataFrame):
    plt.figure(dpi=300)

    plt.yscale("log")

    dataset["mem_used"] = dataset["mem_used"] / 1024

    sns.boxplot(
        dataset,
        x="complexity",
        y="mem_used",
        hue="complexity",
        palette="tab10",
        legend=False,
    )

    plt.ylabel("Memory Usage (MB)")
    plt.xlabel("Model complexity")
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_PREFIX}_mem_used.png")


def plot_model_accuracy(dataset: pd.DataFrame):
    plt.figure(dpi=300)

    sns.boxplot(
        dataset,
        x="complexity",
        y="recall",
        hue="complexity",
        palette="tab10",
        legend=False,
    )

    plt.ylabel("Accuracy")
    plt.xlabel("Model complexity")
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_PREFIX}_accuracy.png")


def plot_dash_metrics_fps(dataset: pd.DataFrame):
    plt.figure(dpi=300)

    # sns.ecdfplot(
    #     dataset,
    #     x="frameRate",
    #     hue="complexity",
    #     palette="tab10",
    #     legend=False,
    # )

    depths = dataset["complexity"].unique()

    for depth in depths:
        subset = dataset[dataset["complexity"] == depth]
        sns.ecdfplot(
            data=subset,
            x="frameRate",
            label=str(depth),
        )

    plt.legend(
        # loc="upper center",
        title="Complexity",
        ncols=2,
        fontsize=14,
        title_fontsize=16,
    )

    plt.ylabel("Proportion")
    plt.xlabel("FrameRate (FPS)")
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_PREFIX}_dash_metrics_fps.png")


def plot_dash_metrics_bufferlevel(dataset: pd.DataFrame):
    plt.figure(dpi=300)

    # sns.ecdfplot(
    #     dataset,
    #     x="frameRate",
    #     hue="complexity",
    #     palette="tab10",
    #     legend=False,
    # )

    depths = dataset["complexity"].unique()

    for depth in depths:
        subset = dataset[dataset["complexity"] == depth]
        sns.ecdfplot(
            data=subset,
            x="bufferLevel",
            label=str(depth),
        )

    plt.legend(
        # loc="upper center",
        title="Complexity",
        ncols=2,
        fontsize=14,
        title_fontsize=16,
    )

    plt.ylabel("Proportion")
    plt.xlabel("BufferLevel (Seconds)")
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_PREFIX}_dash_metrics_bufferlevel.png")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dirs", nargs="+", help="Experiment result dirs", type=str)

    args = parser.parse_args()

    dash_metrics_column_names = [
        "time",
        "bufferLevel",
        "frameRate",
        "bitrate",
        "resolution",
        "calculatedBitrate",
    ]

    swm_dfs = []
    acc_dfs = []
    met_dfs = []

    for i, dir in enumerate(args.dirs):
        if not dir.endswith("/"):
            dir += "/"

        swm = pd.read_csv(f"{dir}system_metrics.csv")
        acc = pd.read_csv(f"{dir}dash_accuracy.csv")
        met = pd.read_csv(
            f"{dir}logs.txt",
            sep=";",
            header=None,
            names=dash_metrics_column_names,
            parse_dates=["time"],
        )

        swm["complexity"] = i + 1
        acc["complexity"] = i + 1
        met["complexity"] = i + 1

        swm_dfs.append(swm)
        acc_dfs.append(acc)
        met_dfs.append(met)

    df_swm = pd.concat(swm_dfs, ignore_index=True)
    df_acc = pd.concat(acc_dfs, ignore_index=True)
    df_met = pd.concat(met_dfs, ignore_index=True)

    df_swm = df_swm.dropna()
    df_acc = df_acc.dropna()
    df_met = df_met.dropna()

    plt.rcParams.update({"font.size": 20})

    plot_switch_cpu_total(df_swm)
    plot_switch_mem_used(df_swm)
    plot_model_accuracy(df_acc)
    plot_dash_metrics_fps(df_met)
    plot_dash_metrics_bufferlevel(df_met)


if __name__ == "__main__":
    main()
