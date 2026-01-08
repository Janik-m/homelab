#!/bin/bash
set -e

# Katalog na NFS w labie
TARGET="/mnt/lab-backup/proxmox-port"
MOUNT_POINT="$(dirname "$TARGET")"
NFS_SOURCE="IP:/srv/backup/pi"

CT_LIST="100 101 102 103"

echo "=== Backup LXC do $TARGET ==="

# Sprawdź, czy udział jest zamontowany
if ! mountpoint -q "$MOUNT_POINT"; then
  echo "Udział $MOUNT_POINT nie jest zamontowany. Próbuję montować..."

  # albo, jeśli montujesz “ręcznie”, zamiast powyższego użyj np.:
   mount -t nfs "$NFS_SOURCE" "$MOUNT_POINT" || {
     echo "ERROR: Nie udało się zamontować $NFS_SOURCE na $MOUNT_POINT. Przerywam."
     exit 1
   }
fi

# Utwórz katalog, jeśli nie istnieje
mkdir -p "$TARGET"

echo "Usuwam stare backupy z $TARGET ..."
rm -rf "$TARGET"/*

echo "Uruchamiam vzdump dla: $CT_LIST ..."
vzdump $CT_LIST \
  --mode snapshot \
  --compress zstd \
  --dumpdir "$TARGET" \
  --remove 0

echo "BACKUP_OK: LXC $CT_LIST zapisane w $TARGET"
