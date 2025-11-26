# GPU Passthrough – RTX 4070 SUPER → Ubuntu + Ollama

Dokument opisuje konfigurację PCIe Passthrough karty **NVIDIA RTX 4070 SUPER** z hosta Proxmox do maszyny wirtualnej Ubuntu, na której działa Ollama (LLM).

## 1. Wymagania wstępne

- Proxmox VE: 9.1.1
- CPU: Intel Core i9-13900KF (VT-x, VT-d włączone w BIOS)
- Płyta główna: ASRock Z790 Steel Legend
- GPU: NVIDIA RTX 4070 SUPER (dedykowana wyłącznie dla tej VM)

## 2. Konfiguracja hosta Proxmox

### 2.1. Włączenie IOMMU w Proxmox

Plik: `/etc/default/grub`  

- Linia GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on iomu=pt"

Po zmianach:
- `update-grub`
- restart hosta

### 2.2. Izolacja GPU dla VFIO

1.  Edycja modules
nano /etc/modules

Dodanie:
vfio
vfio_iommu_type1
vfio_pci
vfio_virqfd

2. Edycja nano /etc/modprobe.d/blacklist.conf

Dodanie:
blacklist nouveau
blacklist nvidia
blacklist nvidiafb
blacklist nvidia_drm

3. Aktualizacja initramfs i restart hosta

> Cel: Host nie ładuje sterowników NVIDIA – karta jest zarezerwowana dla maszyny wirtualnej.[web:44][web:50]

## 3. Konfiguracja VM w Proxmox

Najważniejsze parametry (fragment konfiguracji VM w `/etc/pve/qemu-server/<ID>.conf`):

- `hostpci0: <PCI-ID-GPU>,pcie=1`
- `machine: q35`
- `cpu: host`

## 4. Konfiguracja w Ubuntu (guest)

- Instalacja sterowników NVIDIA (repozytoria dystrybucji lub oficjalne)
- Weryfikacja:
  - `nvidia-smi` pokazuje RTX 4070 SUPER
- Instalacja Ollama i weryfikacja, że model korzysta z GPU (np. obciążenie w `nvidia-smi` podczas inferencji)

