from SortAlgorithm import SortAlgorithm

class ShellSort(SortAlgorithm):
    def __init__(self, array):
        super().__init__("ShellSort", array)

    def sort(self):
        n = len(self.array)
        h = 1
        while h < n / 9:
            h = h * 3 + 1
        while h > 0:
            for i in range(h, n):
                j = i
                while j >= h and self.compare(j - h, j):
                    self.swap(j, j - h)
                    j -= h
            h = int(h / 3)