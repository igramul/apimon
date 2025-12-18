# Fix für Memory Allocation Error auf Raspberry Pi

## Problem
Der Fehler `ws2811_init failed with code -6 (Unable to map registers into userspace)` tritt auf, wenn:
- Die NeoPixel-Bibliothek zu häufig Hardware-Register zuordnet
- Speicher nicht korrekt freigegeben wird
- Gunicorn Worker abstürzen und neu starten

## Implementierte Lösungen

### 1. Optimierung der Pixel-Updates (`neopixel_controller.py`)
- **Änderung vor Update**: Nur `show()` aufrufen, wenn sich tatsächlich Farben geändert haben
- **Error Handling**: Abfangen von Exceptions beim `show()` Aufruf
- **Reduzierte Hardware-Zugriffe**: Weniger Memory-Allocations

### 2. Reduzierte Update-Frequenz (`apimon.py`)
- **Vorher**: 10 Updates/Sekunde (0.1s Intervall)
- **Nachher**: 2 Updates/Sekunde (0.5s Intervall)
- **Vorteil**: Weniger Speicherdruck, weiterhin flüssige Animationen

### 3. Verbessertes Error Handling
- Exception-Handling in allen Update-Methoden
- Worker-Abstürze werden verhindert
- Fehler werden geloggt, aber die Anwendung läuft weiter

### 4. Gunicorn-Konfiguration (`gunicorn_config.py`)
- **Single Worker**: Verhindert Ressourcenkonflikte
- **Timeouts konfiguriert**: Verhindert hängende Requests
- **Logging optimiert**: Bessere Fehlerdiagnose

### 5. Ressourcen-Cleanup (`rpi_ws281x_pixel.py`)
- Destruktor hinzugefügt für sauberes Aufräumen
- Error Handling im `show()` Aufruf
- `__getitem__` implementiert für Farbvergleiche

## Installation der Änderungen

### Auf dem Raspberry Pi:

1. **Code aktualisieren**:
```bash
cd /home/apimon/Work/apimon
git pull
```

2. **Service-Datei aktualisieren**:
```bash
sudo cp etc/apimon.service /etc/systemd/system/
# Pfade in der Datei anpassen
sudo nano /etc/systemd/system/apimon.service
```

3. **Service neu laden und starten**:
```bash
sudo systemctl daemon-reload
sudo systemctl restart apimon
```

4. **Logs überwachen**:
```bash
sudo journalctl -u apimon -f
```

## Zusätzliche Empfehlungen

### Memory-Überwachung
Überwachen Sie den Speicher auf dem Raspberry Pi:
```bash
free -h
watch -n 5 'free -h'
```

### Swap erhöhen (falls nötig)
Für Raspberry Pi Zero mit wenig RAM:
```bash
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# CONF_SWAPSIZE=1024 (statt 100)
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### GPU Memory reduzieren
In `/boot/config.txt`:
```
gpu_mem=16  # Minimal, da keine GPU benötigt wird
```

### System-Limits erhöhen
In `/etc/security/limits.conf`:
```
root soft memlock unlimited
root hard memlock unlimited
```

## Monitoring

Nach den Änderungen sollten Sie:
1. Keine `mmap error: Cannot allocate memory` Fehler mehr sehen
2. Keine Worker-Abstürze mehr haben
3. Stabilere LED-Updates haben

Überwachen Sie das System für mindestens 24 Stunden, um sicherzustellen, dass der Fehler nicht mehr auftritt.

## Troubleshooting

Wenn der Fehler weiterhin auftritt:

1. **Update-Intervall weiter erhöhen** (z.B. auf 1 Sekunde):
   ```python
   @scheduler.task('interval', id='do_job_update_pixels', seconds=1.0)
   ```

2. **Alternative NeoPixel-Bibliothek verwenden**:
   - Wechsel zu `rpi_ws281x` direkt ohne Adafruit-Wrapper

3. **System-Ressourcen prüfen**:
   ```bash
   cat /proc/meminfo
   dmesg | grep -i memory
   ```

4. **Gunicorn durch einfachen WSGI-Server ersetzen**:
   - Für Raspberry Pi Zero könnte `waitress` besser geeignet sein

