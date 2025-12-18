#!/usr/bin/env python3
"""
Demo script to test QtPixel class
Shows how LEDs are displayed graphically using Qt
"""

import time
import sys
from app.qtpixel import QtPixel
from app.models.color import Color


def main():
    # Erstelle zwei LED-Streifen
    strip1 = QtPixel(pin=18, n=16, name="AINT")
    strip2 = QtPixel(pin=19, n=16, name="APIM")

    # Initialisiere die Anzeige
    strip1.init()
    strip2.init()

    # Setze einige Farben
    for i in range(strip1.n):
        if i < 4:
            strip1[i] = Color.red.tuple
        elif i < 8:
            strip1[i] = Color.green.tuple
        elif i < 12:
            strip1[i] = Color.blue.tuple
        else:
            strip1[i] = Color.yellow.tuple

    for i in range(strip2.n):
        if i % 2 == 0:
            strip2[i] = Color.magenta.tuple
        else:
            strip2[i] = Color.cyan.tuple

    # Zeige die LEDs an
    strip1.show()
    strip2.show()

    print("Qt LED Display gestartet. Fenster sollten nun sichtbar sein.")
    print("Drücke Ctrl+C zum Beenden...")

    # Animationsloop
    try:
        counter = 0
        while True:
            # Rotiere die Farben von strip1
            temp = strip1[0]
            for i in range(strip1.n - 1):
                strip1[i] = strip1[i + 1]
            strip1[strip1.n - 1] = temp
            strip1.show()

            # Debug: Zeige die erste LED-Farbe
            if counter % 10 == 0:
                print(f"Counter: {counter}, Strip1[0]: {strip1[0]}, Strip2[0]: {strip2[0]}")

            # Blinke strip2
            if counter % 2 == 0:
                strip2.fill(Color.white.tuple)
            else:
                strip2.fill(Color.black.tuple)
            strip2.show()

            counter += 1
            time.sleep(0.5)

            # Qt Events verarbeiten
            QtPixel.process_events()

    except KeyboardInterrupt:
        print("\nBeende...")
        sys.exit(0)


if __name__ == "__main__":
    main()

