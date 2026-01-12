#!/usr/bin/env bash

mkdir graphs 2>/dev/null

NO_ML_WEB=$1
WITH_ML_WEB=$2

NO_ML_FILE=$3
WITH_ML_FILE=$4

NO_ML_VIDEO=$5
WITH_ML_VIDEO=$6

pushd graphs >/dev/null

../code/plot_acc.py ../code/accuracy.csv

../code/plot_classification_time.py ../${NO_ML_WEB}/telemetry.csv ../${WITH_ML_WEB}/telemetry.csv
mv classification_time.png forwarding_time_for_web.png
../code/plot_classification_time.py ../${NO_ML_FILE}/telemetry.csv ../${WITH_ML_FILE}/telemetry.csv
mv classification_time.png forwarding_time_for_file.png
../code/plot_classification_time.py ../${NO_ML_VIDEO}/telemetry.csv ../${WITH_ML_VIDEO}/telemetry.csv
mv classification_time.png forwarding_time_for_video.png

../code/plot_graphs.py -i ../${WITH_ML_WEB} ../${NO_ML_WEB}
mv iperf_kde_vazao_density.png iperf_kde_vazao_density_web.png
mv iperf_vazao_tempo.png iperf_vazao_tempo_web.png
../code/plot_graphs.py -i ../${WITH_ML_FILE} ../${NO_ML_FILE}
mv iperf_kde_vazao_density.png iperf_kde_vazao_density_file_transfer.png
mv iperf_vazao_tempo.png iperf_vazao_tempo_file_transfer.png
../code/plot_graphs.py -i ../${WITH_ML_VIDEO} ../${NO_ML_VIDEO}
mv iperf_kde_vazao_density.png iperf_kde_vazao_density_video.png
mv iperf_vazao_tempo.png iperf_vazao_tempo_video.png

../code/plot_sw_metrics.py ../${NO_ML_WEB}/system_metrics.csv ../${WITH_ML_WEB}/system_metrics.csv
mv sw_metrics_cpu_total.png sw_metrics_cpu_total_web.png
mv sw_metrics_mem_used.png sw_metrics_mem_used_web.png
../code/plot_sw_metrics.py ../${NO_ML_FILE}/system_metrics.csv ../${WITH_ML_FILE}/system_metrics.csv
mv sw_metrics_cpu_total.png sw_metrics_cpu_total_file.png
mv sw_metrics_mem_used.png sw_metrics_mem_used_file.png
../code/plot_sw_metrics.py ../${NO_ML_VIDEO}/system_metrics.csv ../${WITH_ML_VIDEO}/system_metrics.csv
mv sw_metrics_cpu_total.png sw_metrics_cpu_total_video.png
mv sw_metrics_mem_used.png sw_metrics_mem_used_video.png

# ../code/plot_sw_metrics.py -m mem_used ../${NO_ML_WEB}/system_metrics.csv ../${WITH_ML_WEB}/system_metrics.csv
# ../code/plot_sw_metrics.py -m mem_used ../${NO_ML_FILE}/system_metrics.csv ../${WITH_ML_FILE}/system_metrics.csv
# ../code/plot_sw_metrics.py -m mem_used ../${NO_ML_VIDEO}/system_metrics.csv ../${WITH_ML_VIDEO}/system_metrics.csv

../code/plot_http_metrics.py ../${NO_ML_WEB}/http_metrics.csv ../${WITH_ML_WEB}/http_metrics.csv
../code/plot_file_transfer_metrics.py ../${NO_ML_FILE}/flow_completion_time.csv ../${WITH_ML_FILE}/flow_completion_time.csv
../code/plot_ffmpeg_metrics.py ../${NO_ML_VIDEO}/video_metrics.csv ../${WITH_ML_VIDEO}/video_metrics.csv

popd >/dev/null
