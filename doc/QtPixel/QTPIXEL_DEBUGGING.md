# QtPixel Debugging Guide

## Problem: QtPixel-Fenster werden nicht angezeigt

### Ursachen und Lösungen

#### 1. **init() wird nicht aufgerufen**
**Problem:** Die QtPixel-Fenster werden nur angezeigt, wenn `init()` aufgerufen wird.

**Lösung:** ✅ BEHOBEN in `NeoPixelController.__init__()`:
```python
# Initialisiere die Pixel-Instanz (wichtig für QtPixel und ConsolePixel)
if hasattr(self._pixels, 'init'):
    self._pixels.init()
```

#### 2. **Qt Event Loop wird nicht verarbeitet**
**Problem:** Qt-Fenster benötigen eine Event Loop, um auf Ereignisse zu reagieren und sich zu aktualisieren.

**Lösung:** ✅ IMPLEMENTIERT in `QtPixel.show()`:
```python
def show(self):
    # ... Update LEDs ...
    # Qt Event Loop verarbeiten
    if QtPixel._app:
        QtPixel._app.processEvents()
```

Dies wird automatisch aufgerufen bei jedem `update()` in `NeoPixelController`.

#### 3. **PyQt5 nicht installiert**
**Problem:** Wenn PyQt5 nicht installiert ist, wird ConsolePixel als Fallback verwendet.

**Prüfung:**
```bash
python -c "import PyQt5; print('PyQt5 ist installiert')"
```

**Installation:**
```bash
pip install PyQt5
# oder
pip install -r requirements.txt
```

#### 4. **Display/GUI nicht verfügbar**
**Problem:** Wenn die Anwendung als systemd-Service läuft, hat sie keinen Zugriff auf das Display.

**Prüfung:**
```bash
echo $DISPLAY
```

**Lösung für systemd-Service:**
```ini
[Service]
Environment="DISPLAY=:0"
Environment="XAUTHORITY=/home/username/.Xauthority"
```

## Test-Skripte

### 1. Einfacher QtPixel-Test
```bash
python test_qtpixel_simple.py
```
Testet nur QtPixel ohne die gesamte Anwendung.

### 2. NeoPixelController-Test
```bash
python test_neopixel_controller.py
```
Testet NeoPixelController mit QtPixel (simuliert apimon).

### 3. Demo mit Animation
```bash
python demo_qtpixel.py
```
Zeigt zwei animierte LED-Streifen.

### 4. Volle Anwendung
```bash
python apimon.py
```
Startet die Flask-Anwendung mit LED-Anzeige.

## Debugging

### Welche Pixel-Klasse wird verwendet?

Füge dies am Anfang von `neopixel_controller.py` nach den Imports ein:
```python
print(f"Using Pixel class: {Pixel.__name__} from {Pixel.__module__}")
```

### Logging aktivieren

In `apimon.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

### Qt-Fenster manuell anzeigen

Test ob Qt funktioniert:
```python
python -c "
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
import sys
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Test')
label = QLabel('Qt funktioniert!', window)
window.show()
print('Fenster sollte sichtbar sein...')
app.exec_()
"
```

## Erwartetes Verhalten

### Beim Start von apimon.py:

1. ✅ NeoPixelController erstellt Pixel-Instanzen
2. ✅ `init()` wird aufgerufen (Fenster erscheinen)
3. ✅ Initialisierungs-Animation läuft (bunte LEDs, dann Lauflicht)
4. ✅ Scheduler startet und ruft alle 0.1s `update_pixels()` auf
5. ✅ `update()` → `show()` → `processEvents()` hält Fenster aktiv

### LED-Updates:

- Status-LED (Index 0): Pulsiert weiß/orange/rot je nach Status
- Ticket-LEDs (1 bis n-2): Zeigen Ticket-Status
- Overflow-LED (Index n-1): Pulsiert weiß bei Overflow
- Update-Intervall: 0.1 Sekunden (10 Hz)

## Bekannte Einschränkungen

### macOS
- ⚠️ macOS kann App-Nap aktivieren und die Event Loop verlangsamen
- Lösung: App im Vordergrund halten oder App-Nap deaktivieren

### Linux (Headless)
- ⚠️ Ohne X11/Wayland Display funktioniert Qt nicht
- Fallback: ConsolePixel wird automatisch verwendet

### Windows
- ✅ Sollte out-of-the-box funktionieren

## Troubleshooting-Checklist

- [ ] PyQt5 installiert? (`pip list | grep PyQt5`)
- [ ] DISPLAY gesetzt? (`echo $DISPLAY`)
- [ ] `init()` wird aufgerufen? (Log-Ausgabe prüfen)
- [ ] Test-Skripte funktionieren?
- [ ] Fenster minimiert? (Taskbar/Dock prüfen)
- [ ] Andere Displays? (Bei Multi-Monitor-Setup)

## Performance

- **CPU-Last:** ~1-2% pro LED-Streifen bei 10 Hz Update-Rate
- **Memory:** ~50-100 MB für Qt-Framework
- **Fenster-Updates:** Smooth bei 10 Hz (100ms Intervall)

