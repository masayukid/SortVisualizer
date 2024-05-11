# SortVisualizer

配列のソートをアニメーションで可視化します。配列の要素数・初期列（昇順/降順/ランダム）・アニメーション速度などを変更できます。
ソートアルゴリズムも変更可能で、オリジナルのソートアルゴリズムを実行することもできます。

## Requirement

- pygame==2.5.2

## Usage

```
$ pip install -r requirements.txt
$ python main.py
```

### Option
- **Initialize Method** : Random/Ascending/Descending
- **Sort Algorithm** : Simple/Bubble/Selection/Insertion/Shell/Quick/Heap/Merge
- **Array Size** : 2/4/8/16/32/64/128/256/512
- **Animation Speed** : 0.01/0.1/0.5/1.0/2.0/10/100

## Custom Sorting Algorithm

SortAlgorithmクラスを継承し、sort関数にアルゴリズムを記述してください。
比較/スワップ回数を表示するために、組み込みのcompare/swapメソッドを使うことを推奨します。

```
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
```

## License

[MIT license](https://en.wikipedia.org/wiki/MIT_License)
