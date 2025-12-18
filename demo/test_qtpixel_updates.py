#!/usr/bin/env python3
"""
Debug-Test für QtPixel Updates
Testet ob Updates nach der Initialisierung funktionieren
"""

import time
import logging
from app.qtpixel import QtPixel
from app.models.color import Color

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

def test_updates():
    logging.info("Erstelle QtPixel Instanz...")
    strip = QtPixel(pin=18, n=8, name="Debug-Test")

    logging.info("Initialisiere...")
    strip.init()

    logging.info("Setze initiale Farben (alle rot)...")
    strip.fill(Color.red.tuple)
    strip.show()

    logging.info("Warte 2 Sekunden...")
    time.sleep(2)

    logging.info("Starte Update-Loop (sollte alle 0.5s die Farbe ändern)...")

    colors = [
        ("Rot", Color.red.tuple),
        ("Grün", Color.green.tuple),
        ("Blau", Color.blue.tuple),
        ("Gelb", Color.yellow.tuple),
        ("Magenta", Color.magenta.tuple),
        ("Cyan", Color.cyan.tuple),
        ("Weiß", Color.white.tuple),
        ("Schwarz", Color.black.tuple),
    ]

    try:
        for i in range(100):  # 50 Sekunden
            color_name, color_tuple = colors[i % len(colors)]
            logging.info(f"Update {i+1}: Setze alle LEDs auf {color_name}")

            strip.fill(color_tuple)

            logging.debug(f"  LED[0] = {strip[0]}")
            logging.debug(f"  LED[1] = {strip[1]}")

            logging.debug("  Rufe show() auf...")
            strip.show()

            logging.debug("  Rufe processEvents() auf...")
            QtPixel.process_events()

            time.sleep(0.5)

    except KeyboardInterrupt:
        logging.info("Beende Test...")

    logging.info("Test abgeschlossen")


if __name__ == "__main__":
    test_updates()

