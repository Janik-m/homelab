# 🌐 Network Architecture

Architektura sieci to hybryda klasycznej sieci płaskiej (Home Network) oraz izolowanej strefy wirtualnej (Lab Network). Dzięki temu krytyczne usługi domowe (DNS, Smart Home) są łatwo dostępne dla domowników, podczas gdy wrażliwe środowisko testowe jest odseparowane firewallem.

### 🗺️ Topologia Sieci

Ruch sieciowy odbywa się w dwóch głównych segmentach:
1.  **Strefa Zaufana (Home):** Dostępna bezpośrednio z routera fizycznego. Tu znajdują się urządzenia fizyczne oraz usługi "produkcyjne" (DNS, Pliki).
2.  **Strefa Izolowana (Lab):** Wirtualna sieć za NAT-em OPNsense. Tu znajdują się narzędzia Security i AI, chronione przed przypadkowym dostępem z sieci domowej.

---

### 🛡️ Segmentacja Sieci (Network Segmentation)

| Nazwa Strefy | Adresacja (CIDR) | Urządzenia / Usługi | Opis i Rola |
| :--- | :--- | :--- | :--- |
| **HOME LAN** | `192.168.0.0/24` | • Router ISP (Brama)<br>• **Raspberry Pi 5** (Całość)<br>• **Proxmox Host** (Mgmt IP)<br>• **File Server** (LXC na PC) | Główna sieć domowa. Usługi tutaj muszą być dostępne dla każdego domownika (np. AdGuard) lub służą do wymiany plików (Backup). |
| **SEC LAB** | `192.168.100.0/24` | • **Wazuh SIEM**<br>• **Ollama AI**<br>• **Docker Security** | Izolowany poligon. Brak bezpośredniego routingu z HOME LAN. Wyjście na świat tylko przez OPNsense (Double NAT). |
| **VPN TUNNEL** | `10.0.100.0/24` | • Klient Administratora | Szyfrowany tunel pozwalający na bezpieczne "wbicie się" do strefy SEC LAB z poziomu HOME LAN lub Internetu. |

---

### 🧱 Firewall & Routing (OPNsense)

Wirtualny router OPNsense (na maszynie VM wewnątrz PC) pełni rolę strażnika strefy Lab.

**Kluczowe zasady ruchu:**
1.  **File Server (Wyjątek):** Mimo że działa na PC, jest wystawiony w sieci `192.168.0.x`, aby Raspberry Pi mogło robić na nim backupy bez konieczności zestawiania tuneli VPN.
2.  **Izolacja Labu:** Urządzenia z sieci domowej (TV, telefony) "nie widzą" serwerów Wazuha czy AI. Zapobiega to przypadkowym infekcjom lub wyciekom z testowanego środowiska.
3.  **Dostęp Administracyjny:** Aby zarządzać Wazuhem, admin musi połączyć się przez OpenVPN – nawet będąc fizycznie w domu.

### 🔌 Fizyczne Połączenia
*   **PC Server:** Podpięty kablem ETH. Obsługuje dwie wirtualne karty sieciowe: jedną dla sieci domowej (bridge do File Servera i Mgmt), drugą prywatną dla Labu.
*   **Raspberry Pi:** Podpięte kablem ETH. Działa w pełni w sieci domowej, służąc jako stabilny punkt dostępowy DNS (AdGuard) dla wszystkich urządzeń w domu.
