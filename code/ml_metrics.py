#!/usr/bin/env python3

import os

import numpy as np

import argparse
import subprocess

from time import sleep
from pathlib import Path

script_dir = os.path.dirname(os.path.abspath(__file__))
cmatrix_path = f"{script_dir}/cmatrix"


def get_switch_results_counter(class_num: int) -> int:
    cmd = f"echo 'counter_read MyIngress.resultCounter {class_num}' | simple_switch_CLI | awk -F ' ' 'NR==4 {print $5}')"

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        try:
            return int(result.stdout.strip())
        except ValueError:
            return 0
    else:
        return 0



class Metrics:
    def __init__(self, initialMatrix=None):
        if initialMatrix:
            self.cmatrix = [list(x) for x in initialMatrix]
        else:
            self.cmatrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def update(self, y_true: int, curr_pred: list[int]):
        self.cmatrix[y_true] = curr_pred.copy()

    def get_metrics(self):
        #total = np.sum(self.cmatrix)

        #precision = np.nan_to_num(np.diag(self.cmatrix) / np.sum(self.cmatrix, axis=0))
        #recall = np.nan_to_num(np.diag(self.cmatrix) / np.sum(self.cmatrix, axis=1))
        #f1score = np.nan_to_num((2 * precision * recall) / (precision + recall))
        #accuracy = np.nan_to_num(np.trace(self.cmatrix) / total)

        total = sum(sum(x) for x in self.cmatrix)

        col_sums = [0] * len(self.cmatrix)
        for i in range(len(self.cmatrix)):
            for j in range(len(self.cmatrix)):
                col_sums[j] += self.cmatrix[i][j]

        row_sums = [sum(x) for x in self.cmatrix]

        diag = [self.cmatrix[i][i] for i in range(len(self.cmatrix))]

        precision = []
        recall = []
        f1score = []

        for i in range(len(self.cmatrix)):
            precision.append(
                    diag[i] / col_sums[i] if col_sums[i] != 0 else 0
                )

            recall.append(
                    diag[i] / row_sums[i] if row_sums[i] != 0 else 0
                )

            f1score.append(
               (2*precision[i] * recall[i]) / (precision[i] + recall[i]) if (precision[i] + recall[i] != 0) else 0
            )

        accuracy = sum(diag) / total if total != 0 else 0

        return {
            "precision": precision,
            "recall": recall,
            "f1score": f1score,
            "accuracy": accuracy,
        }

    def __str__(self) -> str:
        res = ""
        res += f"{ str(self.cmatrix) }\n"
        metrics = self.get_metrics()

        res += f"Precision: {metrics['precision']}\n"
        res += f"Recall: {metrics['recall']}\n"
        res += f"F1 Score: {metrics['f1score']}\n"
        res += f"Accuracy: {metrics['accuracy']}\n"

        return res


parser = argparse.ArgumentParser()

parser.add_argument("class", help="class name")

args = parser.parse_flags()

if args.class == "web":
    class_num = 0
elif args.class == "file_transfer":
    class_num = 1
elif args.class == "video":
    class_num = 2

try:
    cmatrix = []
    with open(cmatrix_path, "r") as f:
        for i, line in enumerate(f):
            line = line.strip()
            cmatrix.append(list(map(int, line.split())))
    metricas = Metrics(cmatrix)
except FileNotFoundError:
    print("ARQUIVO NAO ENCONTRADO")
    metricas = Metrics()

FILE=f"{script_dir}/accuracy.csv"

if not Path(FILE).is_file():
    with open(FILE, "w+") as f:
        f.write("precision_0, recall_0, f1score_0, precision_1, recall_1, f1score_1, precision_2, recall_2, f1score_2, accuracy\n")

with open(FILE, "a") as f:
    while True:
        pred = [get_switch_results_counter(x) for x in range(3)]
        if all(x == 0 for x in pred):
            continue

        metrics = metricas.get_metrics()

        for i in range(3):
            f.write(f"{metrics['precision'][i]:.3f},")
            f.write(f"{metrics['recall'][i]:.3f},")
            f.write(f"{metrics['f1score'][i]:.3f},")
        f.write(f"{metrics['accuracy']:.3f}")
        f.write("\n")
        sleep(1)
