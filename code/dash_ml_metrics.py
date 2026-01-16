#!/usr/bin/env python3

import argparse
import os
import signal
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from time import sleep

script_dir = os.path.dirname(os.path.abspath(__file__))
cmatrix_path = "{}/dash_cmatrix".format(script_dir)


def get_switch_results_counter(class_num):
    echo_cmd = ["echo", "counter_read MyIngress.resultCounter {}".format(class_num)]
    s_CLI_cmd = ["simple_switch_CLI"]
    awk_cmd = ["awk", "-F", " ", "NR==4 {{print $5}}"]

    try:
        echo_res = subprocess.Popen(echo_cmd, stdout=subprocess.PIPE)
        s_cli_res = subprocess.Popen(
            s_CLI_cmd, stdin=echo_res.stdout, stdout=subprocess.PIPE
        )
        awk_res = subprocess.Popen(
            awk_cmd, stdin=s_cli_res.stdout, stdout=subprocess.PIPE
        )

        result, _ = awk_res.communicate()
    except KeyboardInterrupt:
        sys.exit(0)

    try:
        return int(result.strip())
    except ValueError:
        return 0


def handle_exit(sig, frame):
    with open(cmatrix_path, "w") as f:
        for linha in metricas.cmatrix:
            f.write(" ".join(map(str, linha)))
            f.write("\n")

    sys.exit(0)


class Metrics:
    def __init__(self, initialMatrix=None):
        if initialMatrix:
            if len(initialMatrix) != 4 or any(len(x) != 4 for x in initialMatrix):
                raise ValueError("Matriz não é 4x4")
            self.cmatrix = [list(x) for x in initialMatrix]
        else:
            self.cmatrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    def update(self, y_true, curr_pred):
        if y_true < 0 or y_true > 3:
            raise ValueError("y_true precisa ser 0, 1, 2 ou 3")
        if len(curr_pred) != 4:
            raise ValueError("curr_pred precisa ser de tamanho 4")

        self.cmatrix[y_true] = curr_pred.copy()

    def get_metrics(self):
        # total = np.sum(self.cmatrix)

        # precision = np.nan_to_num(np.diag(self.cmatrix) / np.sum(self.cmatrix, axis=0))
        # recall = np.nan_to_num(np.diag(self.cmatrix) / np.sum(self.cmatrix, axis=1))
        # f1score = np.nan_to_num((2 * precision * recall) / (precision + recall))
        # accuracy = np.nan_to_num(np.trace(self.cmatrix) / total)

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
            precision.append(diag[i] / col_sums[i] if col_sums[i] != 0 else 0)

            recall.append(diag[i] / row_sums[i] if row_sums[i] != 0 else 0)

            f1score.append(
                (2 * precision[i] * recall[i]) / (precision[i] + recall[i])
                if (precision[i] + recall[i] != 0)
                else 0
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
        res += "{}\n".format(str(self.cmatrix))
        metrics = self.get_metrics()

        res += "Precision: {}\n".format(metrics["precision"])
        res += "Recall: {}\n".format(metrics["recall"])
        res += "F1 Score: {}\n".format(metrics["f1score"])
        res += "Accuracy: {}\n".format(metrics["accuracy"])

        return res


parser = argparse.ArgumentParser()

parser.add_argument("class_name", help="class name")
parser.add_argument("output_dir", help="output dir")

args = parser.parse_args()

if args.class_name == "web":
    class_num = 0
elif args.class_name == "file_transfer":
    class_num = 1
elif args.class_name == "video":
    class_num = 2
elif args.class_name == "dash":
    class_num = 3
else:
    raise ValueError("Nome de classe invalido")

### Salva a cmatrix antes de fechar ###
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

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

FILE = "{}/dash_accuracy.csv".format(args.output_dir)

if not Path(FILE).is_file():
    with open(FILE, "w+") as f:
        f.write(
            # "precision_0,recall_0,f1score_0,precision_1,recall_1,f1score_1,precision_2,recall_2,f1score_2,accuracy\n"
            "timestamp,class,precision,recall,f1score,accuracy\n"
        )

with open(FILE, "a") as f:
    while True:
        sleep(1)
        pred = [get_switch_results_counter(x) for x in range(4)]
        if all(x == 0 for x in pred):
            continue

        metricas.update(class_num, pred)

        metrics = metricas.get_metrics()

        f.write("{},".format(datetime.now().timestamp()))

        # for i in range(3):
        #     f.write("{},".format(metrics["precision"][i]))
        #     f.write("{},".format(metrics["recall"][i]))
        #     f.write("{},".format(metrics["f1score"][i]))
        f.write("{},".format(class_num))
        f.write("{},".format(metrics["precision"][class_num]))
        f.write("{},".format(metrics["recall"][class_num]))
        f.write("{},".format(metrics["f1score"][class_num]))
        f.write("{}".format(metrics["accuracy"]))
        f.write("\n")
