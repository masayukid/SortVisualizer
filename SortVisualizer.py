import os
import sys
import glob
import random
import inspect
import importlib

import pygame
from pygame.locals import *
from SortAlgorithm import SortAlgorithm
from VisualizerUI import Display, Button, CyclicButton, Slider, ColorChooser

# =======================
#     SortVisualizer
# =======================
class SortVisualizer:
    def __init__(self):
        """コンストラクタ"""
        # pygameの初期化
        pygame.init()
        pygame.display.set_caption("Sort Visualizer")
        icon = pygame.image.load("icon.png")
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()

        # パラメータの初期化
        self.init_methods = ["Random", "Ascending", "Descending"]
        self.sort_algorithms = self.load_algorithms()
        self.array_sizes = [2 ** x for x in range(1, 10)]
        self.anim_speeds = [0.01, 0.1, 0.5, 1.0, 2.0, 10, 100]
        self.actions = ["Sort", "Pause", "Resume", "Restart"]
        self.init_method_idx = 0
        self.sort_algorithm_idx = 0
        self.array_size_idx = 4
        self.anim_speed_idx = 3
        self.action_idx = 0
        self.min_color = (50, 50, 50)
        self.max_color = (200, 200, 200)

        # 定数
        self.__max_array_size = 512
        self.__margin = 20
        self.__ui_size = (200, 50)
        self.__ui_margin = 36
        self.__window_size = self.get_min_window_size()

        self.init_array()
        self.refresh()

    def load_algorithms(self):
        """SortAlgorithmを読み込み"""
        # PATHに実行ディレクトリを追加
        sys.path.append(os.path.dirname(sys.argv[0]))

        cls_list = []
        # .pyファイルを順次読み込み
        for filepath in glob.glob('*.py'):
            path = os.path.splitext(filepath)[0]
            mod = importlib.import_module(path)
            for _, cls in inspect.getmembers(mod, inspect.isclass):
                # SortAlgorithmを継承していればリストに追加
                if cls.__base__ is SortAlgorithm:
                    cls_list.append(cls)
        # SortAlgorithmが1つもないときはエラー
        if len(cls_list) == 0:
            raise Exception("Algorithm Not Found.")
        return cls_list

    def set_init_method(self, idx):
        """初期列の生成法を設定"""
        self.init_method_idx = idx

    def set_sort_algorithm(self, idx):
        """整列アルゴリズムを設定"""
        self.sort_algorithm_idx = idx
        self.draw_array()

    def set_array_size(self, idx):
        """配列サイズを設定"""
        # 配列サイズが変わったら初期化
        if idx != self.array_size_idx:
            self.array_size_idx = idx
            self.init_array()
        self.draw_array()

    def set_anim_speed(self, idx):
        """再生速度を設定"""
        self.anim_speed_idx = idx

    def set_action(self, idx):
        """操作を設定"""
        self.action_idx = idx

    def set_min_color(self, color):
        """最小値の色を設定"""
        self.min_color = color
        self.array_display.set_color(self.min_color, self.max_color)

    def set_max_color(self, color):
        """最大値の色を設定"""
        self.max_color = color
        self.array_display.set_color(self.min_color, self.max_color)

    def get_init_method(self):
        """初期列の生成法を取得"""
        return self.init_methods[self.init_method_idx]

    def get_sort_algorithm(self):
        """整列アルゴリズムを取得"""
        return self.sort_algorithms[self.sort_algorithm_idx]

    def get_array_size(self):
        """配列サイズを取得"""
        return self.array_sizes[self.array_size_idx]

    def get_anim_speed(self):
        """再生速度を取得"""
        return self.anim_speeds[self.anim_speed_idx]

    def get_action(self):
        """操作を取得"""
        return self.actions[self.action_idx]

    def get_min_color(self):
        """最小値の色を取得"""
        return self.min_color

    def get_max_color(self):
        """最大値の色を取得"""
        return self.max_color

    def get_min_window_size(self):
        """最小ウィンドウサイズを取得"""
        return (
            self.__max_array_size + self.__margin * 3 + self.__ui_size[0],
            self.__margin + (self.__ui_margin + self.__ui_size[1]) * 8)

    def init_array(self):
        """配列を初期化"""
        init_method = self.get_init_method()
        array_size = self.get_array_size()
        if init_method == "Random":
            self.array = random.sample(range(1, array_size + 1), array_size)
        elif init_method == "Ascending":
            self.array = list(range(1, array_size + 1))
        elif init_method == "Descending":
            self.array = list(range(array_size, 0, -1))
        else:
            raise Exception("Invalid Initialize Method:", init_method)

    def resize(self, size):
        """ウィンドウのリサイズ"""
        min_window_size = self.get_min_window_size()
        self.__window_size = (
            max(min_window_size[0], size[0]),
            max(min_window_size[1], size[1]))
        self.refresh()

    def refresh(self):
        """画面全体を再描画"""
        self.main_surface = pygame.display.set_mode(self.__window_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.main_surface.fill((255, 255, 255))
        self.create_UI()
        self.draw_array()

    def create_UI(self):
        """UIを生成"""
        font_m = pygame.font.SysFont('meiryoui', 14)
        font_l = pygame.font.SysFont('meiryoui', 16)
        pos_x = self.__window_size[0] - self.__margin - self.__ui_size[0]
        pos_y = self.__ui_margin

        def initialize():
            """Initializeボタン押下時の処理"""
            self.init_array()
            self.draw_array()

        def action(idx):
            """操作ボタン押下時の処理"""
            if idx == 0:
                self.array_display.restart(self.array.copy())
            if idx == 1:
                self.array_display.sort(self.get_sort_algorithm())
            if idx == 2:
                self.array_display.pause()
            if idx == 3:
                self.array_display.resume()

        # 初期化・操作ボタン
        init_button = Button(
            Rect(pos_x, self.__window_size[1] - (self.__margin + self.__ui_size[1]) * 2, self.__ui_size[0], self.__ui_size[1]),
            font_l, "Initialize", initialize)
        self.action_button = CyclicButton(
            Rect(pos_x, self.__window_size[1] - self.__margin - self.__ui_size[1], self.__ui_size[0], self.__ui_size[1]),
            font_l, self.actions, 0, action)

        # 配列を描画するディスプレイ
        width = self.__window_size[0] - self.__ui_size[0] - self.__margin * 3
        height = self.__window_size[1] - self.__margin * 2
        self.array_display = Display(
            Rect(self.__margin, self.__margin, width, height),
            font_m, self.min_color, self.max_color, self.get_anim_speed, self.action_button)

        def place_text(text_str):
            """テキストを配置"""
            nonlocal pos_y
            text = font_m.render(text_str, True, (50, 50, 50))
            self.main_surface.blit(text, (pos_x + 2, pos_y - 22))
            # UI要素1つ分下にずらす
            pos_y += self.__ui_size[1] + self.__ui_margin

        # 各パラメータ設定用UI
        init_method_button = CyclicButton(
            Rect(pos_x, pos_y, self.__ui_size[0], self.__ui_size[1]),
            font_l, self.init_methods, self.init_method_idx, self.set_init_method)
        place_text("Initialize Method")
        sort_algorithm_button = CyclicButton(
            Rect(pos_x, pos_y, self.__ui_size[0], self.__ui_size[1]),
            font_l, [x.__name__ for x in self.sort_algorithms], self.sort_algorithm_idx, self.set_sort_algorithm)
        place_text("Sort Algorithm")
        array_size_slider = Slider(
            Rect(pos_x, pos_y, self.__ui_size[0], self.__ui_size[1]),
            20, self.array_sizes, font_m, self.array_size_idx, self.set_array_size)
        place_text("Array Size")
        anim_speed_slider = Slider(
            Rect(pos_x, pos_y, self.__ui_size[0], self.__ui_size[1]),
            20, self.anim_speeds, font_m, self.anim_speed_idx, self.set_anim_speed)
        place_text("Animation Speed")
        min_color_chooser = ColorChooser(
            Rect(pos_x, pos_y, self.__ui_size[0], self.__ui_size[1]), self.min_color, self.set_min_color)
        place_text("Min Color")
        max_color_chooser = ColorChooser(
            Rect(pos_x, pos_y, self.__ui_size[0], self.__ui_size[1]), self.max_color, self.set_max_color)
        place_text("Max Color")

        self.group = pygame.sprite.Group(
            init_button,
            self.action_button,
            self.array_display,
            init_method_button,
            sort_algorithm_button,
            array_size_slider,
            anim_speed_slider,
            min_color_chooser,
            max_color_chooser)

    def draw_array(self):
        """配列を描画"""
        self.array_display.init_display()
        self.array_display.draw_array(self.array.copy())

    def main(self):
        """main関数"""
        while True:
            # 30 [fps (frames per second)] に制限
            self.clock.tick(30)
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == VIDEORESIZE:
                    self.resize(event.size)
            self.group.update(events)
            self.group.draw(self.main_surface)
            pygame.display.update()