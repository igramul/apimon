from typing import List, Tuple, Optional
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

from .models.color import Color


class QtPixel(List[Tuple[int, int, int]]):
    """
    NeoPixel Duck Typing Class for Qt GUI
    Displays LEDs graphically using PyQt5
    """

    _instance_counter = 0  # Klassenvariable für den Enumerator
    _app = None  # Gemeinsame QApplication für alle Instanzen
    _windows = []  # Liste aller Fenster

    def __init__(self, pin: Optional[int], n: int, name: str):
        super().__init__([Color.black.tuple] * n)
        self.pin = pin
        self.name = name
        # Jede Instanz bekommt ihre eigene Nummer
        self._instance_id = QtPixel._instance_counter
        QtPixel._instance_counter += 1

        # Qt Application initialisieren (nur einmal)
        if QtPixel._app is None:
            QtPixel._app = QApplication.instance()
            if QtPixel._app is None:
                QtPixel._app = QApplication(sys.argv)

        # Fenster erstellen
        self._window = None
        self._led_labels = []
        self._create_window()

    def _create_window(self):
        """Erstellt das Qt Fenster mit den LED-Widgets - vertikal, LED 0 unten"""
        self._window = QWidget()
        self._window.setWindowTitle(f'LED Strip: {self.name}')

        # Hauptlayout: Horizontal mit Titel links und LEDs rechts
        main_layout = QHBoxLayout()

        # Titel Label (links)
        title_label = QLabel(f'{self.name}\n(Pin: {self.pin})')
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # LED Container - VERTIKAL von oben nach unten
        led_layout = QVBoxLayout()
        led_layout.setSpacing(3)

        # LED Labels erstellen
        # Durchlaufe von n-1 bis 0 (von oben nach unten im Display)
        # aber speichere in normaler Reihenfolge im Array
        temp_labels = []
        for i in range(self.n):
            led_label = QLabel()
            led_label.setFixedSize(30, 15)  # Breiter für vertikale Anordnung
            led_label.setAutoFillBackground(True)
            # Initial mit schwarz
            color = Color.black.tuple
            led_label.setStyleSheet(f"background-color: rgb({color[0]}, {color[1]}, {color[2]}); border: 1px solid black; border-radius: 5px;")
            temp_labels.append(led_label)

        # Füge Labels in umgekehrter Reihenfolge zum Layout hinzu
        # (LED n-1 oben, LED 0 unten)
        for i in reversed(range(self.n)):
            led_layout.addWidget(temp_labels[i])

        # Speichere in normaler Reihenfolge (Index = LED-Nummer)
        self._led_labels = temp_labels

        main_layout.addLayout(led_layout)
        self._window.setLayout(main_layout)

        # Fenster zur Liste hinzufügen
        QtPixel._windows.append(self._window)

    def _set_led_color(self, label: QLabel, color: Tuple[int, int, int]):
        """Setzt die Farbe eines LED Labels"""
        label.setStyleSheet(f"background-color: rgb({color[0]}, {color[1]}, {color[2]}); border: 1px solid black; border-radius: 10px;")

    def init(self):
        """Initialisiert die LED-Anzeige"""
        self._window.show()
        # Positioniere Fenster nebeneinander (da vertikal)
        self._window.move(100 + (self._instance_id * 200), 100)

    def fill(self, color):
        """Füllt alle LEDs mit der gleichen Farbe"""
        for i in range(self.n):
            self[i] = color

    def show(self):
        """Aktualisiert die Anzeige"""
        # Update alle LED-Farben
        for i, color_tuple in enumerate(self):
            if i < len(self._led_labels):
                self._set_led_color(self._led_labels[i], color_tuple)

        # Qt Event Loop verarbeiten - NUR EINMAL um Rekursion zu vermeiden
        if QtPixel._app:
            QtPixel._app.processEvents()

    @property
    def n(self):
        return len(self)

    @staticmethod
    def run_app():
        """Startet die Qt Event Loop (blockierend)"""
        if QtPixel._app:
            sys.exit(QtPixel._app.exec_())

    @staticmethod
    def process_events():
        """Verarbeitet Qt Events ohne zu blockieren"""
        if QtPixel._app:
            QtPixel._app.processEvents()

