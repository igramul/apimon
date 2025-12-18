# QtPixel - Vertikale Anordnung

## Änderung

Die QtPixel-LEDs werden jetzt **vertikal** angeordnet, wobei **LED 0 unten** ist.

## Layout

```
┌─────────────────┐
│ AINT            │
│ (Pin: 18)  ███  │ ← LED 39 (oben)
│            ███  │ ← LED 38
│            ███  │ ← LED 37
│            ...  │
│            ███  │ ← LED 2
│            ███  │ ← LED 1
│            ███  │ ← LED 0 (unten)
└─────────────────┘
```

## Vorher vs. Nachher

### Vorher (horizontal):
```
┌────────────────────────────────────┐
│           AINT (Pin: 18)           │
│ ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■ │
│ 0 1 2 3 4 5 6 7 ... 37 38 39       │
└────────────────────────────────────┘
```

### Nachher (vertikal):
```
┌─────────────┐
│ AINT        │
│ (Pin: 18)   │
│        ███  │ ← 39 (oben)
│        ███  │ ← 38
│        ...  │
│        ███  │ ← 1
│        ███  │ ← 0 (unten)
└─────────────┘
```

## Technische Details

### LED-Größe
- **Vorher:** 20x20 Pixel (quadratisch)
- **Nachher:** 30x15 Pixel (rechteckig, breiter)

### Layout-Struktur
```python
main_layout = QHBoxLayout()  # Horizontal: Titel | LEDs
├─ title_label (links)
└─ led_layout (rechts) - QVBoxLayout (vertikal)
    ├─ LED[n-1] (oben im Display)
    ├─ LED[n-2]
    ├─ ...
    ├─ LED[1]
    └─ LED[0] (unten im Display)
```

### Fensterpositionierung
- **Vorher:** Untereinander (Y-Achse)
  - Fenster 0: (100, 100)
  - Fenster 1: (100, 220)
- **Nachher:** Nebeneinander (X-Achse)
  - Fenster 0: (100, 100)
  - Fenster 1: (300, 100)

## Code-Änderungen

### _create_window()
```python
# Erstelle LED-Labels in normaler Reihenfolge (0 bis n-1)
temp_labels = []
for i in range(self.n):
    led_label = QLabel()
    led_label.setFixedSize(30, 15)  # Breiter
    # ...
    temp_labels.append(led_label)

# Füge zum Layout in umgekehrter Reihenfolge hinzu
# (n-1 oben, 0 unten im Display)
for i in reversed(range(self.n)):
    led_layout.addWidget(temp_labels[i])

# Speichere in normaler Reihenfolge
# (Index entspricht LED-Nummer)
self._led_labels = temp_labels
```

### init()
```python
# Positioniere nebeneinander statt untereinander
self._window.move(100 + (self._instance_id * 200), 100)
```

## Test

```bash
python test_vertical_layout.py
```

**Erwartetes Verhalten:**
1. LED 0 (ROT) erscheint UNTEN
2. LED 7 (GRÜN) erscheint OBEN
3. Lauflicht von UNTEN nach OBEN (0→7)
4. Lauflicht von OBEN nach UNTEN (7→0)
5. Regenbogen von UNTEN (rot) nach OBEN (weiß)

## Warum diese Anordnung?

### Vorteile:
✅ Natürlichere Darstellung für physische LED-Streifen
✅ LED 0 (Status-LED) ist prominent unten positioniert
✅ Bessere Übersicht bei vielen LEDs (40 LEDs = ~600px Höhe)
✅ Fenster können nebeneinander platziert werden

### Nachteile:
⚠️ Höhere Fenster (benötigen mehr vertikalen Platz)
⚠️ Bei sehr vielen LEDs (>50) könnte Fenster zu hoch werden

## Anwendung in apimon.py

Bei 40 LEDs pro Strip:
- Fensterhöhe: ~600-700 Pixel (40 * 15 + Spacing + Titel)
- Fensterbreite: ~100 Pixel (Titel + LED + Margins)
- Zwei Strips nebeneinander: ~400 Pixel breit

Passt gut auf Standard-Bildschirme (1920x1080 oder höher).

## Zukünftige Erweiterungen (optional)

- [ ] LED-Nummern neben den LEDs anzeigen
- [ ] Zoom-Funktion für viele LEDs
- [ ] Horizontale/Vertikale Umschaltung per Config
- [ ] Auto-Layout basierend auf Bildschirmgröße

