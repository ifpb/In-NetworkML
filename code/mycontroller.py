#!/usr/bin/env python

import re
import time

inputfile = './tree.txt'
actionfile = './action.txt'

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


def find_feature(textfile):
    f = open(textfile)
    line = f.readline()
    seq = re.findall(r"\d+", line)
    line = f.readline()
    ack = re.findall(r"\d+", line)
    line = f.readline()
    window = re.findall(r"\d+", line)
    line = f.readline()
    ipi = re.findall(r"\d+", line)
    f.close
    seq = [int(i) for i in seq]
    ack = [int(i) for i in ack]
    window = [int(i) for i in window]
    ipi = [int(i) for i in ipi]
    return seq, ack, window, ipi

def find_classification(textfile, fseq, fack, fwindow, fipi):
    fea = []
    sign = []
    num = []
    f = open(textfile, 'r')
    for line in f:
        n = re.findall(r"when", line)
        if n:
            fea.append(re.findall(r"(seq|ack|window|ipi)", line))
            sign.append(re.findall(r"(<=|>)", line))
            num.append(re.findall(r"\d+\.?\d*", line))
    f.close()

    seq = []
    ack = []
    window = []
    ipi = []
    classfication = []

    for i in range(len(fea)):
        feature1 = [k for k in range(len(fseq) + 1)]
        feature2 = [k for k in range(len(fack) + 1)]
        feature3 = [k for k in range(len(fwindow) + 1)]
        feature4 = [k for k in range(len(fipi) + 1)]
        for j, feature in enumerate(fea[i]):
            if feature == 'seq':
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = fseq.index(thres)
                if sig == '<=':
                    while id < len(fseq):
                        if id + 1 in feature1:
                            feature1.remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature1:
                            feature1.remove(id)
                        id = id - 1
            elif feature == 'ack':
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = fack.index(thres)
                if sig == '<=':
                    while id < len(fack):
                        if id + 1 in feature2:
                            feature2.remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature2:
                            feature2.remove(id)
                        id = id - 1
            elif feature == "window":
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = fwindow.index(thres)
                if sig == '<=':
                    while id < len(fwindow):
                        if id + 1 in feature3:
                            feature3.remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature3:
                            feature3.remove(id)
                        id = id - 1
            elif feature == "ipi":
                sig = sign[i][j]
                thres = int(float(num[i][j]))
                id = fipi.index(thres)
                if sig == '<=':
                    while id < len(fipi):
                        if id + 1 in feature4:
                            feature4.remove(id + 1)
                        id = id + 1
                else:
                    while id >= 0:
                        if id in feature4:
                            feature4.remove(id)
                        id = id - 1
        seq.append(feature1)
        ack.append(feature2)
        window.append(feature3)
        ipi.append(feature4)
        a = len(num[i])
        classfication.append(num[i][a - 1])
    return (seq, ack, window, ipi, classfication)

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

def writeactionrule(writer, a, b, c, d, action, result):
    print([a, b, c, d])
    print("Action",action)
    print(f"table_add classify_exact {action} {a[0]}->{a[1]} {b[0]}->{b[1]} {c[0]}->{c[1]} {d[0]}->{d[1]} => {str(result)} 0")
    writer.write(f"table_add classify_exact {action} {a[0]}->{a[1]} {b[0]}->{b[1]} {c[0]}->{c[1]} {d[0]}->{d[1]} => {str(result)} 0\n")
    print("add action rule")

def writefeatureXrule(writer, range, table, action, ind):
    print(range)
    print(ind)
    print(f"table_add {table} {action} {range[0]}->{range[1]} => {str(ind)}")
    writer.write(f"table_add {table} {action} {range[0]}->{range[1]} => {str(ind)} 0\n")
    print(f"add {table} rule")

def main():
    seq, ack, window, ipi = find_feature(inputfile)
    print("all features: \n")
    print(seq)
    print(ack)
    print(window)
    print(ipi)

    seq_values, ack_values, window_values, ipi_values, classification = find_classification(inputfile, seq, ack, window, ipi)

    print("all classification: \n")
    print(seq_values)
    print(ack_values)
    print(window_values)
    print(ipi_values)


    action = find_action(actionfile)
    print(f"action = {action}\n")

    with open("table2.txt", "w") as f:
        for i in range(len(classification)):
            a = seq_values[i]
            #print(type(a), a)
            id = len(a) - 1
            del a[1:id]
            if len(a) == 1:
                a.append(a[0])
            b = ack_values[i]
            id = len(b) - 1
            del b[1:id]
            if len(b) == 1:
                b.append(b[0])
            c = window_values[i]
            id = len(c) - 1
            del c[1:id]
            if len(c) == 1:
                c.append(c[0])
            d = ipi_values[i]
            id = len(d) - 1
            del d[1:id]
            if len(d) == 1:
                d.append(d[0])

            ind = int(classification[i])
            ac = action[ind]
            a = [i + 1 for i in a]
            b = [i + 1 for i in b]
            c = [i + 1 for i in c]
            d = [i + 1 for i in d]

            print(a, b, c, d, "set_result", "IND:", ind, "AC:",ac )

            #if ac == 0:
            #    pass
            #else:
            writeactionrule(f, a, b, c, d, 'set_result', ind)

        # for feature1 table
        if len(seq) != 0:
            seq.append(0)
            seq.append(2 ** 32 -1)
            seq.sort()
            for i in range(len(seq) - 1):
                writefeatureXrule(f, seq[i:i + 2], "feature1_exact", "set_actionselect1", i+1)
        else:
            writefeatureXrule(f, [0, 2 ** 32 -1], "feature1_exact", "set_actionselect1", 1)


        # for feature2 table
        if len(ack) != 0:
            ack.append(0)
            ack.append(2 ** 32 -1)
            ack.sort()
            for i in range(len(ack) - 1):
                writefeatureXrule(f, ack[i:i + 2], "feature2_exact", "set_actionselect2", i+1)
        else:
            writefeatureXrule(f, [0, 2 ** 32 -1], "feature2_exact", "set_actionselect2", 1)

        # for feature3 table
        if len(window) != 0:
            window.append(0)
            window.append(2 ** 16 -1)
            window.sort()
            for i in range(len(window) - 1):
                writefeatureXrule(f, window[i:i + 2], "feature3_exact", "set_actionselect3", i+1)
        else:
            writefeatureXrule(f, [0, 2 ** 16 -1], "feature3_exact", "set_actionselect3", 1)


        # for feature4 table (ifi)
        if len(ipi) != 0:
            ipi.append(0)
            ipi.append(2 ** 48 -1)
            ipi.sort()
            for i in range(len(ipi) - 1):
                writefeatureXrule(f, ipi[i:i + 2], "feature4_exact", "set_actionselect4", i+1)
        else:
            writefeatureXrule(f, [0, 2 ** 48 -1], "feature4_exact", "set_actionselect4", 1)


if __name__ == '__main__':
    start = time.time()
    seq, ack, window, ipi = find_feature(inputfile)
    for x in (seq, ack, window, ipi):
        print(x)
    for i,x in enumerate(find_classification(inputfile, seq, ack, window, ipi)):
        print(i)
        print(x)

    main()
    end = time.time()
    print("time to load the tables:", end-start)
