#!/bin/bash

# Start the signal-cli daemon
signal-cli --config /var/lib/signal-cli -a $ACCOUNT daemon --http localhost:1234 &

# Start the cron service
cron -f -l 8 &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
