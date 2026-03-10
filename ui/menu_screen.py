"""Экран главного меню для Green Energy City."""

import os
from functools import partial

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.lang import Builder

from game.state import GameState
from game import i18n

# Путь к иконке приложения (отображается вместо эмодзи)
_APP_ICON = os.path.join('data', 'splash', 'icon.png')

Builder.load_string("""
<MenuScreen>:
    canvas.before:
        Color:
            rgba: 0.04, 0.13, 0.04, 1
        Rectangle:
            pos: self.pos
            size: self.size
""")

# Цвета кнопок сложности: активная / неактивная
_DIFF_ACTIVE   = (0.1, 0.65, 0.1, 1)
_DIFF_INACTIVE = (0.15, 0.35, 0.15, 1)

# Единственный источник правды для уровней сложности —
# ключ перевода i18n и год победы из GameState.DIFFICULTY_YEARS
_DIFFICULTY_OPTIONS = list(zip(
    ['difficulty_easy', 'difficulty_medium', 'difficulty_hard'],
    GameState.DIFFICULTY_YEARS.values(),   # [2030, 2035, 2040]
))


class MenuScreen(Screen):
    """Экран запуска с названием игры, выбором сложности и кнопкой начала."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ссылки на виджеты с переводимым текстом
        self._subtitle_label   = None
        self._play_btn         = None
        self._lang_btn         = None
        self._difficulty_label = None
        # Кнопки сложности в порядке: лёгкий, средний, сложный
        self._diff_btns: list[Button] = []
        # Выбранный год победы (по умолчанию — сложный уровень, 2040)
        self._selected_year = 2040
        self._build_ui()

    def _build_ui(self):
        root = FloatLayout()

        # ── Кнопка смены языка (верхний правый угол) ──────────────────
        self._lang_btn = Button(
            text=i18n.t('lang_toggle'),
            font_size="16sp",
            bold=True,
            size_hint=(None, None),
            size=(dp(60), dp(40)),
            pos_hint={"right": 0.98, "top": 0.98},
            background_color=(0.1, 0.4, 0.1, 1),
            color=(0.9, 1.0, 0.9, 1),
        )
        self._lang_btn.bind(on_release=self._toggle_lang)
        root.add_widget(self._lang_btn)

        # ── Основной вертикальный блок (центр экрана) ─────────────────
        col = BoxLayout(
            orientation="vertical",
            size_hint=(0.85, None),
            height=dp(515),
            pos_hint={"center_x": 0.5, "center_y": 0.52},
            spacing=dp(14),
            padding=(dp(16), dp(8)),
        )

        # Иконка приложения (PNG вместо эмодзи)
        col.add_widget(Image(
            source=_APP_ICON,
            size_hint_y=None,
            height=dp(120),
            allow_stretch=True,
            keep_ratio=True,
        ))

        # Название игры (логотип, не переводится)
        col.add_widget(Label(
            text="Green Energy City",
            font_size="32sp",
            bold=True,
            color=(0.4, 1.0, 0.4, 1),
            size_hint_y=None,
            height=dp(50),
            halign="center",
        ))

        # Подзаголовок — без указания конкретного года (переводится)
        self._subtitle_label = Label(
            text=i18n.t('menu_subtitle'),
            font_size="16sp",
            color=(0.75, 0.95, 0.75, 1),
            size_hint_y=None,
            height=dp(60),
            halign="center",
            text_size=(dp(290), None),
        )
        col.add_widget(self._subtitle_label)

        # ── Раздел выбора сложности ───────────────────────────────────
        self._difficulty_label = Label(
            text=i18n.t('difficulty_label'),
            font_size="15sp",
            color=(0.65, 0.9, 0.65, 1),
            size_hint_y=None,
            height=dp(26),
            halign="center",
        )
        col.add_widget(self._difficulty_label)

        # Три кнопки сложности в горизонтальный ряд
        diff_row = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(52),
            spacing=dp(8),
        )
        self._diff_btns = []
        for key, year in _DIFFICULTY_OPTIONS:
            is_default = (year == self._selected_year)
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
        col.add_widget(diff_row)

        # Кнопка начала игры (переводится)
        self._play_btn = Button(
            text=i18n.t('play'),
            font_size="26sp",
            bold=True,
            size_hint=(None, None),
            size=(dp(220), dp(60)),
            background_color=(0.15, 0.7, 0.15, 1),
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5},
        )
        self._play_btn.bind(on_release=self._start_game)
        col.add_widget(self._play_btn)

        root.add_widget(col)
        self.add_widget(root)

    # ------------------------------------------------------------------
    # Обработчики событий
    # ------------------------------------------------------------------

    def _select_difficulty(self, year: int, *_):
        """Выбрать уровень сложности и визуально выделить кнопку."""
        self._selected_year = year
        GameState.set_difficulty(year)
        # Обновить цвет всех кнопок сложности на основе _DIFFICULTY_OPTIONS
        for btn, (_, btn_year) in zip(self._diff_btns, _DIFFICULTY_OPTIONS):
            btn.background_color = _DIFF_ACTIVE if btn_year == year else _DIFF_INACTIVE

    def _toggle_lang(self, *_):
        """Переключить язык (EN ↔ RU) и обновить все переводимые надписи."""
        new_lang = 'ru' if i18n.get_lang() == 'en' else 'en'
        i18n.set_lang(new_lang)
        self._update_labels()

    def _update_labels(self):
        """Обновить тексты всех переводимых виджетов меню."""
        self._subtitle_label.text   = i18n.t('menu_subtitle')
        self._play_btn.text         = i18n.t('play')
        self._lang_btn.text         = i18n.t('lang_toggle')
        self._difficulty_label.text = i18n.t('difficulty_label')
        # Обновить тексты кнопок сложности через единый список _DIFFICULTY_OPTIONS
        for btn, (key, _) in zip(self._diff_btns, _DIFFICULTY_OPTIONS):
            btn.text = i18n.t(key)

    def _start_game(self, *_):
        """Перейти к игровому экрану."""
        self.manager.current = "game"
