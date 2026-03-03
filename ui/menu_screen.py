"""Main menu screen for Green Energy City."""

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.lang import Builder

from game.state import GameState

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
    """Startup screen with game title and play button."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        root = FloatLayout()

        col = BoxLayout(
            orientation="vertical",
            size_hint=(0.8, None),
            height=dp(380),
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            spacing=dp(20),
            padding=(dp(20), dp(10)),
        )

        # City icon / emoji splash
        col.add_widget(Label(
            text="🏙️",
            font_size="72sp",
            size_hint_y=None,
            height=dp(100),
            halign="center",
        ))

        # Game title
        col.add_widget(Label(
            text="Green Energy City",
            font_size="28sp",
            bold=True,
            color=(0.4, 1.0, 0.4, 1),
            size_hint_y=None,
            height=dp(50),
            halign="center",
        ))

        # Subtitle
        col.add_widget(Label(
            text=(
                f"Guide your city to a green future by {GameState.WIN_YEAR}.\n"
                "Swipe cards left or right to make decisions."
            ),
            font_size="14sp",
            color=(0.75, 0.95, 0.75, 1),
            size_hint_y=None,
            height=dp(60),
            halign="center",
            text_size=(dp(280), None),
        ))

        # Play button
        play_btn = Button(
            text="PLAY",
            font_size="22sp",
            bold=True,
            size_hint=(None, None),
            size=(dp(200), dp(55)),
            background_color=(0.15, 0.7, 0.15, 1),
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5},
        )
        play_btn.bind(on_release=self._start_game)
        col.add_widget(play_btn)

        # Stats legend
        col.add_widget(Label(
            text="⚡ Energy   💰 Economy   🌿 Environment   😊 Happiness",
            font_size="12sp",
            color=(0.6, 0.85, 0.6, 1),
            size_hint_y=None,
            height=dp(40),
            halign="center",
            text_size=(dp(300), None),
        ))

        root.add_widget(col)
        self.add_widget(root)

    def _start_game(self, *_):
        self.manager.current = "game"
