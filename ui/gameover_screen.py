"""Экран конца игры для Green Energy City."""

import os

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from game import i18n
from game.resources import resource_path

# Пути к иконкам результата игры
_WIN_ICON = resource_path(os.path.join('data', 'icons', 'win.png'))
_LOSE_ICON = resource_path(os.path.join('data', 'icons', 'lose.png'))

Builder.load_file(os.path.join(os.path.dirname(__file__), 'gameover_screen.kv'))


class GameOverScreen(Screen):
    """Показывается при завершении игры (победа или поражение)."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Данные результата игры, переданные из GameScreen
        self._win = False
        self._reason = ""
        self._year = 2026
        self._decisions = 0

    def setup(self, *, win, reason, year, decisions):
        """Сохранить результат игры и немедленно обновить UI до начала перехода."""
        self._win = win
        self._reason = reason
        self._year = year
        self._decisions = decisions
        self._update_ui()

    def _update_ui(self):
        """Обновить все надписи экрана по текущему языку и результату игры."""
        self.ids.result_icon.source = _WIN_ICON if self._win else _LOSE_ICON

        if self._win:
            self.ids.title_label.text = i18n.t('win_title')
            self.ids.title_label.color = (0.3, 1.0, 0.3, 1)
        else:
            self.ids.title_label.text = i18n.t('lose_title')
            self.ids.title_label.color = (1.0, 0.35, 0.35, 1)

        self.ids.reason_label.text = self._reason
        self.ids.stats_label.text = (
            i18n.t('year_reached').format(self._year) + "\n" +
            i18n.t('decisions_made').format(self._decisions)
        )

        self.ids.play_again_btn.text = i18n.t('play_again')
        self.ids.menu_btn.text = i18n.t('main_menu')

    def on_enter(self):
        """Обновить все надписи экрана при входе (на случай смены языка)."""
        self._update_ui()

    def on_kv_post(self, _base_widget):
        self.ids.play_again_btn.bind(on_release=self._play_again)
        self.ids.menu_btn.bind(on_release=self._go_menu)

    def _play_again(self, *_):
        """Начать новую игру."""
        self.manager.current = "game"

    def _go_menu(self, *_):
        """Вернуться в главное меню."""
        self.manager.current = "menu"
