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
    seq = re.findall('\d+\.\d+', line)
    line = f.readline()
    ack = re.findall('\d+\.\d+', line)
    line = f.readline()
    window = re.findall('\d+\.\d+', line)
    line = f.readline()
    ipi = re.findall('\d+\.\d+', line)
    f.close
    seq = [float(i) for i in seq]
    ack = [float(i) for i in ack]
    window = [float(i) for i in window]
    ipi = [float(i) for i in ipi]
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
                thres = float(num[i][j])
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
                thres = float(num[i][j])
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
                thres = float(num[i][j])
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
                thres = float(num[i][j])
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


def writeactionrule(p4info_helper, switch, a, b, c, action, port):
    para = get_actionpara(port)
    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.ipv4_exact",
        match_fields={"meta.action_select1": a,
                      "meta.action_select2": b,
                      "meta.action_select3": c

                      },
        action_name=action,
        action_params=para
    )
    switch.WriteTableEntry(table_entry)
    print("Installed action rule on %s" % switch.name)


def writefeature1rule(p4info_helper, switch, range, ind):
    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.feature1_exact",
        match_fields={
            "hdr.ipv4.protocol": range},
        action_name="MyIngress.set_actionselect1",
        action_params={
            "featurevalue1": ind,
        })
    switch.WriteTableEntry(table_entry)
    print("Installed feature1 rule on %s" % switch.name)


def writefeature2rule(p4info_helper, switch, range, ind):
    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.feature2_exact",
        match_fields={
            "hdr.tcp.srcPort": range},
        action_name="MyIngress.set_actionselect2",
        action_params={
            "featurevalue2": ind,
        })
    switch.WriteTableEntry(table_entry)
    print("Installed feature2 rule on %s" % switch.name)


def writefeature3rule(p4info_helper, switch, range, ind):
    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.feature3_exact",
        match_fields={
            "hdr.tcp.dstPort": range},
        action_name="MyIngress.set_actionselect3",
        action_params={
            "featurevalue3": ind,
        })
    switch.WriteTableEntry(table_entry)
    print("Installed feature3 rule on %s" % switch.name)


def printGrpcError(e):
    print("gRPC Error:", e.details(), )
    status_code = e.code()
    print("(%s)" % status_code.name, )
    traceback = sys.exc_info()[2]
    print("[%s:%d]" % (traceback.tb_frame.f_code.co_filename, traceback.tb_lineno))


def main(p4info_file_path, bmv2_file_path):
    p4info_helper = p4runtime_lib.helper.P4InfoHelper(p4info_file_path)

    try:

        s1 = p4runtime_lib.bmv2.Bmv2SwitchConnection(
            name='s1',
            address='127.0.0.1:50051',
            device_id=0,
            proto_dump_file='logs/s1-p4runtime-requests.txt')

        s1.MasterArbitrationUpdate()

        s1.SetForwardingPipelineConfig(p4info=p4info_helper.p4info,
                                       bmv2_json_file_path=bmv2_file_path)
        print("Installed P4 Program using SetForwardingPipelineConfig on s1")

        for i in range(len(classfication)):
            a = protocol[i]
            id = len(a) - 1
            del a[1:id]
            if (len(a) == 1):
                a.append(a[0])
            b = srouce[i]
            id = len(b) - 1
            del b[1:id]
            if (len(b) == 1):
                b.append(b[0])
            c = dstination[i]
            id = len(c) - 1
            del c[1:id]
            if (len(c) == 1):
                c.append(c[0])

            ind = int(classfication[i])
            ac = action[ind]
            a = [i + 1 for i in a]
            b = [i + 1 for i in b]
            c = [i + 1 for i in c]

            if ac == 0:
                writeactionrule(p4info_helper, s1, a, b, c, "MyIngress.drop", 0)
            else:
                writeactionrule(p4info_helper, s1, a, b, c, "MyIngress.ipv4_forward", ac)
   

 
        if len(proto) != 0:
            proto.append(0)
            proto.append(32)
            proto.sort()
            for i in range(len(proto) - 1):
                writefeature1rule(p4info_helper, s1, proto[i:i + 2], i + 1)
        else:
            writefeature1rule(p4info_helper, s1, [0, 32], 1)

        if len(src) != 0:
            src.append(0)
            src.append(65535)
            src.sort()
            for i in range(len(src) - 1):
                writefeature2rule(p4info_helper, s1, src[i:i + 2], i + 1)
        if len(dst) != 0:
            dst.append(0)
            dst.append(65535)
            dst.sort()
            for i in range(len(dst) - 1):
                writefeature3rule(p4info_helper, s1, dst[i:i + 2], i + 1)

    except KeyboardInterrupt:
        print("Shutting down.")
    except grpc.RpcError as e:
        printGrpcError(e)

    ShutdownAllSwitchConnections()


if __name__ == '__main__':
    start = time.time()
    seq, ack, window, ipi = find_feature(inputfile)
    for x in (seq, ack, window, ipi):
        print(x)
    for i,x in enumerate(find_classification(inputfile, seq, ack, window, ipi)):
        print(i)
        print(x)

    #main()
    end = time.time()
    print("time to load the tables:", end-start)
