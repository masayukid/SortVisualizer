from SortAlgorithm import SortAlgorithm

class QuickSort(SortAlgorithm):
    def __init__(self, array):
        super().__init__("QuickSort", array)

    def sort(self, left=0, right=None):
        if right is None:
            right = len(self.array) - 1
        if left < right:
            pivot = left - 1
            for j in range(left, right + 1):
                if not self.compare(j, right):
                    pivot += 1
                    if pivot < j:
                        self.swap(pivot, j)
            self.sort(left, pivot - 1)
            self.sort(pivot + 1, right)