#!/usr/bin/env python3
# Created with support from Claude Sonnet 4.5, inspired by
# Hans-Hermann Dubben, Hans-Peter Beck-Bornholdt: "Der Hund, der Eier legt"
import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLabel, QPushButton, QSlider, QGridLayout, QScrollArea)
from PyQt6.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QPainter, QColor, QFont, QPen
from PyQt6.QtCharts import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis


class AnimatedCell(QWidget):
    """Eine animierte Zelle in der Karte"""
    
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self._value = 0
        self._color = QColor(100, 200, 100)  # Grün als Standard
        self.setMinimumSize(60, 60)
        self.setMaximumSize(120, 120)
        self._animation_progress = 0.0
        
    def get_value(self):
        return self._value
    
    def set_value(self, value):
        self._value = value
        self.update()
    
    value = pyqtProperty(int, get_value, set_value)
    
    def get_animation_progress(self):
        return self._animation_progress
    
    def set_animation_progress(self, progress):
        self._animation_progress = progress
        self.update()
    
    animation_progress = pyqtProperty(float, get_animation_progress, set_animation_progress)
    
    def increment_with_animation(self):
        """Erhöht den Wert mit Animation"""
        self._value += 1
        
        # Puls-Animation
        self.animation = QPropertyAnimation(self, b"animation_progress")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        self.animation.start()
        
        self.update()
    
    def set_color(self, color):
        """Setzt die Farbe der Zelle"""
        self._color = color
        self.update()
    
    def paintEvent(self, event):
        """Zeichnet die Zelle"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Berechne Größe mit Animation
        scale = 1.0 + (self._animation_progress * 0.2)
        rect = self.rect()
        center_x = rect.width() / 2
        center_y = rect.height() / 2
        size = min(rect.width(), rect.height()) - 10
        scaled_size = size * scale
        
        # Zeichne Hintergrund mit Farbverlauf
        painter.setBrush(self._color)
        painter.setPen(QPen(QColor(50, 50, 50), 2))
        
        x = center_x - scaled_size / 2
        y = center_y - scaled_size / 2
        painter.drawRoundedRect(int(x), int(y), int(scaled_size), int(scaled_size), 10, 10)
        
        # Zeichne Wert
        painter.setPen(QColor(255, 255, 255))
        font = QFont("Arial", 16, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{self._value:03d}")


class EierHundQt(QMainWindow):
    """Qt6 Version der EierHund Klasse"""
    
    def __init__(self, breite, hoehe, konfidenzintervall=40):
        super().__init__()
        self.breite = breite
        self.hoehe = hoehe
        self.konfidenzintervall = konfidenzintervall
        self.iteration = 0
        self.is_paused = False
        self.speed = 300  # ms
        
        # Berechne Erwartungswert
        n = breite * hoehe
        self.erwartungswert = n * sum(1/i for i in range(1, n+1))
        
        # Erstelle Karte mit AnimatedCell Objekten
        self.karte = [[AnimatedCell(x, y) for x in range(breite)] for y in range(hoehe)]
        
        self.initUI()
        
        # Timer für Animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_step)
        
    def initUI(self):
        """Initialisiert die Benutzeroberfläche"""
        self.setWindowTitle('EierHund Qt6 Visualisierung')
        
        # Fenster auf 90% der Bildschirmgröße setzen
        screen = QApplication.primaryScreen().geometry()
        window_width = int(screen.width() * 0.9)
        window_height = int(screen.height() * 0.9)
        self.setGeometry(
            int((screen.width() - window_width) / 2),
            int((screen.height() - window_height) / 2),
            window_width,
            window_height
        )
        
        # Haupt-Widget und Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        
        # Statistik-Label
        self.stats_label = QLabel()
        self.stats_label.setFont(QFont("Arial", 11))
        self.stats_label.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        self.stats_label.setWordWrap(True)
        main_layout.addWidget(self.stats_label)
        
        # Scroll-Bereich für Karten-Grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        grid_widget = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(3)
        grid_widget.setLayout(self.grid_layout)
        
        for y in range(self.hoehe):
            for x in range(self.breite):
                self.grid_layout.addWidget(self.karte[y][x], y, x)
        
        scroll_area.setWidget(grid_widget)
        main_layout.addWidget(scroll_area, 1)  # Stretch-Faktor 1
        
        # Histogramm
        self.create_histogram()
        main_layout.addWidget(self.chart_view)
        
        # Kontroll-Panel
        control_layout = QHBoxLayout()
        
        # Start/Pause Button
        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.toggle_animation)
        self.start_button.setStyleSheet("QPushButton { font-size: 14px; padding: 10px; }")
        control_layout.addWidget(self.start_button)
        
        # Geschwindigkeits-Slider
        speed_label = QLabel('Geschwindigkeit:')
        control_layout.addWidget(speed_label)
        
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(50)
        self.speed_slider.setMaximum(1000)
        self.speed_slider.setValue(300)
        self.speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.speed_slider.setTickInterval(100)
        self.speed_slider.valueChanged.connect(self.change_speed)
        control_layout.addWidget(self.speed_slider)
        
        self.speed_value_label = QLabel('300 ms')
        control_layout.addWidget(self.speed_value_label)
        
        main_layout.addLayout(control_layout)
        
        self.update_statistics()
        
    def create_histogram(self):
        """Erstellt das Histogramm für die Wertverteilung"""
        self.chart = QChart()
        self.chart.setTitle("Verteilung der Werte")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setMaximumHeight(250)
        
    def update_histogram(self):
        """Aktualisiert das Histogramm"""
        self.chart.removeAllSeries()
        
        # Sammle alle Werte
        alle_werte = [self.karte[y][x].value for y in range(self.hoehe) for x in range(self.breite)]
        
        if not alle_werte or max(alle_werte) == 0:
            return
        
        # Erstelle Histogram-Daten
        max_wert = max(alle_werte)
        bins = min(10, max_wert + 1)
        bin_size = (max_wert + 1) / bins
        
        histogram = [0] * bins
        for wert in alle_werte:
            bin_index = min(int(wert / bin_size), bins - 1)
            histogram[bin_index] += 1
        
        # Erstelle Bar-Serie
        bar_set = QBarSet("Anzahl")
        for count in histogram:
            bar_set.append(count)
        
        series = QBarSeries()
        series.append(bar_set)
        
        self.chart.addSeries(series)
        
        # Achsen
        categories = [f"{int(i*bin_size)}-{int((i+1)*bin_size-1)}" for i in range(bins)]
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        self.chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        axis_y.setRange(0, max(histogram) + 1)
        self.chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)
        
    def update_statistics(self):
        """Aktualisiert die Statistik-Anzeige"""
        alle_werte = [self.karte[y][x].value for y in range(self.hoehe) for x in range(self.breite)]
        
        if alle_werte:
            min_wert = min(alle_werte)
            max_wert = max(alle_werte)
            mittelwert = sum(alle_werte) / len(alle_werte)
            min_anzahl = alle_werte.count(min_wert)
            max_anzahl = alle_werte.count(max_wert)
            
            # Berechne Konfidenzgrenzen
            untere_grenze = mittelwert * (1 - self.konfidenzintervall / 100)
            obere_grenze = mittelwert * (1 + self.konfidenzintervall / 100)
            
            stats_text = (
                f"<b>Iteration:</b> {self.iteration} / <b>Erwartungswert:</b> {self.erwartungswert:.1f} "
                f"| <b>Konfidenzintervall:</b> ±{self.konfidenzintervall}%<br>"
                f"<b>Min:</b> {min_wert:03d} ({min_anzahl}x) | "
                f"<b>Max:</b> {max_wert:03d} ({max_anzahl}x) | "
                f"<b>Mittelwert:</b> {mittelwert:.2f}<br>"
                f"<b>Konfidenzbereich:</b> {untere_grenze:.2f} - {obere_grenze:.2f}"
            )
            
            self.stats_label.setText(stats_text)
            
            # Aktualisiere Farben
            self.update_colors(mittelwert, untere_grenze, obere_grenze)
    
    def update_colors(self, mittelwert, untere_grenze, obere_grenze):
        """Aktualisiert die Farben aller Zellen basierend auf dem Konfidenzintervall"""
        for y in range(self.hoehe):
            for x in range(self.breite):
                wert = self.karte[y][x].value
                
                if wert < untere_grenze:
                    # Blau (unter)
                    self.karte[y][x].set_color(QColor(70, 130, 220))
                elif wert > obere_grenze:
                    # Rot (über)
                    self.karte[y][x].set_color(QColor(220, 70, 70))
                else:
                    # Grün (normal)
                    self.karte[y][x].set_color(QColor(70, 200, 120))
    
    def erhoeheZufaellig(self):
        """Erhöht ein zufälliges Feld"""
        x = random.randint(0, self.breite - 1)
        y = random.randint(0, self.hoehe - 1)
        self.karte[y][x].increment_with_animation()
        self.iteration += 1
    
    def hatNullFelder(self):
        """Prüft ob noch Nullfelder existieren"""
        for y in range(self.hoehe):
            for x in range(self.breite):
                if self.karte[y][x].value == 0:
                    return True
        return False
    
    def update_step(self):
        """Ein Schritt der Animation"""
        if not self.hatNullFelder():
            self.timer.stop()
            self.start_button.setText('Fertig!')
            self.start_button.setEnabled(False)
            return
        
        self.erhoeheZufaellig()
        self.update_statistics()
        self.update_histogram()
    
    def toggle_animation(self):
        """Startet/Pausiert die Animation"""
        if self.timer.isActive():
            self.timer.stop()
            self.start_button.setText('Fortsetzen')
            self.is_paused = True
        else:
            self.timer.start(self.speed)
            self.start_button.setText('Pause')
            self.is_paused = False
    
    def change_speed(self, value):
        """Ändert die Geschwindigkeit"""
        self.speed = value
        self.speed_value_label.setText(f'{value} ms')
        if self.timer.isActive():
            self.timer.setInterval(value)


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print(f"Verwendung: python {sys.argv[0]} <breite> <hoehe> [konfidenzintervall]")
        print(f"Beispiel: python {sys.argv[0]} 5 3 40")
        print(f"Konfidenzintervall ist optional (Standard: 40)")
        sys.exit(1)
    
    try:
        breite = int(sys.argv[1])
        hoehe = int(sys.argv[2])
        konfidenzintervall = int(sys.argv[3]) if len(sys.argv) == 4 else 40
        
        if breite <= 0 or hoehe <= 0:
            print("Fehler: Breite und Höhe müssen positive Zahlen sein!")
            sys.exit(1)
        
        if konfidenzintervall <= 0 or konfidenzintervall > 100:
            print("Fehler: Konfidenzintervall muss zwischen 1 und 100 liegen!")
            sys.exit(1)
        
        app = QApplication(sys.argv)
        window = EierHundQt(breite, hoehe, konfidenzintervall)
        window.show()
        sys.exit(app.exec())
        
    except ValueError:
        print("Fehler: Breite, Höhe und Konfidenzintervall müssen ganze Zahlen sein!")
        sys.exit(1)


if __name__ == '__main__':
    main()
