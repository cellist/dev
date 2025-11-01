from base_sorter import BaseSorter


class MergeSort(BaseSorter):
    """Merge Sort Algorithmus"""
    
    def sort(self, arr):
        yield from self._merge_sort(arr, 0, len(arr) - 1)
        self.visualizer.update_display(arr, [])
    
    def _merge_sort(self, arr, left, right):
        if left < right:
            mid = (left + right) // 2
            yield from self._merge_sort(arr, left, mid)
            yield from self._merge_sort(arr, mid + 1, right)
            yield from self._merge(arr, left, mid, right)
    
    def _merge(self, arr, left, mid, right):
        left_part = arr[left:mid + 1]
        right_part = arr[mid + 1:right + 1]
        
        i = j = 0
        k = left
        
        while i < len(left_part) and j < len(right_part):
            self.comparisons += 1
            if left_part[i] <= right_part[j]:
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                j += 1
            self.swaps += 1
            self.visualizer.update_display(arr, [k])
            yield
            k += 1
        
        while i < len(left_part):
            arr[k] = left_part[i]
            self.swaps += 1
            self.visualizer.update_display(arr, [k])
            yield
            i += 1
            k += 1
        
        while j < len(right_part):
            arr[k] = right_part[j]
            self.swaps += 1
            self.visualizer.update_display(arr, [k])
            yield
            j += 1
            k += 1
