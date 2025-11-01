from base_sorter import BaseSorter


class BubbleSort(BaseSorter):
    """Bubble Sort Algorithmus"""
    
    def sort(self, arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.compare(arr, j, j+1):
                    if self.swap(arr, j, j+1):
                        yield
        self.visualizer.update_display(arr, [])
