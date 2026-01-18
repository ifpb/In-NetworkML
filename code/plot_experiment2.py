#!/usr/bin/env python3

import argparse

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

OUTPUT_PREFIX = "experiment2"


def plot_switch_cpu_total(dataset: pd.DataFrame):
    plt.figure(dpi=300)

    sns.boxplot(dataset)

    plt.ylabel("CPU Usage")
    plt.xlabel("Model complexity")
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_PREFIX}_cpu_usage.png")


def plot_switch_mem_used(dataset: pd.DataFrame):
    plt.figure(dpi=300)

    plt.yscale("log")

    sns.boxplot(dataset)

    plt.ylabel("Memory Usage (KiB)")
    plt.xlabel("Model complexity")
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_PREFIX}_mem_used.png")


def plot_model_accuracy(dataset: pd.DataFrame):
    plt.figure(dpi=300)

    sns.boxplot(dataset)

    plt.ylabel("Accuracy")
    plt.xlabel("Model complexity")
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_PREFIX}_accuracy.png")


def plot_dash_metrics(dataset: pd.DataFrame):
    plt.figure(dpi=300)

    sns.boxplot(dataset)

    plt.ylabel("FrameRate (FPS)")
    plt.xlabel("Model complexity")
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_PREFIX}_dash_metrics.png")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dirs", nargs="+", help="Experiment result dirs", type=str)

    args = parser.parse_args()
    df_cpu = pd.DataFrame()
    df_mem = pd.DataFrame()
    df_acc = pd.DataFrame()
    df_met = pd.DataFrame()

    dash_metrics_column_names = [
        "time",
        "bufferLevel",
        "frameRate",
        "bitrate",
        "resolution",
        "calculatedBitrate",
    ]

    for i, dir in enumerate(args.dirs):
        if not dir.endswith("/"):
            dir += "/"

        swm = pd.read_csv(f"{dir}system_metrics.csv")
        acc = pd.read_csv(f"{dir}dash_accuracy.csv")
        met = pd.read_csv(
            f"{dir}logs.txt", sep=";", header=None, names=dash_metrics_column_names
        )

        df_cpu[i + 1] = swm["cpu_total"]
        df_mem[i + 1] = swm["mem_used"]

        df_acc[i + 1] = acc["recall"]

        df_met[i + 1] = met["frameRate"]

    df_cpu = df_cpu.dropna()
    df_mem = df_mem.dropna()
    df_acc = df_acc.dropna()
    df_met = df_met.dropna()

    plt.rcParams.update({"font.size": 20})

    plot_switch_cpu_total(df_cpu)
    plot_switch_mem_used(df_mem)
    plot_model_accuracy(df_acc)
    plot_dash_metrics(df_met)


if __name__ == "__main__":
    main()
