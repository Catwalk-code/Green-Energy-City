"""Основной игровой экран для Green Energy City."""

import os

from kivy.uix.screenmanager import Screen
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
from game.resources import resource_path
from ui.swipe_card import SwipeCard

# Путь к иконке-точке для обозначения затрагиваемых характеристик
_ICON_POINT = resource_path(os.path.join('data', 'icons', 'point.png'))
# Иконка кнопки "В главное меню" - три полосы (PNG вместо символа)
_ICON_MENU = resource_path(os.path.join('data', 'icons', 'menu.png'))

Builder.load_file(resource_path(os.path.join('ui', 'game_screen.kv')))


class _IconButton(ButtonBehavior, Image):
    """Нажимаемая кнопка-иконка (PNG-картинка с поведением кнопки)."""


class _StatBar(BoxLayout):
    from kivy.properties import StringProperty, NumericProperty, BooleanProperty

    # Путь к PNG-иконке характеристики
    icon = StringProperty("")
    label_text = StringProperty("")
    stat_value = NumericProperty(50)
    # Путь к иконке-точке (показывается во время тяги карточки)
    point_icon = StringProperty(_ICON_POINT)
    # True - показать точку над иконкой; False - скрыть
    dot_visible = BooleanProperty(False)


class GameScreen(Screen):
    """Игровой экран со свайп-карточками и панелью характеристик."""

    menu_icon = _ICON_MENU

    # Пары (ключ стата, путь к иконке, ключ перевода подписи)
    _STAT_META = [
        ("energy", GameState.STAT_ICONS["energy"], "stat_energy"),
        ("economy", GameState.STAT_ICONS["economy"], "stat_economy"),
        ("environment", GameState.STAT_ICONS["environment"], "stat_environment"),
        ("happiness", GameState.STAT_ICONS["happiness"], "stat_happiness"),
    ]

    def __init__(self, **kwargs):
        self.game_state = GameState()
        self._stat_bars: dict[str, _StatBar] = {}
        self._current_card: SwipeCard | None = None
        # Данные сохранения для загрузки при входе на экран (None = новая игра)
        self._load_save_data: dict | None = None
        # Флаг для предотвращения открытия нескольких popup одновременно
        self._exit_popup_open: bool = False
        self._root_layout = None
        self._year_label = None
        self._card_area = None
        self._menu_btn = None
        super().__init__(**kwargs)

    def on_kv_post(self, _base_widget):
        self._root_layout = self.ids.root_layout
        self._year_label = self.ids.year_label
        self._card_area = self.ids.card_area
        self._menu_btn = self.ids.menu_btn
        self._menu_btn.bind(on_release=self._on_menu_btn)
        self._build_stats_panel()
        self.bind(size=self._on_size)
        self._on_size()

    def _build_stats_panel(self):
        stats_panel = self.ids.stats_panel
        stats_panel.clear_widgets()
        self._stat_bars = {}
        for stat, icon, label_key in self._STAT_META:
            bar = _StatBar(icon=icon, label_text=i18n.t(label_key), stat_value=50)
            self._stat_bars[stat] = bar
            stats_panel.add_widget(bar)

    def _on_size(self, *_):
        w, h = self.size
        stats_h = dp(100)
        year_h = dp(36)
        year_y = h - stats_h - year_h - dp(4)
        self._year_label.y = year_y

        area_h = h - stats_h - year_h - dp(10)
        self._card_area.y = 0
        self._card_area.height = area_h

        if self._current_card:
            self._centre_card(self._current_card)

    def _centre_card(self, card):
        """Разместить карточку в центре области карточек."""
        area = self._card_area
        card.x = (area.width - card.width) / 2
        card.y = (area.height - card.height) / 2

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

    def _on_keyboard(self, _window, key, *_args):
        """Перехватить системную кнопку "Назад" (keycode 27 / ESC на Android).

        Возвращает ``True``, если событие поглощено (приложение не закрывается),
        иначе ``False`` для обычной обработки.
        """
        if key == 27:  # Android back / ESC
            self._show_exit_popup()
            return True
        return False

    def _on_menu_btn(self, *_):
        """Нажатие кнопки "Гамбургер-меню" - открыть popup подтверждения выхода."""
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
            # Подсказка свайпа без стрелок (они - картинки в самом виджете)
            swipe_hint=i18n.t('swipe_hint'),
        )
        card.swipe_callback = self._on_swipe
        # Подключить обратный вызов для точек-индикаторов затрагиваемых статов
        card.drag_callback = self._on_drag
        self._current_card = card

        self._centre_card(card)

        # Анимация появления снизу
        orig_y = card.y
        card.y = -card.height
        card.opacity = 0
        self._card_area.add_widget(card)

        Animation(y=orig_y, opacity=1, duration=0.28, t="out_back").start(card)

    def _on_swipe(self, direction):
        """Обработать свайп: передать выбор игровому состоянию."""
        continues = self.game_state.apply_choice(direction)
        self._refresh_stats()
        if continues:
            save_game(self.game_state)
            self._show_card()
        else:
            self._go_to_game_over()

    def _on_drag(self, direction):
        """Показать/скрыть точки над статами при тяге карточки.

        Args:
            direction: 'left' / 'right' - показать точки на статах,
                       которые изменятся при этом выборе; None - скрыть все.
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
        # Игра завершена - сохранение больше не актуально
        delete_save()
        go_screen = self.manager.get_screen("gameover")
        go_screen.setup(
            win=self.game_state.win,
            reason=self.game_state.game_over_reason,
            year=self.game_state.year,
            decisions=self.game_state.decisions_count,
        )
        self.manager.current = "gameover"
