from base_sorter import BaseSorter


class RadixSort(BaseSorter):
    """Radix Sort Algorithmus (LSD - Least Significant Digit)"""
    
    def sort(self, arr):
        # Finde den maximalen Wert um die Anzahl der Digits zu bestimmen
        max_val = max(arr)
        
        # Führe Counting Sort für jede Digit-Position durch
        exp = 1
        while max_val // exp > 0:
            yield from self._counting_sort(arr, exp)
            exp *= 10
        
        self.visualizer.update_display(arr, [])
    
    def _counting_sort(self, arr, exp):
        """Counting Sort basierend auf der aktuellen Digit-Position (exp)"""
        n = len(arr)
        output = [0] * n
        count = [0] * 10
        
        # Zähle das Vorkommen jeder Digit
        for i in range(n):
            index = (arr[i] // exp) % 10
            count[index] += 1
            self.comparisons += 1
            self.visualizer.update_display(arr, [i])
            yield
        
        # Ändere count[i] so dass es die Position im output Array enthält
        for i in range(1, 10):
            count[i] += count[i - 1]
        
        # Baue das output Array
        i = n - 1
        while i >= 0:
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1
            i -= 1
        
        # Kopiere das sortierte Array zurück
        for i in range(n):
            if arr[i] != output[i]:
                arr[i] = output[i]
                self.swaps += 1
                self.visualizer.update_display(arr, [i])
                yield
