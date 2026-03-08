"""Точка входа в приложение Green Energy City."""

import os
import sys

# Принудительный портретный режим
os.environ.setdefault("KIVY_ORIENTATION", "Portrait")

from kivy.config import Config

# На Android не устанавливаем фиксированный размер — используем родное разрешение.
# На десктопе задаём окно 400×700 для удобства разработки.
_is_android = hasattr(sys, 'getandroidapilevel') or os.environ.get('ANDROID_ARGUMENT')
if not _is_android:
    Config.set("graphics", "width", "400")
    Config.set("graphics", "height", "700")
    Config.set("graphics", "resizable", "0")

# Полноэкранный режим: скрывает системную строку состояния Android
Config.set("graphics", "fullscreen", "auto")

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition

# Цвет фона приложения — заполняет всю область окна, включая края на
# телефонах с вытянутым экраном, чтобы не было чёрных полос.
_BG_COLOR = (0.04, 0.13, 0.04, 1)
Window.clearcolor = _BG_COLOR


def _enable_immersive_mode():
    """Включить режим погружения (immersive sticky) на Android.

    Скрывает системную строку состояния и навигационную панель.
    При касании края экрана панели кратко появляются и снова прячутся.
    На не-Android платформах вызов игнорируется.
    """
    try:
        from android.runnable import run_on_ui_thread  # type: ignore[import]
        from jnius import autoclass                     # type: ignore[import]
    except ImportError:
        # Не Android или jnius не установлен — пропускаем
        return

    @run_on_ui_thread
    def _set_flags():
        View     = autoclass('android.view.View')
        Activity = autoclass('org.kivy.android.PythonActivity')
        window   = Activity.mActivity.getWindow()
        decor    = window.getDecorView()
        flags = (
            View.SYSTEM_UI_FLAG_LAYOUT_STABLE
            | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
            | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
            | View.SYSTEM_UI_FLAG_FULLSCREEN
            | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
        )
        decor.setSystemUiVisibility(flags)

    _set_flags()


from ui.menu_screen import MenuScreen
from ui.game_screen import GameScreen
from ui.gameover_screen import GameOverScreen


class GreenEnergyCityApp(App):
    """Главное Kivy-приложение Green Energy City."""

    def build(self):
        self.title = "Green Energy City"
        # Включить режим погружения на Android (системная панель скрыта)
        _enable_immersive_mode()
        # Повторно задать clearcolor после инициализации Window
        Window.clearcolor = _BG_COLOR
        # Менеджер экранов с плавным переходом между ними
        sm = ScreenManager(transition=FadeTransition(duration=0.2))
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(GameOverScreen(name="gameover"))
        return sm


if __name__ == "__main__":
    GreenEnergyCityApp().run()
