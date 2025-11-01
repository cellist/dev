from base_sorter import BaseSorter


class QuickSort(BaseSorter):
    """Quick Sort Algorithmus"""
    
    def sort(self, arr):
        yield from self._quick_sort(arr, 0, len(arr) - 1)
        self.visualizer.update_display(arr, [])
    
    def _quick_sort(self, arr, low, high):
        if low < high:
            pi = yield from self._partition(arr, low, high)
            yield from self._quick_sort(arr, low, pi - 1)
            yield from self._quick_sort(arr, pi + 1, high)
    
    def _partition(self, arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            self.compare(arr, j, high)
            yield
            if arr[j] < pivot:
                i += 1
                if self.swap(arr, i, j):
                    yield
        if self.swap(arr, i + 1, high):
            yield
        return i + 1
