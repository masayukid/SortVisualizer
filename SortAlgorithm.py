from abc import abstractmethod
from threading import Thread

# =======================
#     SortAlgorithm
# =======================
class SortAlgorithm:
    def __init__(self, name, array):
        """コンストラクタ"""
        self.name = name
        self.array = array
        self.steps = []
        self.is_sorted = False
        # インスタンス化と同時に別スレッドでソート開始
        thread = Thread(target=self.__sort)
        thread.start()

    def swap(self, idx1, idx2):
        """スワップ"""
        self.steps.append(((idx1, idx2), "Swap"))
        self.array[idx1], self.array[idx2] = self.array[idx2], self.array[idx1]

    def compare(self, idx1, idx2):
        """比較（gt）"""
        self.steps.append(((idx1, idx2), "Compare"))
        return self.array[idx1] > self.array[idx2]

    def generator(self):
        """ステップのジェネレータ"""
        idx = 0
        while True:
            if len(self.steps) > idx:
                yield self.steps[idx]
                idx += 1
            elif self.is_sorted:
                yield None

    def __sort(self):
        """スレッド用ソート関数"""
        self.sort()
        self.is_sorted = True

    @abstractmethod
    def sort(self):
        """アルゴリズム本体"""
        pass