"""Card data model for Green Energy City."""


class Choice:
    """Represents one swipe direction on a decision card."""

    def __init__(self, text, effects):
        """
        Args:
            text: Short description shown as the choice label.
            effects: Dict[str, int] mapping stat names to delta values
                     (positive = increase, negative = decrease).
        """
        self.text = text
        self.effects = effects


class Card:
    """A single decision card presented to the player."""

    def __init__(self, card_id, character, text, left_choice, right_choice,
                 conditions=None):
        """
        Args:
            card_id: Unique identifier.
            character: Name of the NPC presenting the card.
            text: The situation/question text.
            left_choice: Choice for swiping left (decline / no).
            right_choice: Choice for swiping right (accept / yes).
            conditions: Optional dict mapping stat name to (min, max) tuple.
                        Card only appears when all conditions are met.
        """
        self.card_id = card_id
        self.character = character
        self.text = text
        self.left_choice = left_choice
        self.right_choice = right_choice
        self.conditions = conditions or {}
