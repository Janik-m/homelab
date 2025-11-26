# 🖥️ Hardware Inventory

Szczegółowa specyfikacja sprzętowa mojego "All-in-One" Homelaba. Maszyna została zbudowana jako wysokowydajna stacja robocza, przekształcona w serwer wirtualizacji Proxmox.

## ⚙️ Podzespoły Bazowe (Core Compute)

Sercem laba jest architektura hybrydowa Intel (Raptor Lake), co wymagało odpowiedniej konfiguracji w Proxmoxie (CPU affinity) dla zapewnienia stabilności kluczowych maszyn VM.

| Komponent | Model | Specyfikacja | Rola w Labie |
| :--- | :--- | :--- | :--- |
| **CPU** | **Intel Core i9-13900KF** | 24 Cores (8P + 16E) / 32 Threads<br>Brak iGPU (wersja F) | Potężna moc obliczeniowa dla analizy logów (Wazuh) i wielu kontenerów. Rdzenie P dedykowane dla VM krytycznych. |
| **RAM** | **64 GB Patriot Viper** | 4x 16GB DDR5<br>Taktowanie: 6000 MHz | Duża ilość RAM pozwala na utrzymanie modelu LLM w pamięci bez swapowania. |
| **Płyta Główna** | **ASRock Z790 Steel Legend** | Chipset Z790<br>PCIe 5.0 | Solidna sekcja zasilania dla i9 oraz wsparcie dla IOMMU (VT-d) niezbędnego do GPU Passthrough. |

## 🎨 Grafika i AI (GPU)

Karta graficzna jest w całości odseparowana od hosta (Proxmox) i przekazana (PCIe Passthrough) do maszyny wirtualnej Ubuntu z Ollamą.

| Komponent | Model | VRAM | Zastosowanie |
| :--- | :--- | :--- | :--- |
| **GPU** | **NVIDIA RTX 4070 SUPER** | 12 GB GDDR6X | **Lokalne AI:** Akceleracja modeli LLM (Llama 3, Mistral) używanych w automatyzacji n8n.<br>**Compute:** Dostępna dla eksperymentów z CUDA/Hashcat. |

## 💾 Pamięć Masowa (Storage)

Wykorzystuję bardzo szybki dysk NVMe jako jedyną przestrzeń dyskową (Single Node), co zapewnia błyskawiczny dostęp do baz danych i logów.

| Typ | Model | Pojemność | Konfiguracja |
| :--- | :--- | :--- | :--- |
| **NVMe** | **Lexar NM790** | **2 TB** | **PCIe 4.0 x4**. Hostuje system Proxmox (local) oraz wszystkie dyski wirtualne (local-lvm). |
| **Backup** | - | - | *Brak lokalnego dysku backupu. Backupy kluczowych konfiguracji są wypychane na zewnętrzny udział sieciowy/chmurę.* |

## 🔌 Sieć i Zasilanie

Specyfika laba opiera się na wirtualizacji sieci, ze względu na posiadanie tylko jednego fizycznego interfejsu.

*   **PSU (Zasilacz):** 850W [Certyfikat Gold/Platinum] - Zapas mocy dla RTX 4070 i i9 pod pełnym obciążeniem.
*   **NIC (Sieć):** 1x 2.5GbE (Dragon RTL8125BG - zintegrowana).
    *   *Konfiguracja:* Fizyczny port służy jako uplink do sieci domowej. Cały ruch wewnątrz Lab-u odbywa się na wirtualnych mostkach (Linux Bridge), które nie wychodzą na zewnątrz fizycznego interfejsu bez przejścia przez OPNsense.
*   **Chłodzenie:** Cooler Master MasterLiquid (AIO) - Zapewnia stabilną temperaturę procesora przy ciągłej pracy 24/7.

---

## 📝 Notatki techniczne i wyzwania

### 1. Konfiguracja 4 kości RAM DDR5
Użycie 4 modułów RAM (4x16GB) na platformie konsumenckiej DDR5 jest dużym obciążeniem dla kontrolera pamięci przy taktowaniu 6000 MHz. Wymagało to stabilizacji napięć w BIOS, aby uniknąć błędów ECC/awarii systemu przy pełnym obciążeniu.

### 2. Single NIC Architecture
Ponieważ posiadam tylko jedną fizyczną kartę sieciową, OPNsense nie działa w klasycznym układzie "Physical WAN / Physical LAN".
*   **WAN dla OPNsense:** Jest to wirtualny interfejs podpięty pod `vmbr0` (mostkujący fizyczną kartę).
*   **LAN dla Labu:** Jest to całkowicie wirtualny `vmbr1`, który nie ma przypisanego fizycznego portu. To zapewnia izolację - ruch z Labu nie może "uciec" do sieci domowej z pominięciem firewalla OPNsense.

### 3. Brak iGPU (Wersja KF)
Procesor z końcówką "KF" nie posiada zintegrowanej grafiki. Ponieważ jedyne GPU (RTX 4070) jest przekazywane do VM (Passthrough), konsola hosta Proxmox jest dostępna wyłącznie przez sieć (Web Interface / SSH). Wymaga to ostrożności przy konfiguracji sieci, aby nie odciąć sobie dostępu.
