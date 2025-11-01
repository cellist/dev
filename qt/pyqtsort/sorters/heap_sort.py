from base_sorter import BaseSorter


class HeapSort(BaseSorter):
    """Heap Sort Algorithmus"""
    
    def sort(self, arr):
        n = len(arr)
        
        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            yield from self._heapify(arr, n, i)
        
        # Extract elements from heap
        for i in range(n - 1, 0, -1):
            if self.swap(arr, 0, i):
                yield
            yield from self._heapify(arr, i, 0)
        
        self.visualizer.update_display(arr, [])
    
    def _heapify(self, arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n:
            self.compare(arr, left, largest)
            yield
            if arr[left] > arr[largest]:
                largest = left
        
        if right < n:
            self.compare(arr, right, largest)
            yield
            if arr[right] > arr[largest]:
                largest = right
        
        if largest != i:
            if self.swap(arr, i, largest):
                yield
            yield from self._heapify(arr, n, largest)
