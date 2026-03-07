"""Точка входа в приложение Green Energy City."""

import os

# Принудительный портретный режим и фиксированный размер окна (имитация телефона)
os.environ.setdefault("KIVY_ORIENTATION", "Portrait")

from kivy.config import Config
Config.set("graphics", "width", "400")
Config.set("graphics", "height", "700")
Config.set("graphics", "resizable", "0")
# Полноэкранный режим: скрывает системную строку состояния Android
Config.set("graphics", "fullscreen", "auto")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition


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
        # Менеджер экранов с плавным переходом между ними
        sm = ScreenManager(transition=FadeTransition(duration=0.2))
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(GameOverScreen(name="gameover"))
        return sm


if __name__ == "__main__":
    GreenEnergyCityApp().run()
