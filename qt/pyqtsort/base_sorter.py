from abc import ABC, abstractmethod


class BaseSorter(ABC):
    """Abstrakte Basisklasse für alle Sortieralgorithmen"""
    
    def __init__(self, visualizer):
        self.visualizer = visualizer
        self.comparisons = 0
        self.swaps = 0
        self.compare_indices = []
        
    def swap(self, arr, i, j):
        """Tauscht zwei Elemente und aktualisiert die Visualisierung"""
        arr[i], arr[j] = arr[j], arr[i]
        self.swaps += 1
        self.visualizer.update_display(arr, [i, j])
        return True  # Signal für Pause
        
    def compare(self, arr, i, j):
        """Vergleicht zwei Elemente und hebt sie hervor"""
        self.comparisons += 1
        self.compare_indices = [i, j]
        self.visualizer.update_display(arr, [i, j])
        return arr[i] > arr[j]
    
    @abstractmethod
    def sort(self, arr):
        """Muss von jeder Unterklasse implementiert werden"""
        pass
    
    def reset_stats(self):
        """Setzt Statistiken zurück"""
        self.comparisons = 0
        self.swaps = 0
