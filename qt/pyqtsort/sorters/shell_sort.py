from base_sorter import BaseSorter


class ShellSort(BaseSorter):
    """Shell Sort Algorithmus - Verbesserung von Insertion Sort mit Gaps"""
    
    def sort(self, arr):
        n = len(arr)
        # Starte mit einem großen Gap und reduziere es
        gap = n // 2
        
        while gap > 0:
            # Führe gapped insertion sort für diesen gap durch
            for i in range(gap, n):
                temp = arr[i]
                j = i
                
                # Verschiebe Elemente die größer als temp sind
                while j >= gap and arr[j - gap] > temp:
                    self.compare(arr, j - gap, j)
                    yield
                    arr[j] = arr[j - gap]
                    self.swaps += 1
                    self.visualizer.update_display(arr, [j, j - gap])
                    yield
                    j -= gap
                
                # Füge temp an der richtigen Position ein
                arr[j] = temp
                if j != i:
                    self.visualizer.update_display(arr, [j, i])
                    yield
            
            gap //= 2
        
        self.visualizer.update_display(arr, [])
