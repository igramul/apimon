# QtPixel - Grafische LED-Anzeige

## Übersicht

`QtPixel` ist eine Duck-Typing-Implementierung für NeoPixel LED-Streifen, die die LEDs grafisch mit PyQt5 darstellt. Diese Klasse wird automatisch verwendet, wenn die Software auf einem Mac oder PC läuft (nicht auf einem Raspberry Pi).

## Features

- **Grafische Darstellung**: Jede LED wird als farbiger Kreis in einem Qt-Fenster dargestellt
- **Multi-Strip Support**: Mehrere LED-Streifen können gleichzeitig angezeigt werden
- **Automatische Fensterverwaltung**: Jede Instanz erhält ein eigenes Fenster, das automatisch positioniert wird
- **Kompatibles Interface**: Implementiert das gleiche Interface wie die Hardware-LED-Klassen

## Installation

PyQt5 wird automatisch installiert, wenn `pip install -r requirements.txt` auf einem Nicht-Raspberry-Pi-System ausgeführt wird:

```bash
pip install -r requirements.txt
```

## Verwendung

### Basis-Verwendung

```python
from app.qtpixel import QtPixel
from app.models.color import Color

# LED-Streifen erstellen
strip = QtPixel(pin=18, n=16, name="AINT")

# Initialisieren (Fenster anzeigen)
strip.init()

# Einzelne LEDs setzen
strip[0] = Color.red.tuple
strip[1] = Color.green.tuple
strip[2] = Color.blue.tuple

# Alle LEDs auf einmal setzen
strip.fill(Color.white.tuple)

# Änderungen anzeigen
strip.show()

# Qt Events verarbeiten (wichtig in Loops!)
QtPixel.process_events()
```

### Mehrere LED-Streifen

```python
from app.qtpixel import QtPixel
from app.models.color import Color

# Zwei Streifen erstellen
strip1 = QtPixel(pin=18, n=16, name="AINT")
strip2 = QtPixel(pin=19, n=16, name="APIM")

# Initialisieren
strip1.init()
strip2.init()

# LEDs setzen
strip1.fill(Color.red.tuple)
strip2.fill(Color.blue.tuple)

# Anzeigen
strip1.show()
strip2.show()
```

### Animation-Loop

```python
import time
from app.qtpixel import QtPixel
from app.models.color import Color

strip = QtPixel(pin=18, n=16, name="AINT")
strip.init()

try:
    while True:
        # Animation...
        for i in range(strip.n):
            strip[i] = Color.random.tuple
        
        strip.show()
        time.sleep(0.1)
        
        # WICHTIG: Qt Events verarbeiten!
        QtPixel.process_events()
        
except KeyboardInterrupt:
    print("Beendet")
```

## API

### Konstruktor

```python
QtPixel(pin: None, n: int, name: str)
```

- `pin`: GPIO-Pin-Nummer (wird nur für die Anzeige verwendet)
- `n`: Anzahl der LEDs
- `name`: Name des LED-Streifens (wird im Fenstertitel angezeigt)

### Methoden

#### `init()`
Zeigt das Fenster an und positioniert es automatisch.

#### `fill(color: tuple)`
Füllt alle LEDs mit der gleichen Farbe.

#### `show()`
Aktualisiert die grafische Darstellung mit den aktuellen LED-Farben.

#### `__setitem__(key: int, value: tuple)`
Setzt die Farbe einer einzelnen LED (inherited from List).

```python
strip[0] = (255, 0, 0)  # Rot
```

### Properties

#### `n`
Gibt die Anzahl der LEDs zurück.

```python
led_count = strip.n
```

### Statische Methoden

#### `process_events()`
Verarbeitet Qt Events ohne zu blockieren. MUSS in Animations-Loops aufgerufen werden!

```python
QtPixel.process_events()
```

#### `run_app()`
Startet die Qt Event Loop (blockierend). Nur verwenden, wenn keine andere Event-Behandlung benötigt wird.

```python
QtPixel.run_app()  # Blockiert bis Fenster geschlossen werden
```

## Interne Funktionsweise

### Instanz-Zähler
Jede QtPixel-Instanz erhält eine eindeutige ID (`_instance_id`), die von einem Klassenzähler (`_instance_counter`) stammt. Diese ID wird verwendet, um die Fenster automatisch zu positionieren.

### QApplication-Verwaltung
Alle QtPixel-Instanzen teilen sich eine gemeinsame `QApplication`-Instanz (`_app`). Diese wird beim ersten Erstellen einer QtPixel-Instanz automatisch initialisiert.

### Fenster-Liste
Alle erstellten Fenster werden in der Klassenvariable `_windows` gespeichert.

## Integration mit dem Projekt

Die `QtPixel`-Klasse wird automatisch vom `neopixel_controller.py` verwendet, wenn:
1. Die Hardware-LED-Bibliotheken nicht verfügbar sind (z.B. auf Mac/PC)
2. PyQt5 installiert ist

Die Import-Hierarchie ist:
1. `neopixelwrapper.Pixel` (CircuitPython)
2. `rpi_ws281x_pixel.Pixel` (rpi_ws281x)
3. `qtpixel.QtPixel` (PyQt5) ← **NEU**
4. `consolepixel.ConsolePixel` (Fallback)

## Demo

Führe das Demo-Skript aus, um die QtPixel-Funktionalität zu testen:

```bash
python demo_qtpixel.py
```

Dies zeigt zwei animierte LED-Streifen in separaten Fenstern.

## Troubleshooting

### PyQt5 Import-Fehler
Stelle sicher, dass PyQt5 installiert ist:
```bash
pip install PyQt5==5.15.11
```

### Fenster werden nicht angezeigt
Stelle sicher, dass `init()` nach dem Erstellen der QtPixel-Instanz aufgerufen wird:
```python
strip = QtPixel(pin=18, n=16, name="Test")
strip.init()  # Wichtig!
```

### Fenster reagiert nicht
In Animations-Loops muss `QtPixel.process_events()` regelmäßig aufgerufen werden:
```python
while True:
    # ... Animation code ...
    QtPixel.process_events()  # Wichtig!
```

## Plattform-Spezifische Installation

Die `requirements.txt` installiert PyQt5 nur auf Nicht-Raspberry-Pi-Systemen:

```
PyQt5==5.15.11; platform_system != "Linux" or (platform_machine != "armv7l" and platform_machine != "aarch64")
```

Auf einem Raspberry Pi wird stattdessen `rpi_ws281x` installiert:

```
rpi_ws281x==5.0.0; platform_system == "Linux" and (platform_machine == "armv7l" or platform_machine == "aarch64")
```

