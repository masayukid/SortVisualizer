import pygame
from pygame.locals import *
from tkinter import colorchooser

# =======================
#         Display
# =======================
class Display(pygame.sprite.Sprite):
    """配列表示用ディスプレイ"""
    def __init__(self, rect, font, min_color, max_color, get_anim_speed, action_button):
        """コンストラクタ"""
        super().__init__()
        self.image = pygame.Surface((rect.w, rect.h))
        self.rect = rect
        self.font = font
        self.min_color = min_color
        self.max_color = max_color
        self.get_anim_speed = get_anim_speed
        self.action_button = action_button
        self.init_display()

    def init_display(self):
        """初期化"""
        self.array = []
        self.state = "Idle"
        self.count = 1
        self.details = [0, 0]
        self.step = None
        self.algorithm = None
        self.generator = None
        self.action_button.set_idx(0)
        
    def set_color(self, min_color, max_color):
        """色の設定"""
        self.min_color = min_color
        self.max_color = max_color
        self.draw_array()

    def draw_array(self, array=None):
        """配列の描画"""
        if array:
            self.array = array
        self.image.fill((50, 50, 50))
        width, height = self.rect.w - 2, self.rect.h - 2
        self.image.fill((240, 240, 240), Rect(1, 1, width, height))

        count = 0
        offset = 0
        array_size = len(self.array)
        _elem_width = int(width / array_size)
        lack = width - _elem_width * array_size
        for i in range(array_size):
            proportion = self.array[i] / array_size
            elem_height = int(height * proportion)
            elem_width = _elem_width
            elem_color = self.to_color(proportion)
            if self.step:
                if i in self.step[0]:
                    # 比較・スワップの対象要素は色を変える
                    if self.step[1] == "Compare":
                        elem_color = (255, 0, 0)
                    if self.step[1] == "Swap":
                        elem_color = (0, 255, 0)
            # 横幅の余り分を等間隔で分配
            if lack > 0 and int(array_size * count / lack) == i:
                elem_width += 1
                count += 1
            self.image.fill(
                elem_color, (offset + 1, height - elem_height + 1, elem_width, elem_height))
            offset += elem_width
        
        # ソート中なら比較・スワップ回数を表示
        if self.algorithm:
            text = f"{self.algorithm.name} - {str(self.details[0])} Comparisons, {str(self.details[1])} Swaps"
            text_surf = self.font.render(text, True, (50, 50, 50))
            self.image.blit(text_surf, (10, 5))

    def to_color(self, proportion):
        """大きさに応じて色をグラデーションする"""
        r = self.min_color[0] + (self.max_color[0] - self.min_color[0]) * proportion
        g = self.min_color[1] + (self.max_color[1] - self.min_color[1]) * proportion
        b = self.min_color[2] + (self.max_color[2] - self.min_color[2]) * proportion
        return (r, g, b)

    def sort(self, sort_algorithm):
        """ソート"""
        self.algorithm = sort_algorithm(self.array.copy())
        self.generator = self.algorithm.generator()
        self.state = "Sort"

    def pause(self):
        """一時停止"""
        self.state = "Pause"

    def resume(self):
        """再開"""
        self.state = "Sort"
        self.action_button.set_idx(1)

    def restart(self, array):
        """初めから再ソート"""
        self.array = array
        self.state = "Sort"
        self.count = 1
        self.details = [0, 0]
        self.generator = self.algorithm.generator()
        self.action_button.set_idx(1)

    def swap(self, elems):
        """スワップ"""
        self.array[elems[0]], self.array[elems[1]] = self.array[elems[1]], self.array[elems[0]]

    def update(self, event_list):
        """画面を更新"""
        if self.state == "Sort":
            int_part = int(self.count)
            # 再生速度に応じてステップを進める
            for i in range(int_part):
                self.step = next(self.generator)
                if not self.step:
                    # イテレータが終わったらIdle状態にする
                    self.draw_array()
                    self.state = "Idle"
                    self.action_button.set_idx(3)
                    return
                if self.step[1] == "Compare":
                    self.details[0] += 1
                if self.step[1] == "Swap":
                    self.swap(self.step[0])
                    self.details[1] += 1
                if i == int_part - 1:
                    # 最後の要素で描画を更新
                    self.draw_array()
            # 1.0 のとき、100 [step/second] になるように調整
            self.count += self.get_anim_speed() * 10 / 3 - int_part


# =======================
#         Button
# =======================
class Button(pygame.sprite.Sprite):
    """ボタン"""
    def __init__(self, rect, font, text, callback=None):
        """コンストラクタ"""
        super().__init__()
        self.button_image = pygame.Surface((rect.w, rect.h))
        self.hover_image = pygame.Surface((rect.w, rect.h))
        self.image = self.button_image
        self.rect = rect
        self.font = font
        self.callback = callback
        self.set_text(text)

    def set_text(self, text):
        """表示テキストを設定"""
        text_surf = self.font.render(text, True, (50, 50, 50))
        self.button_image.fill((255, 255, 255))
        self.button_image.blit(text_surf, text_surf.get_rect(center=(self.rect.w // 2, self.rect.h // 2)))
        pygame.draw.rect(self.button_image, (50, 50, 50), self.button_image.get_rect(), 1)
        text_surf = self.font.render(text, True, (255, 255, 255))
        self.hover_image.fill((50, 50, 50))
        self.hover_image.blit(text_surf, text_surf.get_rect(center=(self.rect.w // 2, self.rect.h // 2)))

    def update(self, event_list):
        """画面を更新"""
        hover = pygame.mouse.get_visible() and self.rect.collidepoint(pygame.mouse.get_pos())
        for event in event_list:
            if event.type == MOUSEBUTTONDOWN:
                if hover and event.button == 1:
                    self.on_click()
        self.image = self.hover_image if hover else self.button_image

    def on_click(self):
        """ボタン押下時の処理"""
        if self.callback:
            self.callback()


# =======================
#      CyclicButton
# =======================
class CyclicButton(Button):
    """テキストがループして変わるボタン"""
    def __init__(self, rect, font, texts, idx=0, callback=None):
        """コンストラクタ"""
        super().__init__(rect, font, texts[idx])
        self.texts = texts
        self.idx = idx
        self.callback = callback

    def set_idx(self, idx):
        """Indexを設定"""
        self.idx = idx
        self.set_text(self.texts[self.idx])

    def on_click(self):
        """ボタン押下時の処理"""
        self.idx = (self.idx + 1) % len(self.texts)
        self.set_text(self.texts[self.idx])
        if self.callback:
            self.callback(self.idx)


# =======================
#         Slider
# =======================
class Slider(pygame.sprite.Sprite):
    """スライダー"""
    def __init__(self, rect, radius, range, font, idx=0, callback=None):
        """コンストラクタ"""
        super().__init__()
        self.default_image = pygame.Surface((rect.w, rect.h))
        self.hover_image = pygame.Surface((rect.w, rect.h))
        self.image = self.default_image
        self.rect = rect
        self.radius = radius
        self.range = range
        self.font = font
        self.idx = -1
        self.callback = callback
        self.set_idx(idx)

        # 内部用変数
        self.__delta = 0
        self.__dragging = 0
        self.__drag_start_pos = None

    def update(self, event_list):
        """画面を更新"""
        hover = pygame.mouse.get_visible() and self.rect.collidepoint(pygame.mouse.get_pos())
        for event in event_list:
            if event.type == MOUSEBUTTONDOWN:
                if hover and event.button == 1:
                    # ドラッグ開始
                    self.__dragging = 2
                    self.__drag_start_pos = event.pos
                    self.toggle_drag_mode(True)
            if event.type == MOUSEBUTTONUP:
                if self.__dragging and event.button == 1:
                    # ドラッグ終了
                    pygame.mouse.set_pos(self.__drag_start_pos)
                    self.__dragging = 0
                    self.__drag_start_pos = None
                    self.toggle_drag_mode(False)
            if event.type == MOUSEMOTION:
                if self.__dragging == 2:
                    # 最初の変化量を破棄
                    pygame.mouse.get_rel()
                    self.__dragging = 1
                if self.__dragging == 1:
                    # 変化量を足して閾値を超えたら変更
                    self.__delta += pygame.mouse.get_rel()[0]
                    thresh = self.rect.w // len(self.range)
                    if abs(self.__delta) > thresh: 
                        delta = abs(self.__delta) // thresh
                        if self.__delta < 0:
                            delta *= -1
                        idx = min(len(self.range) - 1, max(0, self.idx + int(delta)))
                        if idx != self.idx:
                            self.set_idx(idx)
                            self.__delta = 0

        self.image = self.default_image
        if hover or self.__dragging > 0:
            self.image = self.hover_image

    def toggle_drag_mode(self, flag):
        """マウスの操作設定を切り替え"""
        pygame.mouse.set_visible(not flag)
        pygame.event.set_grab(flag)

    def set_idx(self, idx):
        """Indexを設定"""
        value = self.range[idx]
        pos_x = self.radius + (self.rect.w - self.radius * 2) * self.get_normalized_pos(idx)

        text_surf = self.font.render(str(value), True, (50, 50, 50))
        self.default_image.fill((255, 255, 255))
        pygame.draw.line(self.default_image, (50, 50, 50), (self.radius, self.rect.h // 2), (self.rect.w - self.radius, self.rect.h // 2))
        pygame.draw.circle(self.default_image, (255, 255, 255), (pos_x, self.rect.h // 2), self.radius)
        pygame.draw.circle(self.default_image, (50, 50, 50), (pos_x, self.rect.h // 2), self.radius, 1)
        self.default_image.blit(text_surf, text_surf.get_rect(center = (pos_x, self.rect.h // 2)))
        text_surf = self.font.render(str(value), True, (255, 255, 255))
        self.hover_image.fill((255, 255, 255))
        pygame.draw.line(self.hover_image, (50, 50, 50), (self.radius, self.rect.h // 2), (self.rect.w - self.radius, self.rect.h // 2))
        pygame.draw.circle(self.hover_image, (50, 50, 50), (pos_x, self.rect.h // 2), self.radius)
        self.hover_image.blit(text_surf, text_surf.get_rect(center = (pos_x, self.rect.h // 2)))

        self.idx = idx
        if self.callback:
            self.callback(idx)

    def get_normalized_pos(self, idx):
        """0～1に正規化した値を返す"""
        return idx / (len(self.range) - 1)


# =======================
#      ColorChooser
# =======================
class ColorChooser(pygame.sprite.Sprite):
    """色選択パレット"""
    def __init__(self, rect, color, callback=None):
        """コンストラクタ"""
        super().__init__()
        self.button_image = pygame.Surface((rect.w, rect.h))
        self.hover_image = pygame.Surface((rect.w, rect.h))
        self.image = self.button_image
        self.rect = rect
        self.callback = callback
        self.set_color(color)

    def set_color(self, color):
        """色を設定"""
        self.button_image.fill((50, 50, 50))
        self.button_image.fill(color, Rect(1, 1, self.rect.w - 2, self.rect.h - 2))
        self.hover_image.fill((50, 50, 50))
        self.hover_image.fill(self.hover_color(color), Rect(1, 1, self.rect.w - 2, self.rect.h - 2))
        self.color = color
        if self.callback:
            self.callback(color)

    def hover_color(self, color):
        """ホバー時の色を返す"""
        r = color[0] / 2
        g = color[1] / 2
        b = color[2] / 2
        return (r, g, b)

    def update(self, event_list):
        """画面を更新"""
        hover = pygame.mouse.get_visible() and self.rect.collidepoint(pygame.mouse.get_pos())
        for event in event_list:
            if event.type == MOUSEBUTTONDOWN:
                if hover and event.button == 1:
                    self.on_click()
        self.image = self.hover_image if hover else self.button_image

    def on_click(self):
        """パレット押下時の処理"""
        color = colorchooser.askcolor()[0]
        if color:
            self.set_color(color)