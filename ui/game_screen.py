"""Основной игровой экран для Green Energy City."""

from __future__ import annotations

import os

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp

from game.state import GameState
from game.save import save_game, delete_save
from game import i18n
from ui.swipe_card import SwipeCard

# Путь к иконке-точке для обозначения затрагиваемых характеристик
_ICON_POINT = os.path.join('data', 'icons', 'point.png')
# Иконка кнопки "В главное меню" — три полосы (PNG вместо символа ☰)
_ICON_MENU  = os.path.join('data', 'icons', 'menu.png')


class _IconButton(ButtonBehavior, Image):
    """Нажимаемая кнопка-иконка (PNG-картинка с поведением кнопки)."""

Builder.load_string("""
<_StatBar>:
    orientation: 'vertical'
    spacing: dp(2)
    # Точка — появляется над иконкой, когда тяга карточки затрагивает этот стат
    Image:
        source: root.point_icon
        size_hint_y: None
        height: dp(10)
        allow_stretch: True
        keep_ratio: True
        opacity: 1 if root.dot_visible else 0
    # Иконка характеристики — PNG-картинка
    Image:
        source: root.icon
        size_hint_y: None
        height: dp(30)
        allow_stretch: True
        keep_ratio: True
    ProgressBar:
        id: pb
        max: 100
        value: root.stat_value
        size_hint_y: None
        height: dp(8)
    Label:
        text: root.label_text
        font_size: sp(13)
        color: 0.85, 0.85, 0.85, 1
        size_hint_y: None
        height: dp(24)
        halign: 'center'
        text_size: self.size
        valign: 'top'

<GameScreen>:
    canvas.before:
        Color:
            rgba: 0.04, 0.13, 0.04, 1
        Rectangle:
            pos: self.pos
            size: self.size
""")


class _StatBar(BoxLayout):
    from kivy.properties import StringProperty, NumericProperty, BooleanProperty
    # Путь к PNG-иконке характеристики
    icon        = StringProperty("")
    label_text  = StringProperty("")
    stat_value  = NumericProperty(50)
    # Путь к иконке-точке (показывается во время тяги карточки)
    point_icon  = StringProperty(_ICON_POINT)
    # True — показать точку над иконкой; False — скрыть
    dot_visible = BooleanProperty(False)


class GameScreen(Screen):
    """Игровой экран со свайп-карточками и панелью характеристик."""

    # Пары (ключ стата, путь к иконке, ключ перевода подписи)
    _STAT_META = [
        ("energy",      GameState.STAT_ICONS["energy"],      "stat_energy"),
        ("economy",     GameState.STAT_ICONS["economy"],     "stat_economy"),
        ("environment", GameState.STAT_ICONS["environment"], "stat_environment"),
        ("happiness",   GameState.STAT_ICONS["happiness"],   "stat_happiness"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_state = GameState()
        self._stat_bars: dict[str, _StatBar] = {}
        self._current_card: SwipeCard | None = None
        # Данные сохранения для загрузки при входе на экран (None = новая игра)
        self._load_save_data: dict | None = None
        # Флаг для предотвращения открытия нескольких popup одновременно
        self._exit_popup_open: bool = False
        self._build_ui()

    
    # Построение интерфейса
    
    def _build_ui(self):
        root = FloatLayout()

        #  Панель характеристик (вверху экрана) 
        stats_panel = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(100),
            pos_hint={"top": 1},
            padding=(dp(10), dp(6)),
            spacing=dp(6),
        )
        for stat, icon, label_key in self._STAT_META:
            bar = _StatBar(icon=icon, label_text=i18n.t(label_key), stat_value=50)
            self._stat_bars[stat] = bar
            stats_panel.add_widget(bar)
        root.add_widget(stats_panel)

        #  Метка текущего года (начинается с 2026) 
        self._year_label = Label(
            text="2026",
            font_size="28sp",
            bold=True,
            color=(0.6, 1.0, 0.6, 1),
            size_hint=(None, None),
            size=(dp(140), dp(36)),
            pos_hint={"center_x": 0.5},
            halign="center",
        )
        root.add_widget(self._year_label)

        #  Область для карточек (центр ниже панели статов) 
        self._card_area = FloatLayout(
            size_hint=(1, None),
        )
        root.add_widget(self._card_area)

        self.add_widget(root)
        self._root_layout = root

        #  Кнопка "В главное меню" (стрелка влево) в левом нижнем углу 
        self._menu_btn = _IconButton(
            source=_ICON_MENU,
            size_hint=(None, None),
            size=(dp(44), dp(44)),
            pos_hint={"x": 0.02, "y": 0.02},
            allow_stretch=True,
            keep_ratio=True,
        )
        self._menu_btn.bind(on_release=self._on_menu_btn)
        root.add_widget(self._menu_btn)

        self.bind(size=self._on_size)

    def _on_size(self, *_):
        w, h = self.size
        stats_h = dp(100)
        year_h  = dp(36)
        year_y  = h - stats_h - year_h - dp(4)
        self._year_label.y = year_y

        area_h = h - stats_h - year_h - dp(10)
        self._card_area.y      = 0
        self._card_area.height = area_h

        if self._current_card:
            self._centre_card(self._current_card)

    def _centre_card(self, card: SwipeCard):
        """Разместить карточку в центре области карточек."""
        area  = self._card_area
        card.x = (area.width  - card.width)  / 2
        card.y = (area.height - card.height) / 2

    
    # Жизненный цикл экрана
    

    def on_enter(self):
        # Обновить подписи статов в соответствии с текущим языком
        for stat, _icon, label_key in self._STAT_META:
            self._stat_bars[stat].label_text = i18n.t(label_key)
        # Привязать обработчик системной кнопки "Назад" (Android)
        Window.bind(on_keyboard=self._on_keyboard)
        # Загрузить сохранение или начать новую игру
        if self._load_save_data is not None:
            self.game_state.restore(self._load_save_data)
            self._load_save_data = None
        else:
            self.game_state.reset()
        self._refresh_stats()
        self._show_card()

    def on_leave(self):
        # Отвязать обработчик клавиатуры при уходе с экрана
        Window.unbind(on_keyboard=self._on_keyboard)
        self._exit_popup_open = False

    
    # Навигация: кнопка ☰ и системная кнопка "Назад"
    

    def _on_keyboard(self, _window, key, *_args) -> bool:
        """Перехватить системную кнопку «Назад» (keycode 27 / ESC на Android).

        Returns:
            ``True`` — событие поглощено (приложение не закрывается);
            ``False`` — обычная обработка.
        """
        if key == 27:  # Android back / ESC
            self._show_exit_popup()
            return True
        return False

    def _on_menu_btn(self, *_):
        """Нажатие кнопки ☰ — открыть popup подтверждения выхода."""
        self._show_exit_popup()

    def _show_exit_popup(self):
        """Показать модальное окно подтверждения сохранения и выхода в меню."""
        if self._exit_popup_open:
            return
        self._exit_popup_open = True

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=(dp(12), dp(8)),
        )
        lbl_body = Label(
            text=i18n.t("back_popup_body"),
            font_size="15sp",
            color=(0.85, 0.95, 0.85, 1),
            halign="center",
            valign="middle",
            size_hint_y=1,
        )
        lbl_body.bind(
            size=lambda lbl, val: setattr(lbl, "text_size", (val[0], None))
        )
        content.add_widget(lbl_body)

        buttons = BoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(60),
        )

        popup = Popup(
            title=i18n.t("back_popup_title"),
            content=content,
            size_hint=(0.85, None),
            height=dp(220),
            auto_dismiss=False,
            separator_color=(0.15, 0.7, 0.15, 1),
            title_color=(0.4, 1.0, 0.4, 1),
        )

        def _do_continue(*_):
            self._exit_popup_open = False
            popup.dismiss()

        def _do_save_exit(*_):
            save_game(self.game_state)
            self._exit_popup_open = False
            popup.dismiss()
            self.manager.current = "menu"

        btn_continue = Button(
            text=i18n.t("continue_game"),
            font_size="14sp",
            bold=True,
            halign="center",
            valign="middle",
            background_color=(0.15, 0.7, 0.15, 1),
            color=(1, 1, 1, 1),
        )
        btn_continue.bind(
            size=lambda btn, val: setattr(btn, "text_size", (val[0], None))
        )
        btn_continue.bind(on_release=_do_continue)

        btn_exit = Button(
            text=i18n.t("save_and_exit"),
            font_size="14sp",
            bold=True,
            halign="center",
            valign="middle",
            background_color=(0.55, 0.2, 0.1, 1),
            color=(1, 1, 1, 1),
        )
        btn_exit.bind(
            size=lambda btn, val: setattr(btn, "text_size", (val[0], None))
        )
        btn_exit.bind(on_release=_do_save_exit)

        buttons.add_widget(btn_continue)
        buttons.add_widget(btn_exit)
        content.add_widget(buttons)

        popup.open()

    
    # Отображение карточек
    
    def _show_card(self):
        """Показать текущую карточку игрового состояния с анимацией появления."""
        # Сбросить точки при смене карточки
        self._clear_dots()
        self._card_area.clear_widgets()
        gc = self.game_state.current_card

        card = SwipeCard(
            character_name=gc.character,
            card_text=gc.text,
            left_text=gc.left_choice.text,
            right_text=gc.right_choice.text,
            # Подсказка свайпа без стрелок (они — картинки в самом виджете)
            swipe_hint=i18n.t('swipe_hint'),
        )
        card.swipe_callback = self._on_swipe
        # Подключить обратный вызов для точек-индикаторов затрагиваемых статов
        card.drag_callback  = self._on_drag
        self._current_card  = card

        self._centre_card(card)

        # Анимация появления снизу
        orig_y  = card.y
        card.y  = -card.height
        card.opacity = 0
        self._card_area.add_widget(card)

        Animation(y=orig_y, opacity=1, duration=0.28, t="out_back").start(card)

    
    # Обратные вызовы игровой логики
    
    def _on_swipe(self, direction: str):
        """Обработать свайп: передать выбор игровому состоянию."""
        continues = self.game_state.apply_choice(direction)
        self._refresh_stats()
        if continues:
            save_game(self.game_state)
            self._show_card()
        else:
            self._go_to_game_over()

    def _on_drag(self, direction: str | None):
        """Показать/скрыть точки над статами при тяге карточки.

        Args:
            direction: 'left' / 'right' — показать точки на статах,
                       которые изменятся при этом выборе; None — скрыть все.
        """
        if direction is None:
            self._clear_dots()
            return
        card = self.game_state.current_card
        choice = card.right_choice if direction == "right" else card.left_choice
        affected = set(choice.effects.keys())
        for stat, bar in self._stat_bars.items():
            bar.dot_visible = stat in affected

    def _clear_dots(self):
        """Скрыть точки-индикаторы на всех полосах статов."""
        for bar in self._stat_bars.values():
            bar.dot_visible = False

    def _refresh_stats(self):
        """Обновить визуальные полосы статов и метку года."""
        for stat, bar in self._stat_bars.items():
            bar.stat_value = self.game_state.stats[stat]
        self._year_label.text = str(self.game_state.year)

    def _go_to_game_over(self):
        """Передать результат на экран конца игры и перейти туда."""
        # Игра завершена — сохранение больше не актуально
        delete_save()
        go_screen = self.manager.get_screen("gameover")
        go_screen.setup(
            win=self.game_state.win,
            reason=self.game_state.game_over_reason,
            year=self.game_state.year,
            decisions=self.game_state.decisions_count,
        )
        self.manager.current = "gameover"
