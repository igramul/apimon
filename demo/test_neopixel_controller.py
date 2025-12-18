#!/usr/bin/env python3
"""
Test-Skript um zu prüfen, ob QtPixel mit NeoPixelController funktioniert
"""

import time
import logging
from app.neopixel_controller import NeoPixelController
from app.models.color import Color

logging.basicConfig(level=logging.INFO)

def main():
    print("Erstelle NeoPixelController...")

    # Erstelle zwei Controller wie in der echten Anwendung
    controller1 = NeoPixelController(led_count=16, gpio_pin=18, name="AINT", offset=0)
    controller2 = NeoPixelController(led_count=16, gpio_pin=19, name="APIM", offset=1)

    print("Controller erstellt. Fenster sollten jetzt sichtbar sein.")
    print("Teste LED-Updates...")

    # Setze einige LEDs
    leds1 = [Color.black] * 16
    leds1[0] = Color.white  # Status LED
    leds1[1] = Color.red
    leds1[2] = Color.red
    leds1[3] = Color.green
    leds1[4] = Color.blue

    leds2 = [Color.black] * 16
    leds2[0] = Color.white  # Status LED
    leds2[1] = Color.yellow
    leds2[2] = Color.magenta
    leds2[3] = Color.cyan

    controller1.set_leds(leds1)
    controller2.set_leds(leds2)

    print("Starte Update-Loop (wie im echten apimon mit 0.1s Intervall)...")
    print("Drücke Ctrl+C zum Beenden")

    try:
        counter = 0
        while True:
            # Update wie im Scheduler
            controller1.update()
            controller2.update()

            # Alle 5 Sekunden Farben ändern
            if counter % 50 == 0:
                print(f"Update {counter/10:.1f}s - Ändere Farben...")
                # Rotiere die Farben
                temp = leds1[1]
                for i in range(1, len(leds1) - 1):
                    leds1[i] = leds1[i + 1]
                leds1[-2] = temp

                controller1.set_leds(leds1)

            time.sleep(0.1)  # Wie im Scheduler
            counter += 1

    except KeyboardInterrupt:
        print("\nBeende...")
        controller1.clear()
        controller2.clear()
        print("Fertig.")


if __name__ == "__main__":
    main()

