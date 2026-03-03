"""Unit tests for game logic (no Kivy UI dependency)."""

import sys
import os

# Add repo root to path so imports work without installing the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from unittest.mock import patch
import random

from game.card import Card, Choice
from game.state import GameState
from game.cards_data import CARDS, INTRO_CARD


class TestChoice(unittest.TestCase):
    def test_attributes(self):
        c = Choice("Accept", {"energy": 10, "economy": -5})
        self.assertEqual(c.text, "Accept")
        self.assertEqual(c.effects["energy"], 10)
        self.assertEqual(c.effects["economy"], -5)


class TestCard(unittest.TestCase):
    def _make_card(self):
        return Card(
            card_id=99,
            character="Tester",
            text="Test question.",
            left_choice=Choice("No", {"energy": -5}),
            right_choice=Choice("Yes", {"energy": 5}),
        )

    def test_attributes(self):
        card = self._make_card()
        self.assertEqual(card.card_id, 99)
        self.assertEqual(card.character, "Tester")
        self.assertEqual(card.conditions, {})

    def test_conditions(self):
        card = Card(
            card_id=100,
            character="Tester",
            text="Conditional card.",
            left_choice=Choice("No", {}),
            right_choice=Choice("Yes", {}),
            conditions={"energy": (0, 30)},
        )
        self.assertIn("energy", card.conditions)


class TestGameState(unittest.TestCase):
    def setUp(self):
        # Use a fixed seed for reproducibility
        random.seed(42)
        self.gs = GameState()

    def tearDown(self):
        # Восстановить сложность по умолчанию после каждого теста
        GameState.set_difficulty(2040)

    # ------------------------------------------------------------------ reset
    def test_initial_stats(self):
        for stat in GameState.STATS:
            self.assertEqual(self.gs.stats[stat], 50)

    def test_initial_year(self):
        self.assertEqual(self.gs.year, 2026)

    def test_initial_not_game_over(self):
        self.assertFalse(self.gs.game_over)
        self.assertFalse(self.gs.win)

    def test_first_card_is_intro(self):
        self.assertEqual(self.gs.current_card.card_id, INTRO_CARD.card_id)

    # ------------------------------------------------------------------ apply_choice
    def test_apply_right_choice_changes_stats(self):
        card = self.gs.current_card
        effects = card.right_choice.effects
        before = dict(self.gs.stats)
        self.gs.apply_choice("right")
        for stat, delta in effects.items():
            self.assertEqual(self.gs.stats[stat], max(0, min(100, before[stat] + delta)))

    def test_apply_left_choice_changes_stats(self):
        card = self.gs.current_card
        effects = card.left_choice.effects
        before = dict(self.gs.stats)
        self.gs.apply_choice("left")
        for stat, delta in effects.items():
            self.assertEqual(self.gs.stats[stat], max(0, min(100, before[stat] + delta)))

    def test_decisions_count_increments(self):
        self.gs.apply_choice("right")
        self.assertEqual(self.gs.decisions_count, 1)

    def test_year_advances_every_4_decisions(self):
        for _ in range(4):
            self.gs.apply_choice("right")
        self.assertEqual(self.gs.year, 2027)

    def test_year_does_not_advance_before_4_decisions(self):
        for _ in range(3):
            self.gs.apply_choice("right")
        self.assertEqual(self.gs.year, 2026)

    def test_stat_clamped_at_zero(self):
        self.gs.stats["energy"] = 5
        # Force energy to drop below 0 via a choice with large negative effect
        self.gs.current_card = Card(
            card_id=999,
            character="Test",
            text="Test",
            left_choice=Choice("Drop", {"energy": -20}),
            right_choice=Choice("Keep", {}),
        )
        self.gs.apply_choice("left")
        self.assertEqual(self.gs.stats["energy"], 0)

    def test_stat_clamped_at_100(self):
        self.gs.stats["energy"] = 95
        self.gs.current_card = Card(
            card_id=998,
            character="Test",
            text="Test",
            left_choice=Choice("Keep", {}),
            right_choice=Choice("Boost", {"energy": 20}),
        )
        self.gs.apply_choice("right")
        self.assertEqual(self.gs.stats["energy"], 100)

    # ------------------------------------------------------------------ game over
    def test_game_over_when_stat_hits_zero(self):
        self.gs.stats["energy"] = 5
        self.gs.current_card = Card(
            card_id=997,
            character="Test",
            text="Test",
            left_choice=Choice("Drop", {"energy": -10}),
            right_choice=Choice("Keep", {}),
        )
        result = self.gs.apply_choice("left")
        self.assertFalse(result)
        self.assertTrue(self.gs.game_over)
        self.assertFalse(self.gs.win)

    def test_game_over_when_stat_hits_100(self):
        self.gs.stats["happiness"] = 95
        self.gs.current_card = Card(
            card_id=996,
            character="Test",
            text="Test",
            left_choice=Choice("Keep", {}),
            right_choice=Choice("Boost", {"happiness": 10}),
        )
        result = self.gs.apply_choice("right")
        self.assertFalse(result)
        self.assertTrue(self.gs.game_over)

    def test_win_when_year_reaches_2040(self):
        # Fast-forward year to 2039 and trigger the last increment
        self.gs.year = 2039
        self.gs.decisions_count = 3  # one more decision triggers year advance
        result = self.gs.apply_choice("right")
        self.assertFalse(result)
        self.assertTrue(self.gs.win)
        self.assertTrue(self.gs.game_over)

    def test_game_continues_normally(self):
        result = self.gs.apply_choice("right")
        self.assertTrue(result)
        self.assertFalse(self.gs.game_over)

    # ------------------------------------------------------------------ card cycling
    def test_next_card_changes_after_choice(self):
        first_id = self.gs.current_card.card_id
        self.gs.apply_choice("right")
        second_id = self.gs.current_card.card_id
        self.assertNotEqual(first_id, second_id)

    def test_cards_data_not_empty(self):
        self.assertGreater(len(CARDS), 0)

    def test_all_card_effects_valid_stats(self):
        valid_stats = set(GameState.STATS)
        for card in CARDS:
            for stat in card.left_choice.effects:
                self.assertIn(stat, valid_stats, f"Card {card.card_id} left_choice: unknown stat '{stat}'")
            for stat in card.right_choice.effects:
                self.assertIn(stat, valid_stats, f"Card {card.card_id} right_choice: unknown stat '{stat}'")

    def test_reset_restores_initial_state(self):
        for _ in range(5):
            self.gs.apply_choice("right")
        self.gs.reset()
        self.assertEqual(self.gs.decisions_count, 0)
        self.assertEqual(self.gs.year, 2026)
        for stat in GameState.STATS:
            self.assertEqual(self.gs.stats[stat], 50)

    # ------------------------------------------------------------------ difficulty
    def test_default_difficulty_is_hard(self):
        """По умолчанию уровень сложности — сложный (2040)."""
        self.assertEqual(self.gs.win_year, 2040)

    def test_set_difficulty_easy_changes_win_year(self):
        """Лёгкий уровень устанавливает год победы 2030."""
        GameState.set_difficulty(2030)
        self.gs.reset()
        self.assertEqual(self.gs.win_year, 2030)

    def test_set_difficulty_medium_changes_win_year(self):
        """Средний уровень устанавливает год победы 2035."""
        GameState.set_difficulty(2035)
        self.gs.reset()
        self.assertEqual(self.gs.win_year, 2035)

    def test_win_easy_when_year_reaches_2030(self):
        """При лёгком уровне победа наступает в 2030 году."""
        GameState.set_difficulty(2030)
        self.gs.reset()
        self.gs.year = 2029
        self.gs.decisions_count = 3
        result = self.gs.apply_choice("right")
        self.assertFalse(result)
        self.assertTrue(self.gs.win)

    def test_win_medium_when_year_reaches_2035(self):
        """При среднем уровне победа наступает в 2035 году."""
        GameState.set_difficulty(2035)
        self.gs.reset()
        self.gs.year = 2034
        self.gs.decisions_count = 3
        result = self.gs.apply_choice("right")
        self.assertFalse(result)
        self.assertTrue(self.gs.win)

    def test_invalid_difficulty_ignored(self):
        """Неверный год сложности должен игнорироваться."""
        GameState.set_difficulty(2025)   # не в списке допустимых
        self.gs.reset()
        self.assertEqual(self.gs.win_year, 2040)  # должен остаться 2040


if __name__ == "__main__":
    unittest.main()
