name_mapping = {
    "sport": "srcPort",
    "dport": "dstPort",
    "tos": "diffserv",
    "length": "totalLen",
    "id": "identification",
    "ttl": "ttl",
    "chksum": "hdrChecksum",
    "seq": "seqNo",
    "ack": "ackNo",
    "window": "window",
}

type_mapping = {
    "srcPort": 16,
    "dstPort": 16,
    "diffserv": 8,
    "totalLen": 16,
    "identification": 16,
    "ttl": 8,
    "hdrChecksum": 16,
    "seqNo": 32,
    "ackNo": 32,
    "window": 16,
    "frame_size": 32,
    "ipi": 48,
}


def get_datatype(feature_name):
    if feature_name in type_mapping:
        return type_mapping[feature_name]

    translated = name_mapping.get(feature_name, feature_name)

    if translated in type_mapping:
        return type_mapping[translated]

    return None
