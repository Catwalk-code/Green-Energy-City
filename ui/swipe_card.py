"""Виджет карточки с поддержкой свайпа для Green Energy City."""

import os

from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (
    NumericProperty,
    StringProperty,
    ListProperty,
)
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.lang import Builder

# Пути к иконкам стрелок подсказки свайпа
_ICON_LEFT_ARROW  = os.path.join('data', 'icons', 'leftarrow.png')
_ICON_RIGHT_ARROW = os.path.join('data', 'icons', 'rightarrow.png')

Builder.load_string("""
<SwipeCard>:
    size_hint: None, None
    size: dp(300), dp(390)

    # ── Фон карточки (с поворотом) ──────────────────────────────────
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.card_rotation
            origin: root.center
        # Мягкая тень
        Color:
            rgba: 0, 0, 0, 0.18
        RoundedRectangle:
            pos: root.x + 4, root.y - 4
            size: root.size
            radius: [dp(18)]
        # Лицевая сторона карточки
        Color:
            rgba: root.card_color
        RoundedRectangle:
            pos: root.pos
            size: root.size
            radius: [dp(18)]
    canvas.after:
        PopMatrix

    # ── Имя персонажа ────────────────────────────────────────────────
    Label:
        text: root.character_name
        font_size: sp(17)
        bold: True
        color: 0.15, 0.45, 0.15, 1
        size_hint: None, None
        size: root.width - dp(32), dp(44)
        # dp(58) = dp(44) name height + dp(14) top margin
        pos: root.x + dp(16), root.top - dp(58)
        halign: 'center'
        valign: 'middle'
        text_size: self.size

    # ── Горизонтальный разделитель ───────────────────────────────────
    Widget:
        size_hint: None, None
        size: root.width - dp(32), dp(1)
        # dp(62) = dp(58) name bottom + dp(4) gap
        pos: root.x + dp(16), root.top - dp(62)
        canvas:
            Color:
                rgba: 0.75, 0.9, 0.75, 1
            Rectangle:
                pos: self.pos
                size: self.size

    # ── Текст карточки ───────────────────────────────────────────────
    Label:
        text: root.card_text
        font_size: sp(18)
        color: 0.12, 0.12, 0.12, 1
        size_hint: None, None
        # height = card height minus header (62dp) and footer (60dp from bottom) + 18dp adjustment
        size: root.width - dp(32), root.height - dp(140)
        pos: root.x + dp(16), root.y + dp(60)
        text_size: self.size
        halign: 'center'
        valign: 'middle'

    # ── Метка левого варианта (свайп влево) — справа на карточке ────
    # Располагается в правой половине карточки, чтобы оставаться видимой
    # при перетаскивании карточки влево (правая часть покидает экран последней)
    Label:
        text: root.left_text
        font_size: sp(14)
        bold: True
        color: 0.85, 0.15, 0.15, root.left_alpha
        opacity: root.left_alpha
        size_hint: None, None
        size: dp(130), dp(90)
        pos: root.x + root.width - dp(138), root.center_y - dp(45)
        halign: 'center'
        valign: 'middle'
        text_size: self.size
        canvas.before:
            Color:
                rgba: 1, 0.85, 0.85, root.left_alpha * 0.85
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(10)]

    # ── Метка правого варианта (свайп вправо) — слева на карточке ───
    # Располагается в левой половине карточки, чтобы оставаться видимой
    # при перетаскивании карточки вправо (левая часть покидает экран последней)
    Label:
        text: root.right_text
        font_size: sp(14)
        bold: True
        color: 0.1, 0.65, 0.1, root.right_alpha
        opacity: root.right_alpha
        size_hint: None, None
        size: dp(130), dp(90)
        pos: root.x + dp(8), root.center_y - dp(45)
        halign: 'center'
        valign: 'middle'
        text_size: self.size
        canvas.before:
            Color:
                rgba: 0.85, 1, 0.85, root.right_alpha * 0.85
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(10)]

    # ── Подсказка свайпа: [←картинка] [текст] [→картинка] ───────────
    BoxLayout:
        orientation: 'horizontal'
        size_hint: None, None
        size: root.width - dp(16), dp(28)
        pos: root.x + dp(8), root.y + dp(8)
        spacing: dp(4)
        # Картинка левой стрелки
        Image:
            source: root.arrow_left_icon
            size_hint: None, 1
            width: dp(24)
            allow_stretch: True
            keep_ratio: True
            opacity: 0.65
        # Текст подсказки (без стрелок, зависит от языка)
        Label:
            text: root.swipe_hint
            font_size: sp(14)
            color: 0.5, 0.5, 0.5, 0.75
            halign: 'center'
            valign: 'middle'
            text_size: self.size
        # Картинка правой стрелки
        Image:
            source: root.arrow_right_icon
            size_hint: None, 1
            width: dp(24)
            allow_stretch: True
            keep_ratio: True
            opacity: 0.65
""")


class SwipeCard(FloatLayout):
    """Виджет карточки, которую можно смахнуть влево или вправо."""

    card_rotation  = NumericProperty(0)
    card_color     = ListProperty([1, 1, 1, 1])
    character_name = StringProperty("Character")
    card_text      = StringProperty("Card text goes here.")
    left_text      = StringProperty("No")
    right_text     = StringProperty("Yes")
    left_alpha     = NumericProperty(0)
    right_alpha    = NumericProperty(0)
    # Текст подсказки: без стрелок (они теперь картинки), обновляется при смене языка
    swipe_hint      = StringProperty("swipe to decide")
    # Пути к картинкам стрелок
    arrow_left_icon  = StringProperty(_ICON_LEFT_ARROW)
    arrow_right_icon = StringProperty(_ICON_RIGHT_ARROW)

    # Минимальное горизонтальное смещение (px) для подтверждения свайпа
    SWIPE_THRESHOLD = 100
    # Максимальный угол наклона карточки (градусы) во время перетаскивания
    MAX_ROTATION = 10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._touch_start = None
        self._orig_pos = None
        self.swipe_callback = None
        # Коллбэк для уведомления о текущем направлении перетаскивания:
        # вызывается с 'left', 'right' или None (при сбросе/отпускании).
        self.drag_callback = None
        self._animating = False
        self._drag_direction = None  # текущее направление тяги (None / 'left' / 'right')

    # ------------------------------------------------------------------
    # Обработка касаний
    # ------------------------------------------------------------------

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not self._animating:
            touch.grab(self)
            self._touch_start = (touch.x, touch.y)
            self._orig_pos = list(self.pos)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return super().on_touch_move(touch)

        dx = touch.x - self._touch_start[0]
        dy = touch.y - self._touch_start[1]

        # Перемещение карточки (вертикальное движение приглушено)
        self.x = self._orig_pos[0] + dx
        self.y = self._orig_pos[1] + dy * 0.25

        # Наклон пропорционален горизонтальному смещению
        self.card_rotation = -(dx / Window.width) * self.MAX_ROTATION * 2.5

        # Показать подсветку варианта при приближении к порогу
        hint_start = self.SWIPE_THRESHOLD * 0.35
        hint_range = self.SWIPE_THRESHOLD * 0.65

        if dx > hint_start:
            alpha = min(1.0, (dx - hint_start) / hint_range)
            self.right_alpha = alpha
            self.left_alpha = 0
            g = 1.0
            rb = 1.0 - alpha * 0.07
            self.card_color = [rb, g, rb, 1]
            new_dir = "right"
        elif dx < -hint_start:
            alpha = min(1.0, (-dx - hint_start) / hint_range)
            self.left_alpha = alpha
            self.right_alpha = 0
            r = 1.0
            gb = 1.0 - alpha * 0.07
            self.card_color = [r, gb, gb, 1]
            new_dir = "left"
        else:
            self.left_alpha = 0
            self.right_alpha = 0
            self.card_color = [1, 1, 1, 1]
            new_dir = None

        # Уведомить об изменении направления тяги (только при смене)
        if new_dir != self._drag_direction:
            self._drag_direction = new_dir
            if self.drag_callback:
                self.drag_callback(new_dir)

        return True

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return super().on_touch_up(touch)

        touch.ungrab(self)
        dx = touch.x - self._touch_start[0]

        if dx >= self.SWIPE_THRESHOLD:
            self._swipe_out("right")
        elif dx <= -self.SWIPE_THRESHOLD:
            self._swipe_out("left")
        else:
            self._snap_back()

        return True

    # ------------------------------------------------------------------
    # Анимации
    # ------------------------------------------------------------------

    def _swipe_out(self, direction):
        """Анимировать вылет карточки за край экрана."""
        self._animating = True
        target_x = (Window.width * 1.4) if direction == "right" else (-self.width * 1.4)
        end_angle = self.MAX_ROTATION * 2 if direction == "right" else -self.MAX_ROTATION * 2

        anim = Animation(
            x=target_x,
            card_rotation=end_angle,
            opacity=0,
            duration=0.30,
            t="out_quad",
        )
        anim.bind(on_complete=lambda *_: self._on_swipe_done(direction))
        anim.start(self)

    def _snap_back(self):
        """Вернуть карточку на исходную позицию при отпускании."""
        if self._orig_pos is None:
            return
        # Сбросить уведомление о направлении тяги
        if self._drag_direction is not None:
            self._drag_direction = None
            if self.drag_callback:
                self.drag_callback(None)
        anim = Animation(
            x=self._orig_pos[0],
            y=self._orig_pos[1],
            card_rotation=0,
            duration=0.22,
            t="out_elastic",
        )
        anim.bind(on_complete=lambda *_: self._reset_tint())
        anim.start(self)

    def _reset_tint(self):
        """Убрать цветовую подсветку после возврата карточки."""
        self.card_color = [1, 1, 1, 1]
        self.left_alpha = 0
        self.right_alpha = 0

    def _on_swipe_done(self, direction):
        """Вызывается по окончании анимации вылета — передаёт результат."""
        self._animating = False
        if self.swipe_callback:
            self.swipe_callback(direction)
