from SortAlgorithm import SortAlgorithm

class MergeSort(SortAlgorithm):
    def __init__(self, array):
        super().__init__("MergeSort", array)

    def sort(self, array=None, start=0, end=0):
        def merge(start, mid, end):
            start2 = mid + 1
            if not self.compare(mid, start2):
                return
            while (start <= mid and start2 <= end):
                if self.compare(start, start2):
                    idx = start2
                    while (idx != start):
                        self.swap(idx, idx - 1)
                        idx -= 1
                    start += 1
                    mid += 1
                    start2 += 1
                else:
                    start += 1

        if not array:
            array = self.array
            end = len(array) - 1
        if start < end:
            mid = start + (end - start) // 2
            self.sort(array, start, mid)
            self.sort(array, mid + 1, end)
            merge(start, mid, end)