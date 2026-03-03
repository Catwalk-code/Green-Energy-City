"""Game state management for Green Energy City."""

import random

from game.card import Card
from game.cards_data import CARDS, INTRO_CARD


class GameState:
    """Tracks all mutable game state: stats, year, current card, etc."""

    STATS = ("energy", "economy", "environment", "happiness")
    STAT_ICONS = {
        "energy": "⚡",
        "economy": "💰",
        "environment": "🌿",
        "happiness": "😊",
    }

    WIN_YEAR = 2040  # Survive until this year to win

    LOSS_REASONS = {
        "energy": {
            "low": "Power cuts became permanent.\nThe city went dark forever.",
            "high": "Grid overload caused a catastrophic cascade failure.",
        },
        "economy": {
            "low": "The city went bankrupt.\nAll public services collapsed.",
            "high": "Hyperinflation wiped out every citizen's savings.",
        },
        "environment": {
            "low": "Pollution made the city completely uninhabitable.",
            "high": "Nature reclaimed the city and expelled its residents.",
        },
        "happiness": {
            "low": "Citizens revolted and abandoned the city en masse.",
            "high": "Complacency took hold — productivity ground to a halt.",
        },
    }

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset to the initial game state."""
        self.stats = {stat: 50 for stat in self.STATS}
        self.year = 2024
        self.decisions_count = 0
        self.game_over = False
        self.win = False
        self.game_over_reason = ""

        self._deck = list(CARDS)
        random.shuffle(self._deck)
        self._played_ids = set()

        self.current_card = INTRO_CARD

    # ------------------------------------------------------------------
    # Card management
    # ------------------------------------------------------------------

    def _check_conditions(self, card: Card) -> bool:
        for stat, (min_val, max_val) in card.conditions.items():
            if not (min_val <= self.stats.get(stat, 50) <= max_val):
                return False
        return True

    def _get_next_card(self) -> Card:
        """Return the next card that satisfies current stat conditions."""
        # First pass: find a conditional card that matches the current state
        for i, card in enumerate(self._deck):
            if card.conditions and self._check_conditions(card):
                self._deck.pop(i)
                return card

        # Second pass: any unconditional card not yet played
        for i, card in enumerate(self._deck):
            if not card.conditions and card.card_id not in self._played_ids:
                self._deck.pop(i)
                return card

        # Reshuffle when the deck runs low
        self._deck = [c for c in CARDS if not c.conditions]
        random.shuffle(self._deck)
        self._played_ids.clear()
        return self._deck.pop(0)

    # ------------------------------------------------------------------
    # Game logic
    # ------------------------------------------------------------------

    def apply_choice(self, direction: str) -> bool:
        """
        Apply the player's choice and advance game state.

        Args:
            direction: ``'left'`` or ``'right'``.

        Returns:
            ``True`` if the game continues, ``False`` if it is over.
        """
        card = self.current_card
        choice = card.right_choice if direction == "right" else card.left_choice

        for stat, delta in choice.effects.items():
            self.stats[stat] = max(0, min(100, self.stats[stat] + delta))

        self._played_ids.add(card.card_id)
        self.decisions_count += 1

        # Advance year every 4 decisions
        if self.decisions_count % 4 == 0:
            self.year += 1

        # Check win condition
        if self.year >= self.WIN_YEAR:
            self.win = True
            self.game_over = True
            self.game_over_reason = (
                "You guided the city to a green future!\n"
                "The year 2040 has arrived — mission accomplished."
            )
            return False

        # Check loss conditions (stat at 0 or 100)
        for stat, value in self.stats.items():
            if value <= 0:
                self.game_over = True
                self.game_over_reason = self.LOSS_REASONS[stat]["low"]
                return False
            if value >= 100:
                self.game_over = True
                self.game_over_reason = self.LOSS_REASONS[stat]["high"]
                return False

        self.current_card = self._get_next_card()
        return True
