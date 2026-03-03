"""Экран главного меню для Green Energy City."""

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.lang import Builder

from game.state import GameState
from game import i18n

Builder.load_string("""
<MenuScreen>:
    canvas.before:
        Color:
            rgba: 0.04, 0.13, 0.04, 1
        Rectangle:
            pos: self.pos
            size: self.size
""")


class MenuScreen(Screen):
    """Экран запуска с названием игры и кнопкой начала."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ссылки на виджеты с переводимым текстом
        self._subtitle_label = None
        self._play_btn       = None
        self._legend_label   = None
        self._lang_btn       = None
        self._build_ui()

    def _build_ui(self):
        root = FloatLayout()

        # ── Кнопка смены языка (верхний правый угол) ──────────────────
        self._lang_btn = Button(
            text=i18n.t('lang_toggle'),
            font_size="14sp",
            bold=True,
            size_hint=(None, None),
            size=(dp(52), dp(36)),
            pos_hint={"right": 0.98, "top": 0.98},
            background_color=(0.1, 0.4, 0.1, 1),
            color=(0.9, 1.0, 0.9, 1),
        )
        self._lang_btn.bind(on_release=self._toggle_lang)
        root.add_widget(self._lang_btn)

        # ── Основной вертикальный блок (центр экрана) ─────────────────
        col = BoxLayout(
            orientation="vertical",
            size_hint=(0.8, None),
            height=dp(380),
            pos_hint={"center_x": 0.5, "center_y": 0.52},
            spacing=dp(20),
            padding=(dp(20), dp(10)),
        )

        # Иконка города
        col.add_widget(Label(
            text="🏙️",
            font_size="72sp",
            size_hint_y=None,
            height=dp(100),
            halign="center",
        ))

        # Название игры (не переводится — является логотипом)
        col.add_widget(Label(
            text="Green Energy City",
            font_size="28sp",
            bold=True,
            color=(0.4, 1.0, 0.4, 1),
            size_hint_y=None,
            height=dp(50),
            halign="center",
        ))

        # Подзаголовок (переводится)
        self._subtitle_label = Label(
            text=i18n.t('menu_subtitle').format(year=GameState.WIN_YEAR),
            font_size="14sp",
            color=(0.75, 0.95, 0.75, 1),
            size_hint_y=None,
            height=dp(60),
            halign="center",
            text_size=(dp(280), None),
        )
        col.add_widget(self._subtitle_label)

        # Кнопка начала игры (переводится)
        self._play_btn = Button(
            text=i18n.t('play'),
            font_size="22sp",
            bold=True,
            size_hint=(None, None),
            size=(dp(200), dp(55)),
            background_color=(0.15, 0.7, 0.15, 1),
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5},
        )
        self._play_btn.bind(on_release=self._start_game)
        col.add_widget(self._play_btn)

        # Легенда статов (переводится)
        self._legend_label = Label(
            text=i18n.t('stats_legend'),
            font_size="12sp",
            color=(0.6, 0.85, 0.6, 1),
            size_hint_y=None,
            height=dp(40),
            halign="center",
            text_size=(dp(300), None),
        )
        col.add_widget(self._legend_label)

        root.add_widget(col)
        self.add_widget(root)

    def _toggle_lang(self, *_):
        """Переключить язык (EN ↔ RU) и обновить все переводимые надписи."""
        new_lang = 'ru' if i18n.get_lang() == 'en' else 'en'
        i18n.set_lang(new_lang)
        self._update_labels()

    def _update_labels(self):
        """Обновить тексты всех переводимых виджетов меню."""
        self._subtitle_label.text = i18n.t('menu_subtitle').format(year=GameState.WIN_YEAR)
        self._play_btn.text       = i18n.t('play')
        self._legend_label.text   = i18n.t('stats_legend')
        self._lang_btn.text       = i18n.t('lang_toggle')

    def _start_game(self, *_):
        """Перейти к игровому экрану."""
        self.manager.current = "game"
