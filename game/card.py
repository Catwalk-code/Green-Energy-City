"""Модель данных карточки для Green Energy City."""


class Choice:
    """Представляет один вариант выбора при свайпе карточки."""

    def __init__(self, text, effects):
        """
        Args:
            text: Короткий текст, отображаемый на метке варианта.
            effects: Dict[str, int] — название стата → изменение значения
                     (положительное = рост, отрицательное = снижение).
        """
        self.text = text
        self.effects = effects


class Card:
    """Одна карточка решения, представляемая игроку."""

    def __init__(self, card_id, character, text, left_choice, right_choice,
                 conditions=None):
        """
        Args:
            card_id: Уникальный идентификатор карточки.
            character: Имя персонажа, предлагающего решение.
            text: Текст ситуации / вопроса.
            left_choice: Вариант при свайпе влево (отказ / нет).
            right_choice: Вариант при свайпе вправо (принять / да).
            conditions: Опциональный словарь {название_стата: (min, max)}.
                        Карточка появляется только при выполнении всех условий.
        """
        self.card_id = card_id
        self.character = character
        self.text = text
        self.left_choice = left_choice
        self.right_choice = right_choice
        self.conditions = conditions or {}

