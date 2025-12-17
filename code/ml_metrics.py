#!/usr/bin/env python3

import os

import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))
cmatrix_path = f"{script_dir}/cmatrix"


class Metrics:
    def __init__(self, initalMatrix=None):
        if initalMatrix:
            self.cmatrix = np.array(initalMatrix, dtype=int)
        else:
            self.cmatrix = np.zeros((3, 3), dtype=int)

    def update(self, y_true: int, curr_pred: list[int]):
        self.cmatrix[y_true] = curr_pred

    def get_metrics(self):
        total = np.sum(self.cmatrix)

        precision = np.nan_to_num(np.diag(self.cmatrix) / np.sum(self.cmatrix, axis=0))
        recall = np.nan_to_num(np.diag(self.cmatrix) / np.sum(self.cmatrix, axis=1))
        f1score = np.nan_to_num((2 * precision * recall) / (precision + recall))
        accuracy = np.nan_to_num(np.trace(self.cmatrix) / total)

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

print(str(metricas))
