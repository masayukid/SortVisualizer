from SortAlgorithm import SortAlgorithm

class InsertionSort(SortAlgorithm):
    def __init__(self, array):
        super().__init__("InsertionSort", array)

    def sort(self):
        n = len(self.array)
        for i in range(1, n):
            for j in range(i):
                if self.compare(i - j - 1, i - j):
                    self.swap(i - j - 1, i - j)
                else:
                    break