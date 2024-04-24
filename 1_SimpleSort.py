from SortAlgorithm import SortAlgorithm

class SimpleSort(SortAlgorithm):
    def __init__(self, array):
        super().__init__("SimpleSort", array)

    def sort(self):
        n = len(self.array)
        for i in range(n - 1):
            for j in range(i + 1, n):
                if self.compare(i, j):
                    self.swap(i, j)