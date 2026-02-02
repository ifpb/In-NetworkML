#!/usr/bin/env python3

import argparse
import json

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

OUTPUT_PREFIX = "experiment2"


def extract_iperf(inputfile):
    with open(f"{inputfile}iperf.json") as f:
        lines = f.readlines()
        try:
            obj = json.loads("".join(lines))
        except json.JSONDecodeError:
            obj = json.loads("".join(lines[:-11]))
        lst = [x["sum"]["bits_per_second"] / 1e6 for x in obj["intervals"]]
    return lst


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

    plt.ylabel("CPU Usage (%)")
    plt.xlabel("# of features")
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_PREFIX}_cpu_usage.png")


def plot_switch_mem_used(dataset: pd.DataFrame):
    plt.figure(dpi=300)

    # plt.yscale("log")

    dataset["mem_used"] = dataset["mem_used"] / 1024

    # dataset["mem_used"] = dataset["mem_used"] / 100

    sns.boxplot(
        dataset,
        x="n_features",
        y="mem_used",
        hue="n_features",
        palette="tab10",
        legend=False,
    )

    plt.ylabel("Memory Usage (MB)")
    plt.xlabel("# of features")
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_PREFIX}_mem_used.png")


def plot_model_accuracy(dataset: pd.DataFrame):
    plt.figure(dpi=300)

    sns.barplot(
        dataset.groupby(["n_features"]).tail(1),
        x="n_features",
        y="recall",
        hue="n_features",
        palette="tab10",
        legend=False,
    )

    # sns.boxplot(
    #     dataset,
    #     x="n_features",
    #     y="recall",
    #     hue="n_features",
    #     palette="tab10",
    #     legend=False,
    # )

    plt.ylabel("Accuracy")
    # plt.yticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    plt.xlabel("# of features")
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
    plt.xlabel("# features")
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_PREFIX}_queue_delay.png")


def plot_dash_metrics_fps(dataset: pd.DataFrame):
    plt.figure(dpi=300)

    counts = (
        dataset.groupby(["n_features", "frameRate"]).size().reset_index(name="count")
    )

    counts["total"] = counts.groupby("n_features")["count"].transform("sum")

    counts["percentage"] = (counts["count"] / counts["total"]) * 100

    sns.barplot(
        data=counts,
        x="n_features",
        y="percentage",
        hue="frameRate",
        palette="tab10",
    )

    # dataset["menor_que_30"] = dataset["frameRate"] < 30
    #
    # data = dataset.groupby("n_features")["menor_que_30"].mean().reset_index()
    # data["menor_que_30"] = data["menor_que_30"] * 100
    #
    # sns.barplot(
    #     data=data,
    #     x="n_features",
    #     # y="frameRate",
    #     y="menor_que_30",
    #     hue="n_features",
    #     palette="tab10",
    #     legend=False,
    # )

    plt.ylabel("Percentage (%)")
    plt.xlabel("# of features")
    plt.legend(
        title="Frame Rate (FPS)",
        fontsize=14,
        title_fontsize=16,
    )
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_PREFIX}_dash_metrics_fps.png")


def plot_dash_metrics_bufferlevel(dataset: pd.DataFrame):
    plt.figure(dpi=300)

    sns.boxplot(
        dataset,
        x="n_features",
        y="bufferLevel",
        hue="n_features",
        palette="tab10",
        legend=False,
    )

    # depths = dataset["n_features"].unique()

    # for depth in depths:
    #     subset = dataset[dataset["n_features"] == depth]
    #     sns.ecdfplot(
    #         data=subset,
    #         x="bufferLevel",
    #         label=str(depth),
    #     )

    # plt.legend(
    #     # loc="upper center",
    #     title="N features",
    #     ncols=2,
    #     fontsize=14,
    #     title_fontsize=16,
    # )

    plt.ylabel("BufferLevel (Seconds)")
    plt.xlabel("# of features")
    plt.tight_layout()
    plt.grid(alpha=0.3)
    plt.savefig(f"{OUTPUT_PREFIX}_dash_metrics_bufferlevel.png")


def plot_throughput(dataset):
    plt.figure(dpi=300)

    dataset["mbps_smoothed"] = dataset["mbps"].rolling(10).mean()

    sns.lineplot(
        data=dataset,
        x="runtime_s",
        y="mbps_smoothed",
        legend=False,
    )

    plt.ylabel("Throughput (mbps)")
    plt.xlabel("Runtime (s)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_PREFIX}_throughput.png")


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

    for i, dir in enumerate(args.dirs, 1):
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

    # 1. Read the raw tshark output
    tp_df = pd.read_csv(f"{args.dirs[-1]}throughput_raw.csv")

    # 2. Convert epoch to datetime
    tp_df["time"] = pd.to_datetime(tp_df["frame.time_epoch"], unit="s")

    # 3. Resample to 1-second intervals and sum the bytes
    #    We set 'time' as index strictly for resampling
    tp_df = tp_df.set_index("time")
    throughput_resampled = (
        tp_df["frame.len"].resample("1s").sum().to_frame(name="bytes")
    )

    # 4. Convert Bytes/sec to Mbps
    throughput_resampled["mbps"] = (throughput_resampled["bytes"] * 8) / 1_000_000

    # 5. Create a relative time column (0, 1, 2...) for plotting consistency
    #    We reset index to get 'time' back as a column, then calculate delta
    throughput_resampled = throughput_resampled.reset_index()
    start_time = throughput_resampled["time"].min()
    throughput_resampled["runtime_s"] = (
        throughput_resampled["time"] - start_time
    ).dt.total_seconds()

    df_tp = throughput_resampled.dropna()

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
    plot_throughput(df_tp)


if __name__ == "__main__":
    main()
