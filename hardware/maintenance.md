# Hardware Maintenance & Monitoring

Zbiór praktycznych informacji o utrzymaniu sprzętu homelaba w dobrej kondycji.

## 1. Monitoring temperatur i obciążenia

- Narzędzia:
  - Na hoście Proxmox: `sensors`, `pveperf`, `htop`
  - W VM z Ollamą: `nvidia-smi` (monitoring GPU)
- Cele:
  - CPU: < 85°C pod długotrwałym obciążeniem
  - GPU: < 80°C przy pracy modeli LLM
  - Brak throttlingu przy pełnym obciążeniu Wazuh + LLM

## 2. Zarządzanie Energią i Cykl Pracy (Power Management)

- **Tryb pracy:** **On-Demand** (Na żądanie)
  - Lab jest uruchamiany wyłącznie na czas aktywnych sesji szkoleniowych, testów penetracyjnych lub prac developerskich.
  - Podejście to pozwala na oszczędność energii oraz symuluje środowiska typu "ephemeral" (ulotne), gdzie ciągłość uptime nie jest priorytetem.
  
- **Zasilanie:**
  - PSU: 850W [Certyfikat Gold] Stand-by(uruchomione maszyny) - 100W LLM - 300W 
  - Średni czas pracy: 10h godzin tygodniowo (uruchamiane ad-hoc).
  - **Procedura Cold Start:** Po uruchomieniu hosta, skrypt startowy automatycznie podnosi kluczowe kontenery (Wazuh, OPNsense) w odpowiedniej kolejności, aby zapewnić spójność logów.

## 3. Konserwacja Systemu (Ważne w trybie On-Demand)

Ze względu na nieregularny czas pracy, procedury maintenance różnią się od serwerów 24/7:

- **Time Sync (NTP):** Krytyczne dla Wazuha i logów. Weryfikacja synchronizacji czasu `chrony`/`ntp` następuje natychmiast po starcie maszyny.
- **Aktualizacje:** Wykonywane ręcznie na początku sesji ("Patch Tuesday" podejście), zamiast automatycznych cron-ów w nocy, które mogłyby zostać pominięte.
