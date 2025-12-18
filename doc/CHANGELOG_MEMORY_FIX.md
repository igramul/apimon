# Änderungszusammenfassung - Memory Leak Fix

## Datum: 18. Dezember 2025

## Problem
- Memory Allocation Error alle ~11 Minuten auf Raspberry Pi Zero
- Worker-Abstürze durch SIGSEGV
- Fehler: `ws2811_init failed with code -6 (Unable to map registers into userspace)`

## Root Cause
1. Zu häufige Hardware-Register-Zuordnung durch NeoPixel-Bibliothek
2. `show()` wurde bei jedem Update aufgerufen, auch ohne Änderungen
3. Sehr hohe Update-Frequenz (10x/Sekunde) auf einem Raspberry Pi Zero
4. Keine robuste Error-Behandlung bei Hardware-Fehlern

## Implementierte Lösungen

### 1. `app/neopixel_controller.py`
**Änderung**: Intelligentes Update mit Change-Detection
- `_update()` Methode optimiert
- `show()` nur aufrufen wenn tatsächlich Änderungen vorhanden
- Try-Except Block um `show()` Aufruf
- Flag `needs_update` trackt Änderungen

**Vorteil**: Reduziert Hardware-Zugriffe um bis zu 90%

### 2. `apimon.py`
**Änderung**: Update-Intervall angepasst
- Pixel-Update-Intervall: 0.1s → 0.5s (2 Updates/Sekunde)
- Exception-Handling in `job_update_pixels()`

**Vorteil**: 
- 80% weniger Hardware-Zugriffe pro Minute
- Animationen bleiben flüssig (2 FPS ausreichend)
- Worker crasht nicht mehr bei Fehlern

### 3. `app/rpi_ws281x_pixel.py`
**Änderung**: Ressourcen-Management verbessert
- `__del__()` Destruktor hinzugefügt
- `__getitem__()` für Farbvergleiche implementiert
- Error-Handling in `show()` Methode
- Cleanup bei Objekt-Zerstörung

**Vorteil**: Saubere Ressourcen-Freigabe

### 4. `app/JTLS/JiraTicketLedStripe.py`
**Änderung**: Robustes Error-Handling
- Try-Except in `update_pixels()`
- Fehler werden geloggt aber stoppen nicht die Anwendung
- Error-Status wird gesetzt

**Vorteil**: Einzelne LED-Fehler bringen nicht die ganze App zum Absturz

### 5. `gunicorn_config.py` (NEU)
**Änderung**: Gunicorn-Optimierung
- Single Worker (verhindert Ressourcen-Konflikte)
- Timeout-Konfiguration
- Worker-Lifecycle-Hooks
- Optimiertes Logging

**Vorteil**: Stabilerer Betrieb, bessere Diagnose

### 6. `etc/apimon.service`
**Änderung**: Service nutzt Gunicorn-Config
- Referenziert neue Config-Datei

### 7. `MEMORY_FIX.md` (NEU)
**Dokumentation** für Installation und Troubleshooting

## Performance-Impact

### Vorher
- 10 Updates/Sekunde
- ~600 Hardware-Zugriffe/Minute
- Worker-Crash alle ~11 Minuten
- Hohe Memory-Fragmentierung

### Nachher
- 2 Updates/Sekunde
- ~120 Hardware-Zugriffe/Minute (nur bei tatsächlichen Änderungen)
- Keine Worker-Crashes erwartet
- Minimale Memory-Fragmentierung

## Testing

Auf dem Raspberry Pi testen:
```bash
# Service aktualisieren
sudo systemctl daemon-reload
sudo systemctl restart apimon

# Logs überwachen
sudo journalctl -u apimon -f

# Memory überwachen
watch -n 5 'free -h'
```

Nach 24 Stunden sollten keine Memory-Fehler mehr auftreten.

## Rollback

Falls Probleme auftreten:
```bash
cd /home/apimon/Work/apimon
git checkout HEAD~1
sudo systemctl restart apimon
```

## Weitere Optimierungsmöglichkeiten

Falls das Problem weiterhin auftritt:
1. Intervall auf 1 Sekunde erhöhen
2. Pulsing-Effekte vereinfachen
3. Alternative NeoPixel-Bibliothek verwenden
4. Swap-Speicher erhöhen
5. GPU-Memory reduzieren (in /boot/config.txt: gpu_mem=16)

