from SortAlgorithm import SortAlgorithm

class BubbleSort(SortAlgorithm):
    def __init__(self, array):
        super().__init__("BubbleSort", array)

    def sort(self):
        n = len(self.array)
        for i in range(n - 1):
            for j in range(n - 1, i, -1):
                if self.compare(j - 1, j):
                    self.swap(j - 1, j)