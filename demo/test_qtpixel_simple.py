#!/usr/bin/env python3
"""
Einfacher Test für QtPixel ohne Animation
"""

import sys
from app.qtpixel import QtPixel
from app.models.color import Color


def test_basic():
    """Test basic functionality"""
    print("Erstelle LED-Streifen...")
    strip = QtPixel(pin=18, n=8, name="Test")

    print("Initialisiere...")
    strip.init()

    print("Setze Farben...")
    strip[0] = Color.red.tuple
    strip[1] = Color.green.tuple
    strip[2] = Color.blue.tuple
    strip[3] = Color.yellow.tuple
    strip[4] = Color.magenta.tuple
    strip[5] = Color.cyan.tuple
    strip[6] = Color.white.tuple
    strip[7] = Color.black.tuple

    print("Zeige LEDs...")
    strip.show()

    print("LEDs gesetzt. Liste:")
    for i in range(strip.n):
        print(f"  LED {i}: {strip[i]}")

    print("\nFenster sollte jetzt die Farben zeigen.")
    print("Teste Update in 2 Sekunden...")

    import time
    time.sleep(2)

    print("Ändere alle LEDs zu Rot...")
    strip.fill(Color.red.tuple)
    strip.show()

    print("Warte 2 Sekunden...")
    time.sleep(2)

    print("Ändere zu Grün...")
    strip.fill(Color.green.tuple)
    strip.show()

    print("Warte 2 Sekunden...")
    time.sleep(2)

    print("Test abgeschlossen. Fenster bleibt offen...")
    print("Drücke Ctrl+C zum Beenden")

    try:
        while True:
            QtPixel.process_events()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nBeendet.")
        sys.exit(0)


if __name__ == "__main__":
    test_basic()

