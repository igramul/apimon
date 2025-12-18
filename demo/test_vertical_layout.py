#!/usr/bin/env python3
"""
Test für vertikale LED-Anordnung
LED 0 ist unten, LED n-1 ist oben
"""

import time
from app.qtpixel import QtPixel
from app.models.color import Color


def test_vertical_layout():
    print("Test: Vertikale LED-Anordnung")
    print("LED 0 sollte UNTEN sein")
    print("LED 7 sollte OBEN sein\n")

    # Erstelle einen Strip mit 8 LEDs
    strip = QtPixel(pin=18, n=8, name="Vertical Test")
    strip.init()

    print("1. Setze LED 0 (unten) auf ROT...")
    strip[0] = Color.red.tuple
    strip.show()
    time.sleep(2)

    print("2. Setze LED 7 (oben) auf GRÜN...")
    strip[7] = Color.green.tuple
    strip.show()
    time.sleep(2)

    print("3. Lauflicht von UNTEN nach OBEN (0 → 7)...")
    for i in range(8):
        # Alle schwarz
        for j in range(8):
            strip[j] = Color.black.tuple
        # Aktuelle LED blau
        strip[i] = Color.blue.tuple
        print(f"   LED {i} leuchtet (Position von unten: {i})")
        strip.show()
        time.sleep(0.5)

    print("\n4. Lauflicht von OBEN nach UNTEN (7 → 0)...")
    for i in reversed(range(8)):
        # Alle schwarz
        for j in range(8):
            strip[j] = Color.black.tuple
        # Aktuelle LED gelb
        strip[i] = Color.yellow.tuple
        print(f"   LED {i} leuchtet (Position von unten: {i})")
        strip.show()
        time.sleep(0.5)

    print("\n5. Färbe alle LEDs von unten nach oben ein...")
    colors = [
        Color.red,      # 0 - unten
        Color.orange,   # 1
        Color.yellow,   # 2
        Color.green,    # 3
        Color.cyan,     # 4
        Color.blue,     # 5
        Color.magenta,  # 6
        Color.white,    # 7 - oben
    ]

    for i, color in enumerate(colors):
        strip[i] = color.tuple
        print(f"   LED {i}: {color}")

    strip.show()

    print("\nAlle LEDs gesetzt - Regenbogen von UNTEN (rot) nach OBEN (weiß)")
    print("Drücke Ctrl+C zum Beenden...")

    try:
        while True:
            QtPixel.process_events()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nTest beendet.")


if __name__ == "__main__":
    test_vertical_layout()

