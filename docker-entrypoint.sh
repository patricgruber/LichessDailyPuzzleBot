#!/bin/bash

# Preparation for cron daemon
env >> /etc/environment

# Start the cron daemon
cron -f -l 2 &

# Start the signal-cli daemon
signal-cli --config /var/lib/signal-cli -a $ACCOUNT daemon --http localhost:1234 &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
