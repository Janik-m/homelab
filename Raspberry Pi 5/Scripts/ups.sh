#!/bin/bash
# spokojne wyłączenie kontenerów LXC przy zasilaniu z UPS

LXC_IDS="100 101 102"

for ID in $LXC_IDS; do
  echo "Shutting down LXC $ID..."
  pct shutdown "$ID" --forceStop 0 --timeout 120
done
