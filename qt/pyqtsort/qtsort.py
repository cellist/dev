#!/usr/bin/env python3
import sys
import random
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QComboBox, QSlider, QLabel)
from PyQt6.QtCore import Qt, QTimer

from visualizer_widget import VisualizerWidget
from sorters.bubble_sort import BubbleSort
from sorters.selection_sort import SelectionSort
from sorters.insertion_sort import InsertionSort
from sorters.quick_sort import QuickSort
from sorters.merge_sort import MergeSort
from sorters.heap_sort import HeapSort
from sorters.radix_sort import RadixSort
from sorters.shell_sort import ShellSort
from sorters.cocktail_sort import CocktailSort
from sorters.comb_sort import CombSort
from sorters.gnome_sort import GnomeSort


class SortingVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sortieralgorithmus-Visualisierer")
        self.setGeometry(100, 100, 1200, 700)
        
        # Array initialisieren
        self.array_size = 100
        self.array = []
        self.generate_array()
        
        # Sortieralgorithmen
        self.sorters = {
            "Bubble Sort": BubbleSort(self),
            "Selection Sort": SelectionSort(self),
            "Insertion Sort": InsertionSort(self),
            "Quick Sort": QuickSort(self),
            "Merge Sort": MergeSort(self),
            "Heap Sort": HeapSort(self),
            "Radix Sort": RadixSort(self),
	    "Shell Sort": ShellSort(self),
	    "Cocktail Sort": CocktailSort(self),
	    "Comb Sort": CombSort(self),
	    "Gnome Sort": GnomeSort(self)
        }
        self.current_sorter = None
        self.sort_generator = None
        
        # Timer für Animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.sort_step)
        self.sorting = False
        self.start_time = 0
        
        self.init_ui()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Visualizer Widget
        self.visualizer = VisualizerWidget()
        self.visualizer.set_array(self.array)
        main_layout.addWidget(self.visualizer)
        
        # Statistik Labels
        stats_layout = QHBoxLayout()
        self.label_comparisons = QLabel("Vergleiche: 0")
        self.label_swaps = QLabel("Vertauschungen: 0")
        self.label_time = QLabel("Zeit: 0.00s")
        stats_layout.addWidget(self.label_comparisons)
        stats_layout.addWidget(self.label_swaps)
        stats_layout.addWidget(self.label_time)
        stats_layout.addStretch()
        main_layout.addLayout(stats_layout)
        
        # Kontroll-Layout
        control_layout = QHBoxLayout()
        
        # Algorithmus-Auswahl
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(self.sorters.keys())
        control_layout.addWidget(QLabel("Algorithmus:"))
        control_layout.addWidget(self.algo_combo)
        
        # Geschwindigkeits-Slider
        control_layout.addWidget(QLabel("Geschwindigkeit:"))
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(200)
        self.speed_slider.setValue(50)
        self.speed_slider.setFixedWidth(200)
        control_layout.addWidget(self.speed_slider)
        
        # Buttons
        self.btn_shuffle = QPushButton("Mischen")
        self.btn_shuffle.clicked.connect(self.shuffle_array)
        control_layout.addWidget(self.btn_shuffle)
        
        self.btn_start = QPushButton("Start")
        self.btn_start.clicked.connect(self.toggle_sorting)
        control_layout.addWidget(self.btn_start)
        
        control_layout.addStretch()
        main_layout.addLayout(control_layout)
        
    def generate_array(self):
        """Generiert ein neues zufälliges Array"""
        self.array = list(range(1, self.array_size + 1))
        random.shuffle(self.array)
        
    def shuffle_array(self):
        """Mischt das Array neu"""
        if self.sorting:
            return
        self.generate_array()
        self.visualizer.set_array(self.array)
        self.reset_stats()
        
    def toggle_sorting(self):
        """Startet oder stoppt den Sortiervorgang"""
        if self.sorting:
            self.stop_sorting()
        else:
            self.start_sorting()
            
    def start_sorting(self):
        """Startet den Sortiervorgang"""
        algo_name = self.algo_combo.currentText()
        self.current_sorter = self.sorters[algo_name]
        self.current_sorter.reset_stats()
        
        self.sort_generator = self.current_sorter.sort(self.array)
        self.sorting = True
        self.start_time = time.time()
        self.btn_start.setText("Stop")
        self.btn_shuffle.setEnabled(False)
        self.algo_combo.setEnabled(False)
        
        delay = 201 - self.speed_slider.value()
        self.timer.start(delay)
        
    def stop_sorting(self):
        """Stoppt den Sortiervorgang"""
        self.sorting = False
        self.timer.stop()
        self.btn_start.setText("Start")
        self.btn_shuffle.setEnabled(True)
        self.algo_combo.setEnabled(True)
        
    def sort_step(self):
        """Führt einen Schritt des Sortieralgorithmus aus"""
        try:
            next(self.sort_generator)
            self.update_stats()
            
            # Geschwindigkeit anpassen
            delay = 201 - self.speed_slider.value()
            self.timer.setInterval(delay)
        except StopIteration:
            self.stop_sorting()
            self.visualizer.set_highlight([])
            
    def update_display(self, arr, highlight_indices):
        """Aktualisiert die Visualisierung"""
        self.array = arr[:]
        self.visualizer.set_array(self.array)
        self.visualizer.set_highlight(highlight_indices)
        QApplication.processEvents()
        
    def update_stats(self):
        """Aktualisiert die Statistik-Anzeige"""
        if self.current_sorter:
            self.label_comparisons.setText(f"Vergleiche: {self.current_sorter.comparisons}")
            self.label_swaps.setText(f"Vertauschungen: {self.current_sorter.swaps}")
            elapsed = time.time() - self.start_time
            self.label_time.setText(f"Zeit: {elapsed:.2f}s")
            
    def reset_stats(self):
        """Setzt die Statistiken zurück"""
        self.label_comparisons.setText("Vergleiche: 0")
        self.label_swaps.setText("Vertauschungen: 0")
        self.label_time.setText("Zeit: 0.00s")


def main():
    app = QApplication(sys.argv)
    window = SortingVisualizer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
