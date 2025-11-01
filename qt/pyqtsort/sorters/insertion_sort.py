from base_sorter import BaseSorter


class InsertionSort(BaseSorter):
    """Insertion Sort Algorithmus"""
    
    def sort(self, arr):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0:
                self.compare(arr, j, j+1)
                yield
                if arr[j] > key:
                    arr[j + 1] = arr[j]
                    self.swaps += 1
                    self.visualizer.update_display(arr, [j, j+1])
                    yield
                    j -= 1
                else:
                    break
            arr[j + 1] = key
        self.visualizer.update_display(arr, [])
