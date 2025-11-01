from base_sorter import BaseSorter


class GnomeSort(BaseSorter):
    """Gnome Sort - Einfacher Algorithmus mit Vor- und Rückwärtsbewegung"""
    
    def sort(self, arr):
        n = len(arr)
        index = 0
        
        while index < n:
            if index == 0:
                # Am Anfang: gehe vorwärts
                index += 1
            else:
                # Vergleiche mit dem vorherigen Element
                if self.compare(arr, index - 1, index):
                    # Wenn vorheriges größer: tausche und gehe zurück
                    if self.swap(arr, index - 1, index):
                        yield
                    index -= 1
                else:
                    # Wenn in richtiger Reihenfolge: gehe vorwärts
                    yield
                    index += 1
        
        self.visualizer.update_display(arr, [])
