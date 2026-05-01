"""Управление игровым состоянием для Green Energy City."""

import os
import random

from game.card import Card
from game.cards_data_ru import CARDS as _CARDS_RU, INTRO_CARD as _INTRO_RU
from game import i18n


class GameState:
    """Хранит всё изменяемое состояние игры: статы, год, текущую карточку и т.д."""

    # Названия четырёх игровых характеристик
    STATS = ("energy", "economy", "environment", "happiness")

    # Пути к иконкам характеристик (PNG-файлы вместо эмодзи)
    STAT_ICONS = {
        "energy":      os.path.join('data', 'icons', 'energy.png'),
        "economy":     os.path.join('data', 'icons', 'economy.png'),
        "environment": os.path.join('data', 'icons', 'environment.png'),
        "happiness":   os.path.join('data', 'icons', 'happiness.png'),
    }

    # Максимальный год победы (режим «Сложно» / обратная совместимость)
    WIN_YEAR = 2040

    # Уровни сложности: год победы для каждого уровня
    DIFFICULTY_YEARS = {
        'easy':   2030,
        'medium': 2035,
        'hard':   2040,
    }

    # Выбранный год победы (изменяется методом set_difficulty)
    _difficulty_year = 2040

    @classmethod
    def set_difficulty(cls, year):
        """Установить год победы в соответствии с выбранной сложностью.

        Args:
            year: Целевой год победы - 2030 (лёгкий), 2035 (средний) или 2040 (сложный).
        """
        if year in (2030, 2035, 2040):
            cls._difficulty_year = year

    def __init__(self):
        self.reset()

    def reset(self):
        """Сбросить игровое состояние до начального."""
        # Все статы начинаются с нейтрального значения 50
        self.stats = {stat: 50 for stat in self.STATS}
        # Игра начинается с 2026 года
        self.year = 2026
        # Целевой год победы для текущей партии берётся из выбранной сложности
        self.win_year = GameState._difficulty_year
        self.decisions_count = 0
        self.game_over = False
        self.win = False
        self.game_over_reason = ""

        # Выбрать колоду русских карточек
        cards = _CARDS_RU
        intro  = _INTRO_RU

        self._deck = list(cards)
        random.shuffle(self._deck)
        self._played_ids = set()

        # Первая карточка - всегда вступительная
        self.current_card = intro
        # Запомнить текущую колоду для перемешивания при исчерпании
        self._cards_pool = cards

    
    # Управление колодой карточек
    
    def _check_conditions(self, card):
        """Проверить, удовлетворяют ли текущие статы условиям карточки."""
        for stat, (min_val, max_val) in card.conditions.items():
            if not (min_val <= self.stats.get(stat, 50) <= max_val):
                return False
        return True

    def _get_next_card(self):
        """Вернуть следующую карточку, удовлетворяющую текущим условиям."""
        # Первый проход: приоритет условным карточкам, подходящим по стату
        for i, card in enumerate(self._deck):
            if card.conditions and self._check_conditions(card):
                self._deck.pop(i)
                return card

        # Второй проход: любая безусловная карточка, ещё не сыгранная
        for i, card in enumerate(self._deck):
            if not card.conditions and card.card_id not in self._played_ids:
                self._deck.pop(i)
                return card

        # Колода исчерпана - перемешать только безусловные карточки
        self._deck = [c for c in self._cards_pool if not c.conditions]
        random.shuffle(self._deck)
        self._played_ids.clear()
        return self._deck.pop(0)

    
    # Игровая логика
    
    def apply_choice(self, direction):
        """Применить выбор игрока и обновить игровое состояние.

        Args:
            direction: ``'left'`` (влево) или ``'right'`` (вправо).

        Returns:
            ``True`` - игра продолжается; ``False`` - игра завершена.
        """
        card = self.current_card
        # Определить выбранный вариант в зависимости от направления свайпа
        choice = card.right_choice if direction == "right" else card.left_choice

        # Применить эффекты к статам с ограничением в диапазоне [0, 100]
        for stat, delta in choice.effects.items():
            self.stats[stat] = max(0, min(100, self.stats[stat] + delta))

        self._played_ids.add(card.card_id)
        self.decisions_count += 1

        # Каждые 4 решения - переходим к следующему году
        if self.decisions_count % 4 == 0:
            self.year += 1

        # Проверить условие победы (год партии достиг выбранного целевого года)
        if self.year >= self.win_year:
            self.win = True
            self.game_over = True
            # Текст победы берётся из модуля переводов
            self.game_over_reason = i18n.t('win_reason').format(year=self.win_year)
            return False

        # Проверить условия поражения (стат достиг 0 или 100)
        for stat, value in self.stats.items():
            if value <= 0:
                self.game_over = True
                self.game_over_reason = i18n.t(f'loss_{stat}_low')
                return False
            if value >= 100:
                self.game_over = True
                self.game_over_reason = i18n.t(f'loss_{stat}_high')
                return False

        self.current_card = self._get_next_card()
        return True

    def restore(self, data):
        """Восстановить состояние игры из словаря сохранения.

        Вызывает :meth:`reset` для инициализации колоды, затем перезаписывает
        статы, год и счётчик решений из сохранения.  В качестве первой карточки
        берётся следующая из колоды (вступительная карточка пропускается).

        Args:
            data: Словарь с ключами ``stats``, ``year``,
                  ``decisions_count``, ``win_year``.
        """
        self.reset()
        saved_stats = data.get("stats", {})
        for stat in self.STATS:
            if stat in saved_stats:
                self.stats[stat] = max(0, min(100, int(saved_stats[stat])))
        self.year = int(data.get("year", 2026))
        self.decisions_count = int(data.get("decisions_count", 0))
        self.win_year = int(data.get("win_year", GameState._difficulty_year))
        # Обновить глобальный уровень сложности, чтобы он соответствовал сохранению
        GameState._difficulty_year = self.win_year
        # Пропустить вступительную карточку - перейти к первой карточке колоды
        self.current_card = self._get_next_card()
