from base_sorter import BaseSorter


class CombSort(BaseSorter):
    """Comb Sort - Verbesserung von Bubble Sort mit schrumpfendem Gap"""
    
    def sort(self, arr):
        n = len(arr)
        gap = n
        shrink = 1.3  # Schrumpffaktor
        sorted_flag = False
        
        while not sorted_flag:
            # Berechne den neuen Gap
            gap = int(gap / shrink)
            if gap <= 1:
                gap = 1
                sorted_flag = True
            
            # Vergleiche alle Elemente mit dem aktuellen Gap
            i = 0
            while i + gap < n:
                if self.compare(arr, i, i + gap):
                    if self.swap(arr, i, i + gap):
                        yield
                    sorted_flag = False
                else:
                    yield
                i += 1
        
        self.visualizer.update_display(arr, [])
