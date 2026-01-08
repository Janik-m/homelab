#!/bin/bash
HOST= # IP serwera Proxmox
if ping -c1 -W1 "$HOST" >/dev/null 2>&1; then
  echo "up"
else
  echo "down"
fi
