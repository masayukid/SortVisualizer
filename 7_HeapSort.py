from SortAlgorithm import SortAlgorithm

class HeapSort(SortAlgorithm):
    def __init__(self, array):
        super().__init__("HeapSort", array)

    def sort(self):
        def upheap(n):
            while n != 0:
                parent = int((n - 1) / 2)
                if self.compare(n, parent):
                    self.swap(n, parent)
                    n = parent
                else:
                    break
        def downheap(n):
            if n == 0:
                return
            parent = 0
            while True:
                child = 2 * parent + 1
                if child > n: break
                if (child < n) and self.compare(child + 1, child):
                    child += 1
                if self.compare(child, parent):
                    self.swap(child, parent)
                    parent = child
                else:
                    break

        i = 0
        n = len(self.array)
        while i < n:
            upheap(i)
            i += 1
        while i > 1:
            i -= 1
            self.swap(0, i)
            downheap(i - 1)