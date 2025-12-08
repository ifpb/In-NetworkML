#!/usr/bin/env python

import re
import time

from datatypes import get_datatype

inputfile = "./tree.txt"
actionfile = "./action.txt"


def find_action(textfile):
    action = []
    f = open(textfile)
    for line in f:
        n = re.findall(r"class", line)
        if n:
            fea = re.findall(r"\d", line)
            action.append(int(fea[1]))
    f.close()
    return action


def find_feature(textfile: str) -> dict[str, list[int]]:
    features = {}

    with open(textfile) as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if " = " not in line:
                break

            name, values_part = line.split("=", 1)
            name = name.strip()
            values = re.findall(r"\d+", values_part)

            if values:
                features[name] = [int(x) for x in values]

    return features


def find_classification(textfile: str, features: dict[str, list[int]]):
    rules = []

    with open(textfile, "r") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("when"):
                continue

            pattern = r"(\w+)\s*(<=|>)\s*(\d+(?:\.\d+)?)"
            conditions = re.findall(pattern, line)
            if not conditions:
                continue

            classification = re.findall(r"then\s+(\d+)", line)
            if not classification:
                continue
            classification = int(classification[0])

            feature_ranges = {}

            for feature in features.keys():
                feature_ranges[feature] = [k for k in range(len(features[feature]) + 1)]

            for fea, sign, num in conditions:
                if fea not in features:
                    continue

                thres = int(float(num))
                id = features[fea].index(thres)
                # Essa linha daqui ^, pode causar error
                # Se thres nao existir dentro de features[fea]

                if sign == "<=":
                    while id < len(features[fea]):
                        if id + 1 in feature_ranges[fea]:
                            feature_ranges[fea].remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature_ranges[fea]:
                            feature_ranges[fea].remove(id)
                        id = id - 1

            rules.append(
                {
                    "conditions": conditions,
                    "ranges": feature_ranges,
                    "classification": classification,
                }
            )

    return rules


def get_actionpara(action):
    para = {}
    if action == 0:
        para = {}
    elif action == 2:
        para = {"dstAddr": "00:00:00:02:02:00", "port": 2}
    elif action == 3:
        para = {"dstAddr": "00:00:00:03:03:00", "port": 3}
    elif action == 4:
        para = {"dstAddr": "00:00:00:04:04:00", "port": 4}

    return para


def writeactionrule(writer, ranges, action, result):
    command = f"table_add classify_exact {action} "
    for i in range(len(ranges)):
        command += f"{ranges[i][0]}->{ranges[i][1]} "
    command += f"=> {str(result)} 0\n"

    writer.write(command)
    print("add action rule")


def writefeatureXrule(writer, range, table, action, ind):
    print(range)
    print(ind)
    print(f"table_add {table} {action} {range[0]}->{range[1]} => {str(ind)}")
    writer.write(f"table_add {table} {action} {range[0]}->{range[1]} => {str(ind)} 0\n")
    print(f"add {table} rule")


def main():
    features = find_feature(inputfile)

    rules = find_classification(inputfile, features)

    action = find_action(actionfile)

    with open("table2.txt", "w") as f:
        for i in range(len(rules)):
            ranges = []

            for fea in features.keys():
                a = rules[i]["ranges"][fea]
                a = [a[0] + 1, a[-1] + 1]
                ranges.append(a)

            ind = int(rules[i]["classification"])
            ac = action[ind]

            print(ranges, "set_result", "IND:", ind, "AC:", ac)

            # if ac == 0:
            #    pass
            # else:
            writeactionrule(f, ranges, "set_result", ind)

        for idx, fea in enumerate(features.keys()):
            max_value = get_datatype(fea)
            if max_value is None:
                max_value = 48

            features[fea].append(0)
            features[fea].append(2**max_value - 1)
            features[fea].sort()
            for i in range(len(features[fea]) - 1):
                writefeatureXrule(
                    f,
                    features[fea][i : i + 2],
                    f"feature{idx+1}_exact",
                    f"set_actionselect{idx+1}",
                    i + 1,
                )


if __name__ == "__main__":
    start = time.time()

    # features = find_feature(inputfile)
    # for x in features.keys():
    #     print(x, "=", features[x])
    #
    # for rules in find_classification(inputfile, features):
    #     print(rules)

    main()

    end = time.time()
    print("time to load the tables:", end - start)
