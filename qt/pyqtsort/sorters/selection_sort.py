from base_sorter import BaseSorter


class SelectionSort(BaseSorter):
    """Selection Sort Algorithmus"""
    
    def sort(self, arr):
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                self.compare(arr, min_idx, j)
                yield
                if arr[j] < arr[min_idx]:
                    min_idx = j
            if min_idx != i:
                if self.swap(arr, i, min_idx):
                    yield
        self.visualizer.update_display(arr, [])
