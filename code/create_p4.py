from datatypes import *



features = ['ipi', 'tos', 'sport']


def generate_match_action(feature, index):
    print(f"    action set_actionselect{index}(bit<14> featurevalue{index})" + " {",
          f"\n        meta.action_select{index} = featurevalue{index}",
          "\n    }\n"
          )

    print(f"    table feature{index}_exact" + " {",
          "\n       key = {",
          f"\n          meta.{feature}: range ;",
          "\n       actions = {",
          f"\n          NoAction;\n          set_actionselect{index};",
          "\n       }\n         size = 1024",
          "\n   }"
          )



# Template inicial nunca muda
print("""
/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_IPV4 = 0x800;

const bit<8> PROTO_INT = 253;
const bit<8> PROTO_TCP = 6;

#define MAX_HOPS 10


/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/


typedef bit<48> macAddr_v;
typedef bit<32> ip4Addr_v;

typedef bit<16> flowID_t;
typedef bit<32> int_t;
typedef bit<48> timestamp_t;

typedef bit<31> switchID_v;
typedef bit<9> ingress_port_v;
typedef bit<9> egress_port_v;
typedef bit<9>  egressSpec_v;
typedef bit<48>  ingress_global_timestamp_v;
typedef bit<48>  egress_global_timestamp_v;
typedef bit<32>  enq_timestamp_v;
typedef bit<19> enq_qdepth_v;
typedef bit<32> deq_timedelta_v;
typedef bit<19> deq_qdepth_v;

header ethernet_h {
    macAddr_v dstAddr;
    macAddr_v srcAddr;
    bit<16>   etherType;
}

header ipv4_h {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    ip4Addr_v srcAddr;
    ip4Addr_v dstAddr;
}

header tcp_h {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<32> seqNo;
    bit<32> ackNo;
    bit<4>  dataOffset;
    bit<3>  res;
    bit<3>  ecn;
    bit<6>  ctrl;
    bit<16> window;
    bit<16> checksum;
    bit<16> urgentPtr;
}

header nodeCount_h{
    bit<16>  count;
}

header InBandNetworkTelemetry_h {
    switchID_v swid;
    ingress_port_v ingress_port;
    egress_port_v egress_port;
    egressSpec_v egress_spec;
    ingress_global_timestamp_v ingress_global_timestamp;
    egress_global_timestamp_v egress_global_timestamp;
    enq_timestamp_v enq_timestamp;
    enq_qdepth_v enq_qdepth;
    deq_timedelta_v deq_timedelta;
    deq_qdepth_v deq_qdepth;
}

struct ingress_metadata_t {
    bit<16>  count;
}

struct parser_metadata_t {
    bit<16>  remaining;
}

struct metadata {
    ingress_metadata_t   ingress_metadata;
    parser_metadata_t   parser_metadata;
    flowID_t flowID;
    bit<32> seqNo;
    bit<32> ackNo;
    bit<16> window;
    timestamp_t ipi;
    bit<14> action_select1;
    bit<14> action_select2;
    bit<14> action_select3;
    bit<14> action_select4;
    bit<3>  result;
}

struct headers {
    ethernet_h         ethernet;
    ipv4_h             ipv4;
    tcp_h              tcp;
    nodeCount_h        nodeCount;
    InBandNetworkTelemetry_h[MAX_HOPS] INT;
}

/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol){
            PROTO_TCP: parse_tcp;
            PROTO_INT: parse_count;
            default: accept;
        }
    }

    state parse_tcp {
        packet.extract(hdr.tcp);
        transition accept;
    }

    state parse_count{
        packet.extract(hdr.nodeCount);
        meta.parser_metadata.remaining = hdr.nodeCount.count;
        transition select(meta.parser_metadata.remaining) {
            0 : accept;
            default: parse_int;
        }
    }

    state parse_int {
        packet.extract(hdr.INT.next);
        meta.parser_metadata.remaining = meta.parser_metadata.remaining  - 1;
        transition select(meta.parser_metadata.remaining) {
            0 : accept;
            default: parse_int;
        }
    }
}
/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply {  }
}

/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {
    // register<bit<3>>(0xffff) flow_queue;
    register<bit<48>>(0xffff) ipi_register;

    register<bit<48>>(0xffff) lpt_register;

    // register<bit<3>>(6) results_reg;

    counter(3, CounterType.packets) resultCounter;

    action drop() {
        mark_to_drop(standard_metadata);
    }
""")

for i in range(len(features)):
    generate_match_action(features[i], i+1)
