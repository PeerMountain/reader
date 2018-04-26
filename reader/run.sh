#!/bin/bash

# Reader needs to communicate with Elasticsearch and HBase
# Elasticsearch is containerized, accessed with an overlay network
# But HBase is running on the host, so we use the host IP
# Also, the Writer just runs on peer-mountain01, the HBase master node
HOST_IP=$(/sbin/ip route|awk '/default/ { print $3 }')
export HBASE_HOSTNAME=$HOST_IP

python reader/main.py
