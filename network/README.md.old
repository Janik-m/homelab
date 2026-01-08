# 🌐 Network Architecture

Moja sieć opiera się na wirtualizacji (SDN - Software Defined Networking) wewnątrz Proxmoxa, wykorzystując tylko jeden fizyczny interfejs sieciowy (Single NIC Architecture).

## 🗺️ Topology Diagram

Poniższy schemat przedstawia przepływ ruchu sieciowego. Fizyczny router domowy "nie widzi" co dzieje się wewnątrz Labu – widzi tylko interfejs WAN OPNsense.


```mermaid
graph TD
    subgraph Physical[Fizyczna Sieć Domowa]
        ISP[Internet / Router ISP] -->|192.168.1.x| PHY_NIC[Fizyczna Karta Sieciowa]
    end

    subgraph Proxmox[Proxmox Host]
        PHY_NIC --- VMBR0[vmbr0 - Linux Bridge WAN]
        
        subgraph OPNsense_VM[VM: OPNsense Firewall]
            VMBR0 -.->|vtnet0 WAN| FW_WAN[Interfejs WAN]
            FW_LAN[Interfejs LAN] -.->|vtnet1 LAN| VMBR1
            FW_OVPN[OpenVPN Server] -.-> FW_WAN
        end
        
        VMBR1[vmbr1 - Izolowany Bridge LAN]
        
        VMBR1 --- Wazuh[VM: Wazuh SIEM]
        VMBR1 --- Ollama[VM: Ollama AI]
        VMBR1 --- Docker[VM: Docker Apps]
        VMBR1 --- N8N[CT: n8n Automation]
    end

    subgraph Admin_Workstation[Laptop Admina]
        WinVM[VM: Windows 11 Secure] -.->|OpenVPN Client| FW_OVPN
    end

    WinVM -.->|SSH i HTTPS via Tunnel| VMBR1
    
    style OPNsense_VM fill:#f96,stroke:#333,stroke-width:2px
    style VMBR1 fill:#bbf,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5
    style WinVM fill:#bfb,stroke:#333,stroke-width:2px
```



## 🛡️ Network Segmentation

| Interfejs | Typ | Bridge | Podsieć (CIDR) | Opis |
| :--- | :--- | :--- | :--- | :--- |
| **WAN** | Virtual | `vmbr0` | 192.168.1.0/24 | Uplink do domowego routera. OPNsense pobiera tu IP przez DHCP. |
| **LAN (Lab)** | Virtual | `vmbr1` | 192.168.100.0/24 | **Izolowana strefa.** Brak fizycznego wyjścia. Cały ruch musi przejść przez firewall OPNsense. |
| **OpenVPN** | Tunnel | `tun0` | 10.0.100.0/24 | Sieć dla zdalnych klientów (admina). |

## 🔐 Firewall & Routing (OPNsense)

Ponieważ Proxmox i OPNsense dzielą ten sam sprzęt, konfiguracja wymagała ostrożności, aby nie odciąć dostępu do GUI Proxmoxa.

### Kluczowe reguły Firewall:
1.  **Block RFC1918 on WAN:** Wyłączone (bo WAN jest w sieci prywatnej 192.168.1.x).
2.  **Allow OpenVPN to LAN:** Zezwolenie na ruch z tunelu 10.0.100.0/24 do sieci Lab 192.168.100.0/24.
3.  **Izolacja IoT:** (Jeśli planujesz w przyszłości) - zablokowanie ruchu z Labu do domowej sieci 192.168.1.x (z wyjątkiem bramy).

### Dostęp Zdalny (OpenVPN)
Zamiast wystawiać porty SSH każdej maszyny na świat, wystawiony jest tylko jeden port UDP dla OpenVPN.
- **Klient:** OpenVPN Connect.
- **Auth:** Certyfikat użytkownika + TLS Key.

