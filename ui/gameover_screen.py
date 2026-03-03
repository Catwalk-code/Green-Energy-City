"""Game-over screen for Green Energy City."""

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.lang import Builder

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
    """Shown when the game ends (win or loss)."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._win = False
        self._reason = ""
        self._year = 2024
        self._decisions = 0
        self._title_label = None
        self._reason_label = None
        self._stats_label = None
        self._build_ui()

    def setup(self, *, win: bool, reason: str, year: int, decisions: int):
        self._win = win
        self._reason = reason
        self._year = year
        self._decisions = decisions

    def on_enter(self):
        if self._title_label:
            if self._win:
                self._title_label.text = "🎉 Victory!"
                self._title_label.color = (0.3, 1.0, 0.3, 1)
            else:
                self._title_label.text = "💀 Game Over"
                self._title_label.color = (1.0, 0.35, 0.35, 1)

        if self._reason_label:
            self._reason_label.text = self._reason

        if self._stats_label:
            self._stats_label.text = (
                f"Year reached: {self._year}\n"
                f"Decisions made: {self._decisions}"
            )

    def _build_ui(self):
        root = FloatLayout()

        col = BoxLayout(
            orientation="vertical",
            size_hint=(0.85, None),
            height=dp(420),
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            spacing=dp(18),
            padding=(dp(20), dp(10)),
        )

        # Result title
        self._title_label = Label(
            text="",
            font_size="34sp",
            bold=True,
            size_hint_y=None,
            height=dp(60),
            halign="center",
        )
        col.add_widget(self._title_label)

        # Reason text
        self._reason_label = Label(
            text="",
            font_size="15sp",
            color=(0.85, 0.95, 0.85, 1),
            size_hint_y=None,
            height=dp(90),
            halign="center",
            text_size=(dp(280), None),
        )
        col.add_widget(self._reason_label)

        # Stats
        self._stats_label = Label(
            text="",
            font_size="14sp",
            color=(0.65, 0.85, 0.65, 1),
            size_hint_y=None,
            height=dp(60),
            halign="center",
        )
        col.add_widget(self._stats_label)

        # Play again button
        play_again_btn = Button(
            text="PLAY AGAIN",
            font_size="20sp",
            bold=True,
            size_hint=(None, None),
            size=(dp(200), dp(55)),
            background_color=(0.15, 0.7, 0.15, 1),
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5},
        )
        play_again_btn.bind(on_release=self._play_again)
        col.add_widget(play_again_btn)

        # Menu button
        menu_btn = Button(
            text="MAIN MENU",
            font_size="16sp",
            size_hint=(None, None),
            size=(dp(200), dp(44)),
            background_color=(0.2, 0.4, 0.2, 1),
            color=(0.9, 0.9, 0.9, 1),
            pos_hint={"center_x": 0.5},
        )
        menu_btn.bind(on_release=self._go_menu)
        col.add_widget(menu_btn)

        root.add_widget(col)
        self.add_widget(root)

    def _play_again(self, *_):
        self.manager.current = "game"

    def _go_menu(self, *_):
        self.manager.current = "menu"
