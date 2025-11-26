# 🤖 AI-Driven Automation (SOAR)

Ta sekcja opisuje moją autorską integrację **Wazuh SIEM** z lokalnym modelem językowym **Ollama (LLM)** przy użyciu **n8n**. 

System automatycznie analizuje alerty bezpieczeństwa, zmniejszając liczbę fałszywych pozytywów (False Positives) i dostarczając kontekst dla administratora.

## 🔄 Workflow Diagram

## 🔄 Workflow Diagram (AI Router)

Mój główny proces automatyzacji (`Wazuh Alert Handler`) działa jako inteligentny router, który klasyfikuje zdarzenia przed podjęciem akcji.

1. **Trigger:** Webhook odbiera surowy alert JSON z Wazuha.
2. **Prompt Engineering:** Skrypt JS przygotowuje kontekst dla modelu, prosząc o kategoryzację na jedną z 4 grup: `WEB_ATTACK`, `AUTH_FAIL`, `SYSTEM`, `UNKNOWN`.
3. **AI Analysis (Ollama):**
   - Model: `foundation-sec-local:latest` (customowy model bazujący na Llama 3).
   - Zadanie: Przeanalizuj logi i zwróć JSON z oceną ryzyka i kluczowymi detalami (np. Attacker IP).
4. **Data Sanitization:**
   - Węzeł *JSON Parser* (Custom JS) naprawia potencjalnie uszkodzony JSON zwrócony przez LLM (np. brakujące klamry) i ekstrahuje dane przy użyciu Regex jako fallback.
5. **Routing (Switch Node):**
   - Na podstawie pola `category` alert trafia do dedykowanego pod-procesu (Sub-workflow):
     - 🔴 **WEB_ATTACK:** Uruchamia analizę dla atakow sieciowych.
     - 🟠 **AUTH_FAIL:** Sprawdza czy IP jest znane, ewentualnie blokuje.
     - 🟡 **SYSTEM:** Loguje anomalie dyskowe/usług.
     - ⚪ **UNKNOWN:** Wysyła powiadomienie do admina w celu ręcznej weryfikacji.

## 🧠 Ollama & GPU Passthrough

Model AI działa na VM z przekazaną kartą **RTX 4070 SUPER**. Dzięki temu analiza pojedynczego alertu zajmuje < 5s (zamiast 30s na CPU).
- **Model:** `Foundation-Sec-8B-Instruct-Q8` (kwantyzacja 8-bit dla szybkości).
- **API:** Dostępne wewnętrznie pod adresem `http://x.x.x.x:11434`.

## 📧 Postfix (SMTP Relay)
Lokalny serwer pocztowy (kontener LXC) służy wyłącznie do wysyłania powiadomień wewnątrz sieci LAN. Jest odizolowany od internetu (brak możliwości odbierania poczty z zewnątrz).
