#!/usr/bin/env python3
"""
Vereinfachte Version von apimon.py zum Testen der QtPixel-Integration
Simuliert die gleiche Struktur wie die echte Anwendung mit QTimer
"""

import logging
import random
from app.neopixel_controller import NeoPixelController
from app.models.color import Color

# Prüfe ob Qt verfügbar ist
try:
    from app.qtpixel import QtPixel
    from PyQt5.QtCore import QTimer
    USING_QT = True
except (ImportError, ModuleNotFoundError):
    USING_QT = False

logging.basicConfig(level=logging.INFO)

def simulate_apimon():
    """
    Simuliert apimon.py mit QTimer für Updates (wie in der echten App)
    """
    print("=" * 60)
    print("APIMON Simulation - QtPixel Test mit QTimer")
    print("=" * 60)

    # Erstelle Controller wie in JiraTicketLedStripeList
    print("\n1. Erstelle LED-Streifen...")
    controllers = [
        NeoPixelController(led_count=40, gpio_pin=18, name="AINT", offset=0),
        NeoPixelController(led_count=40, gpio_pin=19, name="APIM", offset=1),
    ]

    print("   ✓ LED-Streifen erstellt")
    print("   ✓ Fenster sollten jetzt sichtbar sein!")
    print("   ✓ Initialisierungs-Animation läuft")

    # Simuliere Ticket-Daten
    print("\n2. Setze initiale Ticket-Daten...")

    def create_led_array(open_count, in_progress, deferred, checking):
        """Erstellt ein LED-Array basierend auf Ticket-Counts"""
        leds = [Color.black] * 40
        leds[0] = Color.white  # Status LED

        index = 1
        for _ in range(min(open_count, 10)):
            if index < 39:
                leds[index] = Color.red
                index += 1
        for _ in range(min(in_progress, 10)):
            if index < 39:
                leds[index] = Color.magenta
                index += 1
        for _ in range(min(deferred, 10)):
            if index < 39:
                leds[index] = Color.blue
                index += 1
        for _ in range(min(checking, 5)):
            if index < 39:
                leds[index] = Color.green
                index += 1

        return leds

    # Initiale Werte
    aint_leds = create_led_array(open_count=5, in_progress=3, deferred=8, checking=2)
    apim_leds = create_led_array(open_count=3, in_progress=5, deferred=6, checking=1)

    controllers[0].set_leds(aint_leds)
    controllers[1].set_leds(apim_leds)

    print("   ✓ Ticket-Daten gesetzt")

    if USING_QT:
        print("\n3. Verwende QTimer für LED-Updates (wie in apimon.py)...")

        # Timer für LED-Updates (100ms wie in apimon.py)
        pixel_timer = QTimer()
        pixel_timer.timeout.connect(lambda: [c.update() for c in controllers])
        pixel_timer.start(100)

        # Timer für Ticket-Updates (alle 10 Sekunden für Demo)
        update_counter = [0]  # Mutable für Lambda

        def update_tickets():
            update_counter[0] += 1
            seconds = update_counter[0] * 10
            print(f"\n[{seconds}s] Ticket-Update simuliert...")

            aint_leds = create_led_array(
                open_count=random.randint(2, 8),
                in_progress=random.randint(1, 6),
                deferred=random.randint(4, 12),
                checking=random.randint(0, 4)
            )
            apim_leds = create_led_array(
                open_count=random.randint(1, 7),
                in_progress=random.randint(2, 8),
                deferred=random.randint(3, 10),
                checking=random.randint(0, 3)
            )

            controllers[0].set_leds(aint_leds)
            controllers[1].set_leds(apim_leds)
            print("   ✓ LEDs aktualisiert")

        ticket_timer = QTimer()
        ticket_timer.timeout.connect(update_tickets)
        ticket_timer.start(10000)  # 10 Sekunden

        print("   ✓ QTimer gestartet (100ms für LEDs, 10s für Tickets)")
        print("   ✓ Drücke Ctrl+C zum Beenden\n")

        # Starte Qt Event Loop
        try:
            QtPixel.run_app()
        except KeyboardInterrupt:
            print("\n\n4. Beende Anwendung...")
            pixel_timer.stop()
            ticket_timer.stop()
            for controller in controllers:
                controller.clear()
            print("   ✓ LEDs gelöscht")
            print("\nFertig!")
    else:
        print("\n3. Qt nicht verfügbar - verwende einfache Loop...")
        print("   (Für Qt-Modus: pip install PyQt5)")

        import time
        try:
            counter = 0
            while True:
                for controller in controllers:
                    controller.update()

                if counter % 100 == 0 and counter > 0:
                    print(f"[{counter/10:.0f}s] Update...")

                time.sleep(0.1)
                counter += 1

        except KeyboardInterrupt:
            print("\nBeende...")
            for controller in controllers:
                controller.clear()


if __name__ == "__main__":
    simulate_apimon()

