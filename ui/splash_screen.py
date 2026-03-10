"""Экран-заставка при запуске Green Energy City.

Показывает логотип (data/splash/presplash.png) в течение пяти секунд,
затем автоматически переходит на экран главного меню.
"""

import os

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.lang import Builder

# Путь к изображению заставки
_PRESPLASH = os.path.join('data', 'splash', 'presplash.png')

# Длительность отображения заставки в секундах
_SPLASH_DURATION = 5.0

Builder.load_string("""
<SplashScreen>:
    canvas.before:
        Color:
            rgba: 0.04, 0.13, 0.04, 1
        Rectangle:
            pos: self.pos
            size: self.size
""")


class SplashScreen(Screen):
    """Заставка при запуске: показывает логотип и переходит в меню."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._timer = None
        root = FloatLayout()
        root.add_widget(Image(
            source=_PRESPLASH,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        ))
        self.add_widget(root)

    def on_enter(self):
        """При переходе на экран запускаем таймер перехода в меню."""
        self._timer = Clock.schedule_once(self._go_to_menu, _SPLASH_DURATION)

    def on_leave(self):
        """При уходе с экрана отменяем таймер (на случай раннего ухода)."""
        if self._timer is not None:
            Clock.unschedule(self._timer)
            self._timer = None

    def _go_to_menu(self, _dt):
        """Переключиться на экран главного меню."""
        self._timer = None
        if self.manager:
            self.manager.current = "menu"
