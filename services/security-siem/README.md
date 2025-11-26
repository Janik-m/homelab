# 🛡️ Security Operations Center (SOC) - Wazuh

Głównym elementem mojego systemu bezpieczeństwa jest **Wazuh** (Open Source SIEM/XDR). Pełni on rolę centrum monitoringu, zbierając logi ze wszystkich hostów w sieci (Proxmox, OPNsense, VM).

## 🏗️ Architektura Wdrożenia

- **Manager:** Ubuntu Server VM (8 vCPU, 16GB RAM)
- **Agents:** Zainstalowane na wszystkich maszynach Linux (Proxmox Host, Docker VM) oraz Windows (Admin VM).
- **Integracja:** Logi są przesyłane do N8N w celu analizy przez AI (Ollama).

## ⚙️ Kluczowe Konfiguracje

### 1. Wykrywanie ataków na SSH (Brute Force)
Zmodyfikowana reguła w `local_rules.xml` wykrywa nieudane logowania szybciej niż standardowa konfiguracja.
 
	Uwaga: Pełne pliki konfiguracyjne (zanonimizowane) znajdują się w podkatalogu configs/.

### 2. File Integrity Monitoring (FIM)
Monitorowanie zmian w krytycznych plikach konfiguracyjnych Proxmoxa (/etc/pve/).

W konfiguracji agenta (ossec.conf) na hoście Proxmox:
<syscheck>
  <directories check_all="yes" realtime="yes" report_changes="yes">/etc/pve</directories>
  <directories check_all="yes" realtime="yes">/etc/network/interfaces</directories>
  <ignore>/etc/pve/priv/known_hosts</ignore>
</syscheck>
