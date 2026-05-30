"""Экран-заставка при запуске Green Energy City.

Показывает логотип (data/splash/presplash.png) в течение 3.5 секунд,
затем автоматически переходит на экран главного меню.
"""

import os

from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.lang import Builder

# Путь к изображению заставки
_PRESPLASH = os.path.join('data', 'splash', 'presplash.png')

# Длительность отображения заставки в секундах
_SPLASH_DURATION = 3.5

import sys
import os
from kivy.lang import Builder

def get_resource_path(relative_path):
    """Возвращает абсолютный путь к файлу, работает и для разработки, и для .exe"""
    if hasattr(sys, '_MEIPASS'):
        # Запуск из собранного exe: файлы находятся во временной папке
        return os.path.join(sys._MEIPASS, relative_path)
    # Запуск из исходников: файлы находятся рядом с скриптом
    return os.path.join(os.path.abspath("."), relative_path)

# ИСПОЛЬЗУЙТЕ ЭТУ ФУНКЦИЮ ВМЕСТО ОБЫЧНОЙ СТРОКИ:
kv_path = get_resource_path('ui/splash_screen.kv')
Builder.load_file(kv_path)


class SplashScreen(Screen):
    """Заставка при запуске: показывает логотип и переходит в меню."""

    presplash_source = _PRESPLASH

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._timer = None

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
