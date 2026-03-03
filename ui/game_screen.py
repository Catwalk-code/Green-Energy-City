"""Основной игровой экран для Green Energy City."""

from __future__ import annotations

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.metrics import dp

from game.state import GameState
from game import i18n
from ui.swipe_card import SwipeCard

Builder.load_string("""
<_StatBar>:
    orientation: 'vertical'
    spacing: dp(1)
    Label:
        text: root.icon
        font_size: sp(18)
        size_hint_y: None
        height: dp(22)
        halign: 'center'
    ProgressBar:
        id: pb
        max: 100
        value: root.stat_value
        size_hint_y: None
        height: dp(8)
    Label:
        text: root.label_text
        font_size: sp(9)
        color: 0.85, 0.85, 0.85, 1
        size_hint_y: None
        height: dp(14)
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
    from kivy.properties import StringProperty, NumericProperty
    icon       = StringProperty("")
    label_text = StringProperty("")
    stat_value = NumericProperty(50)


class GameScreen(Screen):
    """Игровой экран со свайп-карточками и панелью характеристик."""

    # Пары (ключ стата, иконка, ключ перевода подписи)
    _STAT_META = [
        ("energy",      "⚡", "stat_energy"),
        ("economy",     "💰", "stat_economy"),
        ("environment", "🌿", "stat_environment"),
        ("happiness",   "😊", "stat_happiness"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_state = GameState()
        self._stat_bars: dict[str, _StatBar] = {}
        self._current_card: SwipeCard | None = None
        self._build_ui()

    # ------------------------------------------------------------------
    # Построение интерфейса
    # ------------------------------------------------------------------

    def _build_ui(self):
        root = FloatLayout()

        # ── Панель характеристик (вверху экрана) ──────────────────────
        stats_panel = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(72),
            pos_hint={"top": 1},
            padding=(dp(10), dp(6)),
            spacing=dp(6),
        )
        for stat, icon, label_key in self._STAT_META:
            bar = _StatBar(icon=icon, label_text=i18n.t(label_key), stat_value=50)
            self._stat_bars[stat] = bar
            stats_panel.add_widget(bar)
        root.add_widget(stats_panel)

        # ── Метка текущего года ────────────────────────────────────────
        self._year_label = Label(
            text="2024",
            font_size="20sp",
            bold=True,
            color=(0.6, 1.0, 0.6, 1),
            size_hint=(None, None),
            size=(dp(120), dp(28)),
            pos_hint={"center_x": 0.5},
            halign="center",
        )
        root.add_widget(self._year_label)

        # ── Область для карточек (центр ниже панели статов) ───────────
        self._card_area = FloatLayout(
            size_hint=(1, None),
        )
        root.add_widget(self._card_area)

        self.add_widget(root)
        self._root_layout = root

        self.bind(size=self._on_size)

    def _on_size(self, *_):
        w, h = self.size
        stats_h = dp(72)
        year_h  = dp(28)
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

    # ------------------------------------------------------------------
    # Жизненный цикл экрана
    # ------------------------------------------------------------------

    def on_enter(self):
        # Обновить подписи статов в соответствии с текущим языком
        for stat, _icon, label_key in self._STAT_META:
            self._stat_bars[stat].label_text = i18n.t(label_key)
        # Начать новую игру
        self.game_state.reset()
        self._refresh_stats()
        self._show_card()

    # ------------------------------------------------------------------
    # Отображение карточек
    # ------------------------------------------------------------------

    def _show_card(self):
        """Показать текущую карточку игрового состояния с анимацией появления."""
        self._card_area.clear_widgets()
        gc = self.game_state.current_card

        card = SwipeCard(
            character_name=gc.character,
            card_text=gc.text,
            left_text=gc.left_choice.text,
            right_text=gc.right_choice.text,
            # Подсказка свайпа берётся из модуля переводов
            swipe_hint=i18n.t('swipe_hint'),
        )
        card.swipe_callback = self._on_swipe
        self._current_card  = card

        self._centre_card(card)

        # Анимация появления снизу
        orig_y  = card.y
        card.y  = -card.height
        card.opacity = 0
        self._card_area.add_widget(card)

        Animation(y=orig_y, opacity=1, duration=0.28, t="out_back").start(card)

    # ------------------------------------------------------------------
    # Обратные вызовы игровой логики
    # ------------------------------------------------------------------

    def _on_swipe(self, direction: str):
        """Обработать свайп: передать выбор игровому состоянию."""
        continues = self.game_state.apply_choice(direction)
        self._refresh_stats()
        if continues:
            self._show_card()
        else:
            self._go_to_game_over()

    def _refresh_stats(self):
        """Обновить визуальные полосы статов и метку года."""
        for stat, bar in self._stat_bars.items():
            bar.stat_value = self.game_state.stats[stat]
        self._year_label.text = str(self.game_state.year)

    def _go_to_game_over(self):
        """Передать результат на экран конца игры и перейти туда."""
        go_screen = self.manager.get_screen("gameover")
        go_screen.setup(
            win=self.game_state.win,
            reason=self.game_state.game_over_reason,
            year=self.game_state.year,
            decisions=self.game_state.decisions_count,
        )
        self.manager.current = "gameover"
