from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor


class VisualizerWidget(QWidget):
    """Widget für die graphische Darstellung des Arrays"""
    
    def __init__(self):
        super().__init__()
        self.array = []
        self.highlight_indices = []
        self.setMinimumHeight(400)
        
    def set_array(self, array):
        self.array = array[:]
        self.update()
        
    def set_highlight(self, indices):
        self.highlight_indices = indices
        self.update()
        
    def paintEvent(self, event):
        if not self.array:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        n = len(self.array)
        
        bar_width = width / n
        max_value = max(self.array) if self.array else 1
        
        for i, value in enumerate(self.array):
            bar_height = (value / max_value) * (height - 20)
            x = i * bar_width
            y = height - bar_height
            
            # Farbe festlegen
            if i in self.highlight_indices:
                color = QColor(255, 100, 100)  # Rot für Vergleich
            else:
                color = QColor(100, 150, 255)  # Blau für normale Balken
            
            painter.fillRect(int(x), int(y), int(bar_width - 1), int(bar_height), color)
