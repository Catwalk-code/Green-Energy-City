"""Экран конца игры для Green Energy City."""

import os

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.lang import Builder

from game import i18n

# Пути к иконкам результата игры
_WIN_ICON  = os.path.join('data', 'icons', 'win.png')
_LOSE_ICON = os.path.join('data', 'icons', 'lose.png')

Builder.load_string("""
<GameOverScreen>:
    canvas.before:
        Color:
            rgba: 0.04, 0.13, 0.04, 1
        Rectangle:
            pos: self.pos
            size: self.size
""")


class GameOverScreen(Screen):
    """Показывается при завершении игры (победа или поражение)."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Данные результата игры, переданные из GameScreen
        self._win       = False
        self._reason    = ""
        self._year      = 2026
        self._decisions = 0
        # Ссылки на виджеты, обновляемые при входе на экран
        self._result_icon      = None   # Image win.png / lose.png
        self._title_label      = None
        self._reason_label     = None
        self._stats_label      = None
        self._play_again_btn   = None
        self._menu_btn         = None
        self._build_ui()

    def setup(self, *, win, reason, year, decisions):
        """Сохранить результат игры для отображения при входе на экран."""
        self._win       = win
        self._reason    = reason
        self._year      = year
        self._decisions = decisions

    def on_enter(self):
        """Обновить все надписи экрана по текущему языку и результату игры."""
        # Показать иконку победы или поражения
        if self._result_icon:
            self._result_icon.source = _WIN_ICON if self._win else _LOSE_ICON

        if self._title_label:
            if self._win:
                self._title_label.text  = i18n.t('win_title')
                self._title_label.color = (0.3, 1.0, 0.3, 1)
            else:
                self._title_label.text  = i18n.t('lose_title')
                self._title_label.color = (1.0, 0.35, 0.35, 1)

        if self._reason_label:
            self._reason_label.text = self._reason

        if self._stats_label:
            self._stats_label.text = (
                i18n.t('year_reached').format(self._year) + "\n" +
                i18n.t('decisions_made').format(self._decisions)
            )

        # Обновить тексты кнопок в соответствии с текущим языком
        if self._play_again_btn:
            self._play_again_btn.text = i18n.t('play_again')
        if self._menu_btn:
            self._menu_btn.text = i18n.t('main_menu')

    def _build_ui(self):
        root = FloatLayout()

        col = BoxLayout(
            orientation="vertical",
            size_hint=(0.85, None),
            height=dp(460),
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            spacing=dp(14),
            padding=(dp(20), dp(10)),
        )

        # Иконка результата (win.png / lose.png) вместо эмодзи
        self._result_icon = Image(
            source="",          # устанавливается в on_enter()
            size_hint=(None, None),
            size=(dp(72), dp(72)),
            pos_hint={"center_x": 0.5},
            allow_stretch=True,
            keep_ratio=True,
        )
        col.add_widget(self._result_icon)

        # Заголовок результата (победа / поражение) — без эмодзи
        self._title_label = Label(
            text="",
            font_size="30sp",
            bold=True,
            size_hint_y=None,
            height=dp(50),
            halign="center",
        )
        col.add_widget(self._title_label)

        # Текст причины конца игры
        self._reason_label = Label(
            text="",
            font_size="15sp",
            color=(0.85, 0.95, 0.85, 1),
            size_hint_y=None,
            height=dp(80),
            halign="center",
            text_size=(dp(280), None),
        )
        col.add_widget(self._reason_label)

        # Сводная статистика (год, количество решений)
        self._stats_label = Label(
            text="",
            font_size="14sp",
            color=(0.65, 0.85, 0.65, 1),
            size_hint_y=None,
            height=dp(55),
            halign="center",
        )
        col.add_widget(self._stats_label)

        # Кнопка "Играть снова"
        self._play_again_btn = Button(
            text=i18n.t('play_again'),
            font_size="20sp",
            bold=True,
            size_hint=(None, None),
            size=(dp(200), dp(55)),
            background_color=(0.15, 0.7, 0.15, 1),
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5},
        )
        self._play_again_btn.bind(on_release=self._play_again)
        col.add_widget(self._play_again_btn)

        # Кнопка "Главное меню"
        self._menu_btn = Button(
            text=i18n.t('main_menu'),
            font_size="16sp",
            size_hint=(None, None),
            size=(dp(200), dp(44)),
            background_color=(0.2, 0.4, 0.2, 1),
            color=(0.9, 0.9, 0.9, 1),
            pos_hint={"center_x": 0.5},
        )
        self._menu_btn.bind(on_release=self._go_menu)
        col.add_widget(self._menu_btn)

        root.add_widget(col)
        self.add_widget(root)

    def _play_again(self, *_):
        """Начать новую игру."""
        self.manager.current = "game"

    def _go_menu(self, *_):
        """Вернуться в главное меню."""
        self.manager.current = "menu"
