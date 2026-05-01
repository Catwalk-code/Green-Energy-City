"""Экран главного меню для Green Energy City."""

import os
from functools import partial

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.lang import Builder

from game.state import GameState
from game import i18n

# Путь к иконке приложения (отображается вместо эмодзи)
_APP_ICON = os.path.join('data', 'splash', 'icon.png')

Builder.load_file(os.path.join(os.path.dirname(__file__), 'menu_screen.kv'))

# Цвета кнопок сложности: активная / неактивная
_DIFF_ACTIVE = (0.1, 0.65, 0.1, 1)
_DIFF_INACTIVE = (0.15, 0.35, 0.15, 1)

# Единственный источник правды для уровней сложности -
# ключ перевода i18n и год победы из GameState.DIFFICULTY_YEARS
_DIFFICULTY_OPTIONS = list(zip(
    ['difficulty_easy', 'difficulty_medium', 'difficulty_hard'],
    GameState.DIFFICULTY_YEARS.values(),   # [2030, 2035, 2040]
))


class MenuScreen(Screen):
    """Экран запуска с названием игры, выбором сложности и кнопкой начала."""

    app_icon = _APP_ICON

    def __init__(self, **kwargs):
        # Кнопки сложности в порядке: лёгкий, средний, сложный
        self._diff_btns = []
        # Выбранный год победы (по умолчанию - сложный уровень, 2040)
        self._selected_year = 2040
        super().__init__(**kwargs)

    def on_kv_post(self, _base_widget):
        self.ids.play_btn.bind(on_release=self._start_game)
        self._build_difficulty_buttons()
        self._update_labels()

    def _build_difficulty_buttons(self):
        diff_row = self.ids.diff_row
        diff_row.clear_widgets()
        self._diff_btns = []
        for key, year in _DIFFICULTY_OPTIONS:
            is_default = year == self._selected_year
            btn = Button(
                text=i18n.t(key),
                font_size="14sp",
                bold=True,
                background_color=_DIFF_ACTIVE if is_default else _DIFF_INACTIVE,
                color=(1, 1, 1, 1),
            )
            btn.bind(on_release=partial(self._select_difficulty, year))
            self._diff_btns.append(btn)
            diff_row.add_widget(btn)

    def _select_difficulty(self, year, *_):
        """Выбрать уровень сложности и визуально выделить кнопку."""
        self._selected_year = year
        GameState.set_difficulty(year)
        # Обновить цвет всех кнопок сложности на основе _DIFFICULTY_OPTIONS
        for btn, (_, btn_year) in zip(self._diff_btns, _DIFFICULTY_OPTIONS):
            btn.background_color = _DIFF_ACTIVE if btn_year == year else _DIFF_INACTIVE

    def _update_labels(self):
        """Обновить тексты всех переводимых виджетов меню."""
        self.ids.subtitle_label.text = i18n.t('menu_subtitle')
        self.ids.play_btn.text = i18n.t('play')
        self.ids.difficulty_label.text = i18n.t('difficulty_label')
        # Обновить тексты кнопок сложности через единый список _DIFFICULTY_OPTIONS
        for btn, (key, _) in zip(self._diff_btns, _DIFFICULTY_OPTIONS):
            btn.text = i18n.t(key)

    def _start_game(self, *_):
        """Перейти к игровому экрану."""
        self.manager.current = "game"
