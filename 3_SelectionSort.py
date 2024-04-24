from SortAlgorithm import SortAlgorithm

class SelectionSort(SortAlgorithm):
    def __init__(self, array):
        super().__init__("SelectionSort", array)

    def sort(self):
        n = len(self.array)
        for i in range(n):
            minpos = i
            for j in range(i + 1, n):
                if self.compare(minpos, j):
                    minpos = j
            self.swap(i, minpos)