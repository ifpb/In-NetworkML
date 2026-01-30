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
        x="n_features",
        y="cpu_total",
        hue="n_features",
        palette="tab10",
        legend=False,
    )

    plt.ylabel("CPU Usage")
    plt.xlabel("Model n_features")
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_PREFIX}_cpu_usage.png")


def plot_switch_mem_used(dataset: pd.DataFrame):
    plt.figure(dpi=300)

    #plt.yscale("log")

    dataset["mem_used"] = dataset["mem_used"] / 1024

    #dataset["mem_used"] = dataset["mem_used"] / 100

    sns.boxplot(
        dataset,
        x="n_features",
        y="mem_used",
        hue="n_features",
        palette="tab10",
        legend=False,
    )

    plt.ylabel("Memory Usage (MB)")
    plt.xlabel("Model n_features")
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_PREFIX}_mem_used.png")


def plot_model_accuracy(dataset: pd.DataFrame):
    plt.figure(dpi=300)

    sns.boxplot(
        dataset,
        x="n_features",
        y="recall",
        hue="n_features",
        palette="tab10",
        legend=False,
    )

    plt.ylabel("Accuracy")
    plt.xlabel("Model n_features")
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_PREFIX}_accuracy.png")


def plot_queue_delay(dataset: pd.DataFrame):
    plt.figure(dpi=300)

    sns.boxplot(
        dataset,
        x="n_features",
        y="deq_timedelta",
        hue="n_features",
        palette="tab10",
        legend=False,
    )

    plt.ylabel("Queue Delay")
    plt.xlabel("Model n_features")
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_PREFIX}_queue_delay.png")


def plot_dash_metrics_fps(dataset: pd.DataFrame):
    plt.figure(dpi=300)

    # sns.ecdfplot(
    #     dataset,
    #     x="frameRate",
    #     hue="n_features",
    #     palette="tab10",
    #     legend=False,
    # )

    depths = dataset["n_features"].unique()

    for depth in depths:
        subset = dataset[dataset["n_features"] == depth]
        sns.ecdfplot(
            data=subset,
            x="frameRate",
            label=str(depth),
        )

    plt.legend(
        # loc="upper center",
        title="N features",
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
    #     hue="n_features",
    #     palette="tab10",
    #     legend=False,
    # )

    depths = dataset["n_features"].unique()

    for depth in depths:
        subset = dataset[dataset["n_features"] == depth]
        sns.ecdfplot(
            data=subset,
            x="bufferLevel",
            label=str(depth),
        )

    plt.legend(
        # loc="upper center",
        title="N features",
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
    tel_dfs = []

    for i, dir in enumerate(args.dirs):
        if not dir.endswith("/"):
            dir += "/"

        swm = pd.read_csv(f"{dir}system_metrics.csv")
        acc = pd.read_csv(f"{dir}dash_accuracy.csv")
        tel = pd.read_csv(f"{dir}telemetry.csv")
        met = pd.read_csv(
            f"{dir}logs.txt",
            sep=";",
            header=None,
            names=dash_metrics_column_names,
            parse_dates=["time"],
        )

        swm["n_features"] = i * 2 + 2
        acc["n_features"] = i * 2 + 2
        met["n_features"] = i * 2 + 2
        tel["n_features"] = i * 2 + 2


        swm_dfs.append(swm)
        acc_dfs.append(acc)
        met_dfs.append(met)
        tel_dfs.append(tel)

    df_swm = pd.concat(swm_dfs, ignore_index=True)
    df_acc = pd.concat(acc_dfs, ignore_index=True)
    df_met = pd.concat(met_dfs, ignore_index=True)
    df_tel = pd.concat(tel_dfs, ignore_index=True)

    df_swm = df_swm.dropna()
    df_acc = df_acc.dropna()
    df_met = df_met.dropna()
    df_tel = df_tel.dropna()

    plt.rcParams.update({"font.size": 20})

    plot_switch_cpu_total(df_swm)
    plot_switch_mem_used(df_swm)
    plot_model_accuracy(df_acc)
    plot_dash_metrics_fps(df_met)
    plot_dash_metrics_bufferlevel(df_met)
    plot_queue_delay(df_tel)

if __name__ == "__main__":
    main()
