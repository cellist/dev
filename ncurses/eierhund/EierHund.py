#!/usr/bin/env python3
# Created with support from Claude Sonnet 4.5, inspired by
# Hans-Hermann Dubben, Hans-Peter Beck-Bornholdt: "Der Hund, der Eier legt"
import curses
import sys
import random
import time

class EierHund:
    def __init__(self, breite, hoehe, konfidenzintervall=40):
        """
        Initialisiert eine EierHund-Instanz mit einer 2D-Karte.
        
        Args:
            breite (int): Die Breite (x-Dimension) der Karte
            hoehe (int): Die Höhe (y-Dimension) der Karte
            konfidenzintervall (int): Prozentuale Abweichung vom Mittelwert für "normale" Werte
        """
        self.breite = breite
        self.hoehe = hoehe
        self.konfidenzintervall = konfidenzintervall
        self.iteration = 0
        # Erstelle eine 2D-Liste (Karte) mit Nullen initialisiert
        self.karte = [[0 for x in range(breite)] for y in range(hoehe)]
        # Berechne Erwartungswert (Coupon Collector's Problem)
        n = breite * hoehe
        self.erwartungswert = n * sum(1/i for i in range(1, n+1))
    
    def zeichneMich(self, stdscr):
        """
        Zeichnet die Karte mit ncurses im Terminal.
        
        Args:
            stdscr: Das ncurses Standard-Screen-Objekt
        """
        # Initialisiere Farben (nur beim ersten Aufruf)
        if not hasattr(self, '_farben_initialisiert'):
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Normal
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Über
            curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)   # Unter
            self._farben_initialisiert = True
        
        stdscr.clear()
        
        # Berechne Statistiken
        alle_werte = [wert for zeile in self.karte for wert in zeile]
        min_wert = min(alle_werte)
        max_wert = max(alle_werte)
        mittelwert = sum(alle_werte) / len(alle_werte)
        min_anzahl = alle_werte.count(min_wert)
        max_anzahl = alle_werte.count(max_wert)
        
        # Berechne Konfidenzgrenzen
        untere_grenze = mittelwert * (1 - self.konfidenzintervall / 100)
        obere_grenze = mittelwert * (1 + self.konfidenzintervall / 100)
        
        # Zeige Statistik oberhalb der Karte
        stdscr.addstr(0, 0, f"Iteration: {self.iteration} / Erwartungswert: {self.erwartungswert:.1f}  Konfidenzintervall: ±{self.konfidenzintervall}%")
        stdscr.addstr(1, 0, f"Min: {min_wert:03d} ({min_anzahl}x)  Max: {max_wert:03d} ({max_anzahl}x)  Mittelwert: {mittelwert:.2f}")
        stdscr.addstr(2, 0, f"Konfidenzbereich: {untere_grenze:.2f} - {obere_grenze:.2f}")
        stdscr.addstr(3, 0, "")  # Leerzeile
        
        # Zeichne die Karte (ab Zeile 4)
        start_zeile = 4
        for y in range(self.hoehe):
            # Obere Linie der Zellen
            linie = "+"
            for x in range(self.breite):
                linie += "-----+"
            stdscr.addstr(start_zeile + y * 2, 0, linie)
            
            # Inhalt der Zellen
            for x in range(self.breite):
                wert = self.karte[y][x]
                
                # Bestimme die Farbe basierend auf dem Konfidenzintervall
                if wert < untere_grenze:
                    farbe = curses.color_pair(3)  # Blau (unter)
                elif wert > obere_grenze:
                    farbe = curses.color_pair(2)  # Rot (über)
                else:
                    farbe = curses.color_pair(1)  # Grün (normal)
                
                # Zeichne die Zelle mit der entsprechenden Farbe
                if x == 0:
                    stdscr.addstr(start_zeile + y * 2 + 1, 0, "|")
                stdscr.addstr(start_zeile + y * 2 + 1, x * 6 + 1, f" {wert:03d} ", farbe)
                stdscr.addstr(start_zeile + y * 2 + 1, x * 6 + 6, "|")
        
        # Untere Abschlusslinie
        linie = "+"
        for x in range(self.breite):
            linie += "-----+"
        stdscr.addstr(start_zeile + self.hoehe * 2, 0, linie)
        
        stdscr.refresh()
    
    def erhoeheZufaellig(self):
        """
        Erhöht den Wert eines zufälligen Feldes um 1 und inkrementiert die Iteration.
        """
        x = random.randint(0, self.breite - 1)
        y = random.randint(0, self.hoehe - 1)
        self.karte[y][x] += 1
        self.iteration += 1
    
    def hatNullFelder(self):
        """
        Prüft, ob es noch Felder mit dem Wert 0 gibt.
        
        Returns:
            bool: True wenn noch Nullen vorhanden sind, False sonst
        """
        for zeile in self.karte:
            if 0 in zeile:
                return True
        return False
    
    def __repr__(self):
        """String-Repräsentation der EierHund-Instanz"""
        return f"EierHund(breite={self.breite}, hoehe={self.hoehe}, konfidenzintervall={self.konfidenzintervall})"


# Beispiel-Verwendung:
if __name__ == "__main__":
    # Prüfe Kommandozeilenargumente
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print(f"Verwendung: python {sys.argv[0]} <breite> <hoehe> [konfidenzintervall]")
        print(f"Beispiel: python {sys.argv[0]} 5 3 20")
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
        
        # Erstelle eine Instanz mit den angegebenen Dimensionen
        hund = EierHund(breite, hoehe, konfidenzintervall)
        
        # Funktion für die Animation mit ncurses
        def animiere(stdscr):
            # Schleife bis alle Felder erhöht wurden
            while hund.hatNullFelder():
                hund.erhoeheZufaellig()
                hund.zeichneMich(stdscr)
                time.sleep(0.3)  # 300ms Verzögerung
            
            # Zeige Endstatus und warte auf Tastendruck
            stdscr.addstr(hund.hoehe * 2 + 6, 0, "Fertig! Drücke eine Taste zum Beenden...")
            stdscr.refresh()
            stdscr.getch()
        
        # Starte die Animation mit ncurses
        curses.wrapper(animiere)
        
    except ValueError:
        print("Fehler: Breite und Höhe müssen ganze Zahlen sein!")
        sys.exit(1)
