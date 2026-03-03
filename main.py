"""Entry point for Green Energy City."""

import os

# Use portrait orientation and fixed window size resembling a phone
os.environ.setdefault("KIVY_ORIENTATION", "Portrait")

from kivy.config import Config
Config.set("graphics", "width", "400")
Config.set("graphics", "height", "700")
Config.set("graphics", "resizable", "0")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition

from ui.menu_screen import MenuScreen
from ui.game_screen import GameScreen
from ui.gameover_screen import GameOverScreen


class GreenEnergyCityApp(App):
    """Main Kivy application for Green Energy City."""

    def build(self):
        self.title = "Green Energy City"
        sm = ScreenManager(transition=FadeTransition(duration=0.2))
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(GameOverScreen(name="gameover"))
        return sm


if __name__ == "__main__":
    GreenEnergyCityApp().run()
