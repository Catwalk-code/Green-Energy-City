"""Точка входа в приложение Green Energy City."""

import os
import sys

def get_resource_path(relative_path):
    """Возвращает корректный путь как для разработки, так и для .exe"""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
    
# Принудительный портретный режим
os.environ.setdefault("KIVY_ORIENTATION", "Portrait")

# Цвет фона устанавливается через переменную среды ДО инициализации Kivy,
# чтобы на Android не было чёрной полосы сверху на вытянутых экранах.
os.environ.setdefault("KIVY_BCK_COLOR", "0.04,0.13,0.04,1")

from kivy.config import Config

# На Android не устанавливаем фиксированный размер - используем родное разрешение.
# На десктопе задаём окно 400×700 для удобства разработки.
_is_android = hasattr(sys, 'getandroidapilevel') or os.environ.get('ANDROID_ARGUMENT')
if not _is_android:
    Config.set("graphics", "width", "400")
    Config.set("graphics", "height", "700")
    Config.set("graphics", "resizable", "0")
    # Полноэкранный режим только на десктопе; на Android управляет buildozer.spec
    Config.set("graphics", "fullscreen", "auto")

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition

# Цвет фона приложения заполняет всю область окна, включая края на
# телефонах с вытянутым экраном, чтобы не было чёрных полос.
_BG_COLOR = (0.04, 0.13, 0.04, 1)
Window.clearcolor = _BG_COLOR


def _enable_immersive_mode():
    """Включить режим погружения (immersive sticky) на Android.

    Скрывает системную строку состояния и навигационную панель.
    При касании края экрана панели кратко появляются и снова прячутся.
    Также распространяет контент за вырез экрана (notch/punch-hole),
    чтобы не было чёрной полосы сверху на устройствах с таким вырезом.
    На не-Android платформах вызов игнорируется.
    """
    try:
        from android.runnable import run_on_ui_thread  # type: ignore[import]
        from jnius import autoclass                     # type: ignore[import]
    except ImportError:
        # Не Android или jnius не установлен - пропускаем
        return

    @run_on_ui_thread
    def _set_flags():
        Activity         = autoclass('org.kivy.android.PythonActivity')
        Build_VERSION    = autoclass('android.os.Build$VERSION')
        activity         = Activity.mActivity
        window           = activity.getWindow()
        decor            = window.getDecorView()

        # Расширить контент за вырез (notch) на API 28+ (Android 9+).
        # LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES = 1
        # Без этого система оставляет чёрную полосу высотой выреза у края экрана.
        try:
            WindowManager_LayoutParams = autoclass(
                'android.view.WindowManager$LayoutParams'
            )
            lp = window.getAttributes()
            lp.layoutInDisplayCutoutMode = (
                WindowManager_LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES
            )
            window.setAttributes(lp)
        except Exception:
            pass

        if Build_VERSION.SDK_INT >= 30:
            # API 30+ (Android 11+): WindowInsetsController
            # setSystemUiVisibility устарел; используем новый API.
            try:
                WindowInsetsController = autoclass(
                    'android.view.WindowInsetsController'
                )
                WindowInsets_Type = autoclass('android.view.WindowInsets$Type')
                controller = window.getInsetsController()
                if controller is not None:
                    controller.hide(
                        WindowInsets_Type.statusBars()
                        | WindowInsets_Type.navigationBars()
                    )
                    controller.setSystemBarsBehavior(
                        WindowInsetsController.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
                    )
            except Exception:
                pass
        else:
            # API 21-29: устаревшие флаги - всё ещё поддерживаются
            View = autoclass('android.view.View')
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


from ui.splash_screen import SplashScreen
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
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(GameOverScreen(name="gameover"))
        # На Android нативная presplash (buildozer.spec) уже показала логотип
        # пока грузилось приложение - повторный показ Python-заставки вызывает
        # мерцание. Сразу переходим в меню. На десктопе показываем заставку.
        sm.current = "menu" if _is_android else "splash"
        return sm

    def on_start(self):
        """Проверить наличие сохранения при запуске приложения."""
        from kivy.clock import Clock
        Clock.schedule_once(self._check_save, 0.1)

    def _check_save(self, *_):
        """Показать popup загрузки сохранения, если файл save.json найден."""
        from game.save import has_save, load_save, delete_save
        from game import i18n
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.metrics import dp

        if not has_save():
            return

        data = load_save()
        if data is None:
            # Файл повреждён - удалить и запустить стандартно
            delete_save()
            return

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=(dp(12), dp(8)),
        )
        content.add_widget(Label(
            text=i18n.t("save_found_body"),
            font_size="15sp",
            color=(0.85, 0.95, 0.85, 1),
            halign="center",
            valign="middle",
            size_hint_y=1,
        ))

        buttons = BoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(50),
        )

        popup = Popup(
            title=i18n.t("save_found_title"),
            content=content,
            size_hint=(0.85, None),
            height=dp(200),
            auto_dismiss=False,
            separator_color=(0.15, 0.7, 0.15, 1),
            title_color=(0.4, 1.0, 0.4, 1),
        )

        def _new_game(*_):
            delete_save()
            popup.dismiss()

        def _continue_save(*_):
            popup.dismiss()
            game_screen = self.root.get_screen("game")
            game_screen._load_save_data = data
            self.root.current = "game"

        btn_new = Button(
            text=i18n.t("new_game"),
            font_size="14sp",
            bold=True,
            background_color=(0.2, 0.4, 0.2, 1),
            color=(1, 1, 1, 1),
        )
        btn_new.bind(on_release=_new_game)

        btn_continue = Button(
            text=i18n.t("continue_save"),
            font_size="14sp",
            bold=True,
            background_color=(0.15, 0.7, 0.15, 1),
            color=(1, 1, 1, 1),
        )
        btn_continue.bind(on_release=_continue_save)

        buttons.add_widget(btn_new)
        buttons.add_widget(btn_continue)
        content.add_widget(buttons)

        popup.open()

    def on_resume(self):
        # Повторно включить режим погружения при возврате из фона:
        # на Android система может восстановить строку состояния
        # после нажатия кнопки "Домой" или переключения приложений.
        _enable_immersive_mode()


if __name__ == "__main__":
    GreenEnergyCityApp().run()
