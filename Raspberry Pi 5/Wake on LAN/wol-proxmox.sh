#!/bin/bash
# MAC twojego serwera Proxmox
MAC="mac"

# broadcast twojej sieci LAN (przykład 192.168.0.255)
wakeonlan -i 192.168.x.255 "$MAC"
