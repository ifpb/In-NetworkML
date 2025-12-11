#!/usr/bin/env python3

import os

script_dir = os.path.dirname(os.path.abspath(__file__))
cmatrix = []


with open(f'{script_dir}/cmatrix','r') as f:
    for i, line in enumerate(f):
        line = line.strip()
        cmatrix.append(list(map(int, line.split())))

classes = [0,1,2]
vpt = 0
precision_t = 0
recall_t = 0
f1score_t = 0
specificity_t = 0

results = {
        "classes": [],
    }

for c in classes:
    vp = vn = fp = fn = 0
    for i in range(len(cmatrix)):
        for j in range(len(cmatrix)):
            if (i == c):
                if (j == c):
                    vp += cmatrix[i][j]
                else:
                    fn += cmatrix[i][j]
            else:
                if (j == c):
                    fp += cmatrix[i][j]
                else:
                    vn += cmatrix[i][j]
    vpt += vp
    t = vp + vn + fp + fn

    precision = vp / (vp + fp)
    precision_t += precision

    recall = vp / (vp + fn)
    recall_t += recall

    specificity = fp / (fp + vn)
    specificity_t += specificity


    f1score = (2 * precision * recall) / (precision + recall)
    f1score_t += f1score

    results["classes"].append({
        "vp": vp,
        "vn": vn,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1score": f1score,
        "specificity": specificity,
    })

    print(f'CLASS {c}')
    print(f'Precision : {precision * 100:.3f}%')
    print(f'Recall : {recall * 100:.3f}%')
    print(f'F1 Score : {f1score:.3f}')
    print(f'Specificity : {specificity * 100:.3f}%\n')


precision_t /= 3
recall_t /= 3
f1score_t /= 3
specificity_t /= 3

results["cmatrix"] = cmatrix
results["accuracy"] = vpt/t
results["precision"] = precision_t
results["recall"] = recall_t
results["f1score"] = f1score_t
results["specificity"] = specificity_t

print('MACRO')
print(f'Accuracy: {(vpt/t)*100:.3f}%')
print(f'Precision Macro : {precision_t * 100:.3f}%')
print(f'Recall Macro : {recall_t * 100:.3f}%')
print(f'Specificity Macro : {specificity_t * 100:.3f}%')
print(f'F1 Score Macro : {f1score_t:.3f}')


import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
sns.heatmap(results["cmatrix"], annot=True, fmt='d', cmap='Blues',
            xticklabels=np.unique(classes),
            yticklabels=np.unique(classes))
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.show()

