from base_sorter import BaseSorter


class CocktailSort(BaseSorter):
    """Cocktail Shaker Sort - Bidirektionaler Bubble Sort"""
    
    def sort(self, arr):
        n = len(arr)
        swapped = True
        start = 0
        end = n - 1
        
        while swapped:
            # Reset das swapped Flag beim Start jeder Iteration
            swapped = False
            
            # Vorwärts-Pass (wie normaler Bubble Sort)
            for i in range(start, end):
                if self.compare(arr, i, i + 1):
                    if self.swap(arr, i, i + 1):
                        yield
                    swapped = True
                else:
                    yield
            
            # Wenn nichts getauscht wurde, ist das Array sortiert
            if not swapped:
                break
            
            # Verringere end, da das letzte Element jetzt sortiert ist
            swapped = False
            end -= 1
            
            # Rückwärts-Pass
            for i in range(end - 1, start - 1, -1):
                if self.compare(arr, i, i + 1):
                    if self.swap(arr, i, i + 1):
                        yield
                    swapped = True
                else:
                    yield
            
            # Erhöhe start, da das erste Element jetzt sortiert ist
            start += 1
        
        self.visualizer.update_display(arr, [])
