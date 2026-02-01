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
    "flags": "flags",
    "frag": "fragOffset",
    "ihl": "ihl",
    "proto": "protocol",
    "dataofs": "dataOffset",
    "urgptr": "urgentPtr",
    "reserved": "reserved",
    "chksum_tcp": "tcpChecksum",
    "urg": "urgFlag",
    "ece": "eceFlag",
    "cwr": "cwrFlag",
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
    "flags": 3,
    "fragOffset": 13,
    "ihl": 4,
    "protocol": 8,
    "dataOffset": 4,
    "urgentPtr": 16,
    "reserved": 3,
    "tcpChecksum": 16,
    "urgFlag": 1,
    "eceFlag": 1,
    "cwrFlag": 1,
    "payload_length": 16,
}

source_mapping = {
    "srcPort": "hdr.tcp.srcPort",
    "dstPort": "hdr.tcp.dstPort",
    "diffserv": "hdr.ipv4.diffserv",
    "totalLen": "hdr.ipv4.totalLen",
    "identification": "hdr.ipv4.identification",
    "ttl": "hdr.ipv4.ttl",
    "hdrChecksum": "hdr.ipv4.hdrChecksum",
    "seqNo": "hdr.tcp.seqNo",
    "ackNo": "hdr.tcp.ackNo",
    "window": "hdr.tcp.window",
    "frame_size": "standard_metadata.packet_length",
    "flags": "hdr.ipv4.flags",
    "fragOffset": "hdr.ipv4.fragOffset",
    "ihl": "hdr.ipv4.ihl",
    "protocol": "hdr.ipv4.protocol",
    "dataOffset": "hdr.tcp.dataOffset",
    "urgentPtr": "hdr.tcp.urgentPtr",
    "reserved": "hdr.tcp.reserved",
    "tcpChecksum": "hdr.tcp.checksum",
    "urgFlag": "hdr.tcp.flags[5]",  
    "eceFlag": "hdr.tcp.flags[6]", 
    "cwrFlag": "hdr.tcp.flags[7]", 
    "payload_length": "meta.payload_len",  
}

def translate_name(feature_name):
    return name_mapping.get(feature_name, feature_name)


def get_datatype(feature_name):
    if feature_name in type_mapping:
        return type_mapping[feature_name]

    translated = translate_name(feature_name)

    if translated in type_mapping:
        return type_mapping[translated]

    return None

def get_source_from_type(typeName):
    if typeName in source_mapping:
        return source_mapping[typeName]

    translated = translate_name(typeName)

    if translated in source_mapping:
        return source_mapping[translated]

    return None
