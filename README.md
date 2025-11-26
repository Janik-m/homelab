# Homelab
Witaj w dokumentacji mojego domowego laboratorium. Ten projekt służy mi do nauki cyberbezpieczeństwa, automatyzacji procesów w SOC z wykorzystaniem lokalnego AI oraz testowania aplikacji webowych.

<img width="1729" height="782" alt="Wazuh-dashboard" src="https://github.com/user-attachments/assets/28dae554-7a30-48b4-9a3c-79b2c4949e4f" />

🖥️ Hardware

Całość stoi na jednej maszynie typu "All-in-One".

CPU	     -       Intel Core i9-13900KF	   -     High-performance dla wirtualizacji

RAM	      -            64 GB DDR5	     -       Wystarcza na wiele maszyn VM i LLM

GPU	    -        NVIDIA RTX 4070 SUPER	-        Passthrough do VM z Ollamą

Dysk	   -       2TB NVMe SSD	           -     Szybki storage dla baz danych i logów

🧩 Infrastruktura (Software Stack)

Systemem bazowym jest Proxmox VE 9.1.1. Sieć jest odseparowana od domowego LAN-u za pomocą wirtualnego routera.

1. 🛡️ Bezpieczeństwo i Sieć (VM)

OPNsense (FreeBSD): Główny firewall.

OpenVPN: Skonfigurowany tunel pozwalający na bezpieczny dostęp do laba z zewnątrz, bez konieczności używania Windowsa wewnątrz laba.

Sieć: Cały ruch LAN w labie jest izolowany i przechodzi przez OPNsense.

2. 👁️ Monitoring i Logi (VM)
Wazuh (Ubuntu Server): Centrum operacji bezpieczeństwa (SIEM).

Zbiera logi ze wszystkich VM i kontenerów CT.

Analizuje zdarzenia bezpieczeństwa w czasie rzeczywistym.

3. 🤖 AI i Automatyzacja (VM + CT)
Ollama VM (Ubuntu + GPU Passthrough):

Lokalny model LLM (Foundation-Sec-8B-Instruct-Q8) wykorzystujący RTX 4070.

Służy do analizy alertów z Wazuha oraz wspomagania decyzji w n8n.

n8n (LXC Container):

Silnik automatyzacji. Łączy Wazuh, Ollamę i powiadomienia.

Postfix (LXC Container):

Lokalny serwer SMTP dedykowany wyłącznie do wysyłania alertów z systemu Wazuh.

4. 🐳 Docker i Aplikacje (VM)
Maszyna Ubuntu Server pełniąca rolę hosta dla kontenerów:

DVWA: Środowisko do testów penetracyjnych (Damn Vulnerable Web App).

Custom IP Blocker: Autorska aplikacja do blokowania adresów IP.

MySQL: Baza danych dla aplikacji.
