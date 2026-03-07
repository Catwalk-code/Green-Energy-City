"""Тесты модуля интернационализации (i18n) и поддержки русского языка."""

import sys
import os
import random
import unittest

# Добавить корень репозитория в путь поиска модулей
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from game import i18n
from game.state import GameState
from game.cards_data import CARDS as CARDS_EN, INTRO_CARD as INTRO_EN
from game.cards_data_ru import CARDS as CARDS_RU, INTRO_CARD as INTRO_RU


class TestI18nModule(unittest.TestCase):
    """Тесты базовой функциональности модуля i18n."""

    def setUp(self):
        # Перед каждым тестом устанавливаем английский для изоляции тестов
        i18n.set_lang('en')

    def tearDown(self):
        # Восстанавливаем русский язык (по умолчанию) после каждого теста
        i18n.set_lang('ru')

    def test_default_language_is_russian(self):
        """По умолчанию язык модуля i18n должен быть русским."""
        import importlib
        # Перезагружаем модуль, чтобы увидеть его исходное значение переменной
        importlib.reload(i18n)
        try:
            self.assertEqual(i18n._lang, 'ru')
        finally:
            # Восстановить английский для остальных тестов в этом классе
            i18n.set_lang('en')

    def test_set_lang_to_russian(self):
        """set_lang('ru') должен устанавливать русский язык."""
        i18n.set_lang('ru')
        self.assertEqual(i18n.get_lang(), 'ru')

    def test_set_lang_invalid_ignored(self):
        """Неизвестный код языка должен игнорироваться."""
        i18n.set_lang('fr')
        self.assertEqual(i18n.get_lang(), 'en')

    def test_t_returns_english_string(self):
        """При английском языке t() должен возвращать английский текст."""
        self.assertEqual(i18n.t('play'), 'PLAY')

    def test_t_returns_russian_string(self):
        """При русском языке t() должен возвращать русский текст."""
        i18n.set_lang('ru')
        self.assertEqual(i18n.t('play'), 'ИГРАТЬ')

    def test_t_unknown_key_returns_key(self):
        """Если ключ не найден, t() должен вернуть сам ключ."""
        self.assertEqual(i18n.t('nonexistent_key'), 'nonexistent_key')

    def test_lang_toggle_key_en(self):
        """На английском 'lang_toggle' должен показывать 'RU'."""
        self.assertEqual(i18n.t('lang_toggle'), 'RU')

    def test_lang_toggle_key_ru(self):
        """На русском 'lang_toggle' должен показывать 'EN'."""
        i18n.set_lang('ru')
        self.assertEqual(i18n.t('lang_toggle'), 'EN')

    def test_all_required_keys_exist_in_english(self):
        """Все ключи, необходимые игре, должны присутствовать в английском словаре."""
        required_keys = [
            'lang_toggle', 'play', 'menu_subtitle', 'stats_legend',
            'difficulty_label', 'difficulty_easy', 'difficulty_medium', 'difficulty_hard',
            'stat_energy', 'stat_economy', 'stat_environment', 'stat_happiness',
            'swipe_hint',
            'win_title', 'lose_title', 'year_reached', 'decisions_made',
            'play_again', 'main_menu', 'win_reason',
            'loss_energy_low', 'loss_energy_high',
            'loss_economy_low', 'loss_economy_high',
            'loss_environment_low', 'loss_environment_high',
            'loss_happiness_low', 'loss_happiness_high',
        ]
        for key in required_keys:
            with self.subTest(key=key):
                result = i18n.t(key)
                # Ключ должен быть найден (т.е. результат ≠ самому ключу)
                self.assertNotEqual(result, key, f"Ключ '{key}' не найден в английском словаре")

    def test_all_required_keys_exist_in_russian(self):
        """Все ключи, необходимые игре, должны присутствовать в русском словаре."""
        i18n.set_lang('ru')
        required_keys = [
            'lang_toggle', 'play', 'menu_subtitle', 'stats_legend',
            'difficulty_label', 'difficulty_easy', 'difficulty_medium', 'difficulty_hard',
            'stat_energy', 'stat_economy', 'stat_environment', 'stat_happiness',
            'swipe_hint',
            'win_title', 'lose_title', 'year_reached', 'decisions_made',
            'play_again', 'main_menu', 'win_reason',
            'loss_energy_low', 'loss_energy_high',
            'loss_economy_low', 'loss_economy_high',
            'loss_environment_low', 'loss_environment_high',
            'loss_happiness_low', 'loss_happiness_high',
        ]
        for key in required_keys:
            with self.subTest(key=key):
                result = i18n.t(key)
                self.assertNotEqual(result, key, f"Ключ '{key}' не найден в русском словаре")

    def test_win_reason_contains_year_placeholder(self):
        """Строка win_reason должна содержать плейсхолдер {year}."""
        for lang in ('en', 'ru'):
            i18n.set_lang(lang)
            with self.subTest(lang=lang):
                self.assertIn('{year}', i18n.t('win_reason'))

    def test_menu_subtitle_does_not_contain_year(self):
        """Подзаголовок меню не должен содержать {year} — год показывают кнопки сложности."""
        for lang in ('en', 'ru'):
            i18n.set_lang(lang)
            with self.subTest(lang=lang):
                self.assertNotIn('{year}', i18n.t('menu_subtitle'))

    def test_difficulty_keys_exist(self):
        """Ключи сложности должны существовать в обоих языках."""
        keys = ['difficulty_label', 'difficulty_easy', 'difficulty_medium', 'difficulty_hard']
        for lang in ('en', 'ru'):
            i18n.set_lang(lang)
            for key in keys:
                with self.subTest(lang=lang, key=key):
                    result = i18n.t(key)
                    self.assertNotEqual(result, key, f"Ключ '{key}' не найден в словаре '{lang}'")

    def test_swipe_hint_has_no_arrow_characters(self):
        """Текст подсказки свайпа не должен содержать стрелки — они теперь картинки."""
        for lang in ('en', 'ru'):
            i18n.set_lang(lang)
            with self.subTest(lang=lang):
                hint = i18n.t('swipe_hint')
                self.assertNotIn('←', hint, f"Стрелка ← найдена в swipe_hint ({lang})")
                self.assertNotIn('→', hint, f"Стрелка → найдена в swipe_hint ({lang})")

    def test_russian_strings_are_different_from_english(self):
        """Русские переводы должны отличаться от английских."""
        keys_to_check = ['play', 'swipe_hint', 'win_title', 'lose_title', 'play_again', 'main_menu']
        for key in keys_to_check:
            i18n.set_lang('en')
            en_val = i18n.t(key)
            i18n.set_lang('ru')
            ru_val = i18n.t(key)
            with self.subTest(key=key):
                self.assertNotEqual(en_val, ru_val, f"Ключ '{key}': русский перевод совпадает с английским")


class TestRussianCardsData(unittest.TestCase):
    """Тесты данных русских карточек."""

    def test_intro_card_exists(self):
        """Вступительная русская карточка должна существовать."""
        self.assertIsNotNone(INTRO_RU)

    def test_intro_card_has_same_id_as_english(self):
        """Идентификатор вступительной карточки должен совпадать с английской."""
        self.assertEqual(INTRO_RU.card_id, INTRO_EN.card_id)

    def test_russian_deck_same_length_as_english(self):
        """Количество карточек в русской колоде должно совпадать с английской."""
        self.assertEqual(len(CARDS_RU), len(CARDS_EN))

    def test_russian_cards_same_ids_as_english(self):
        """Идентификаторы всех русских карточек должны совпадать с английскими."""
        en_ids = {c.card_id for c in CARDS_EN}
        ru_ids = {c.card_id for c in CARDS_RU}
        self.assertEqual(en_ids, ru_ids)

    def test_russian_cards_same_effects_as_english(self):
        """Эффекты карточек должны быть одинаковы в обоих языках."""
        en_by_id = {c.card_id: c for c in CARDS_EN}
        ru_by_id = {c.card_id: c for c in CARDS_RU}
        for cid in en_by_id:
            en_card = en_by_id[cid]
            ru_card = ru_by_id[cid]
            with self.subTest(card_id=cid):
                self.assertEqual(en_card.left_choice.effects,  ru_card.left_choice.effects)
                self.assertEqual(en_card.right_choice.effects, ru_card.right_choice.effects)

    def test_russian_cards_same_conditions_as_english(self):
        """Условия появления карточек должны быть одинаковы в обоих языках."""
        en_by_id = {c.card_id: c for c in CARDS_EN}
        ru_by_id = {c.card_id: c for c in CARDS_RU}
        for cid in en_by_id:
            with self.subTest(card_id=cid):
                self.assertEqual(en_by_id[cid].conditions, ru_by_id[cid].conditions)

    def test_russian_card_texts_not_empty(self):
        """Тексты русских карточек не должны быть пустыми."""
        for card in CARDS_RU:
            with self.subTest(card_id=card.card_id):
                self.assertTrue(card.text.strip())
                self.assertTrue(card.left_choice.text.strip())
                self.assertTrue(card.right_choice.text.strip())

    def test_all_ru_card_effects_valid_stats(self):
        """Все эффекты русских карточек должны ссылаться на известные статы."""
        valid_stats = set(GameState.STATS)
        for card in CARDS_RU:
            for stat in card.left_choice.effects:
                self.assertIn(stat, valid_stats, f"Карточка {card.card_id}: неизвестный стат '{stat}'")
            for stat in card.right_choice.effects:
                self.assertIn(stat, valid_stats, f"Карточка {card.card_id}: неизвестный стат '{stat}'")

    def test_ru_intro_card_does_not_mention_2040(self):
        """Вступительная карточка не должна упоминать 2040 — год теперь настраивается."""
        self.assertNotIn('2040', INTRO_RU.text)

    def test_en_intro_card_does_not_mention_2040(self):
        """Английская вступительная карточка не должна упоминать 2040."""
        self.assertNotIn('2040', INTRO_EN.text)

    def test_ru_cards_no_complex_subsidize_term(self):
        """Слово 'субсидировать' (сложное) должно быть заменено в карточках."""
        for card in [INTRO_RU] + list(CARDS_RU):
            with self.subTest(card_id=card.card_id):
                self.assertNotIn('субсидировать', card.text.lower())
                self.assertNotIn('субсидировать', card.left_choice.text.lower())
                self.assertNotIn('субсидировать', card.right_choice.text.lower())


class TestGameStateWithLanguage(unittest.TestCase):
    """Тесты интеграции GameState с переключением языка."""

    def setUp(self):
        random.seed(42)
        i18n.set_lang('en')
        GameState.set_difficulty(2040)  # сбросить сложность до «сложного»

    def tearDown(self):
        # Восстановить язык и сложность после каждого теста
        i18n.set_lang('ru')
        GameState.set_difficulty(2040)

    def test_reset_loads_english_cards_by_default(self):
        """При языке 'en' reset() должен загружать английские карточки."""
        gs = GameState()
        # Вступительная карточка должна иметь английский текст
        self.assertEqual(gs.current_card.card_id, INTRO_EN.card_id)
        self.assertEqual(gs.current_card.character, INTRO_EN.character)

    def test_reset_loads_russian_cards_when_ru(self):
        """При языке 'ru' reset() должен загружать русские карточки."""
        i18n.set_lang('ru')
        gs = GameState()
        self.assertEqual(gs.current_card.card_id, INTRO_RU.card_id)
        # Персонаж вступительной карточки должен быть на русском
        self.assertEqual(gs.current_card.character, INTRO_RU.character)

    def test_win_reason_is_in_english(self):
        """При языке 'en' текст победы должен содержать английский."""
        gs = GameState()
        gs.year = 2039
        gs.decisions_count = 3
        gs.apply_choice('right')
        self.assertIn('green future', gs.game_over_reason.lower())

    def test_win_reason_is_in_russian(self):
        """При языке 'ru' текст победы должен содержать русский."""
        i18n.set_lang('ru')
        gs = GameState()
        gs.year = 2039
        gs.decisions_count = 3
        gs.apply_choice('right')
        # Русский текст победы содержит слово 'будущему' или 'миссия'
        self.assertTrue(
            'будущему' in gs.game_over_reason or 'миссия' in gs.game_over_reason,
            f"Ожидался русский текст победы, получено: {gs.game_over_reason!r}"
        )

    def test_loss_reason_in_english(self):
        """При языке 'en' текст поражения должен быть на английском."""
        from game.card import Card, Choice
        gs = GameState()
        gs.stats['energy'] = 5
        gs.current_card = Card(
            card_id=9000, character="T", text="T",
            left_choice=Choice("Drop", {"energy": -10}),
            right_choice=Choice("Keep", {}),
        )
        gs.apply_choice('left')
        self.assertIn('Power cuts', gs.game_over_reason)

    def test_loss_reason_in_russian(self):
        """При языке 'ru' текст поражения должен быть на русском."""
        from game.card import Card, Choice
        i18n.set_lang('ru')
        gs = GameState()
        gs.stats['energy'] = 5
        gs.current_card = Card(
            card_id=9001, character="T", text="T",
            left_choice=Choice("Drop", {"energy": -10}),
            right_choice=Choice("Keep", {}),
        )
        gs.apply_choice('left')
        self.assertIn('Отключения', gs.game_over_reason)

    def test_switching_language_affects_new_game(self):
        """Переключение языка между играми должно менять колоду карточек."""
        i18n.set_lang('en')
        gs_en = GameState()
        en_intro_char = gs_en.current_card.character

        i18n.set_lang('ru')
        gs_ru = GameState()
        ru_intro_char = gs_ru.current_card.character

        self.assertNotEqual(en_intro_char, ru_intro_char)


if __name__ == "__main__":
    unittest.main()
