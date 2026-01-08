# 🍓 Raspberry Pi 5 - Home Lab Node

Centralny węzeł automatyzacji i bezpieczeństwa domowego oparty na wirtualizacji Proxmox (port ARM). Maszyna pełni rolę serwera "always-on" dla usług IoT, blokowania reklam oraz workflowów automatyzacji AI.

## ⚙️ Specyfikacja Sprzętowa (Hardware)

To nie jest standardowa Malinka. Setup został zbudowany z naciskiem na wydajność I/O oraz niezawodność zasilania.

| Komponent | Model / Szczegóły | Rola |
|-----------|-------------------|------|
| **SBC** | Raspberry Pi 5 (16GB RAM) | Jednostka obliczeniowa |
| **Storage** | Dysk NVMe M.2 (via HAT) | Szybki storage dla kontenerów LXC |
| **Zasilanie (UPS)** | Geekworm x1200 | Podtrzymanie zasilania i zarządzanie energią |
| **Obudowa** | Dedykowana metalowa obudowa | Pasywne i aktywne chłodzenie, ochrona mechaniczna |

## 🏗️ Architektura Systemowa

System działa pod kontrolą **Proxmox VE (port ARM64)**. Usługi są odseparowane od siebie za pomocą kontenerów **LXC (Linux Containers)**, co zapewnia minimalny narzut na wydajność przy zachowaniu izolacji procesów.

### 🚀 Uruchomione Kontenery (LXC)

| Usługa | Rola | Stack Technologiczny |
|--------|------|----------------------|
| **Home Assistant** | Centrum sterowania IoT | Python, YAML |
| **n8n** | Automatyzacja workflow i integracja AI | Node.js, Low-code |
| **AdGuard Home** | DNS Sinkhole, ochrona sieci, blokowanie trackingu | Go |
| **OpenVPN** | Bezpieczny dostęp zdalny do infrastruktury | OpenSSL, VPN |

## 🛡️ Cyberbezpieczeństwo & Networking

- **VPN:** Dostęp do panelu Proxmox i usług wewnętrznych (HA, n8n) jest możliwy z zewnątrz wyłącznie tunelowanym połączeniem przez OpenVPN.
- **DNS:** Cały ruch sieciowy w domu jest filtrowany przez AdGuard Home, co eliminuje telemetrię i złośliwe domeny na poziomie DNS.
- **UPS Monitoring:** Skrypty monitorujące stan Geekworm x1200 (poziom naładowania/zasilanie sieciowe) [TODO: Dodać integrację z Home Assistant].

## 🤖 Automatyzacja & AI (n8n)

Instancja n8n służy jako "mózg" operacyjny, łączący:
1. Webhooki z Home Assistant.
2. Zewnętrzne API modeli LLM (OpenAI/Anthropic/Lokalne modele).
3. Powiadomienia o incydentach bezpieczeństwa.

---
*Repozytorium: Część projektu CyberSec HomeLab.*
