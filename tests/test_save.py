"""Модульные тесты сохранения/загрузки игры (без зависимости от Kivy UI)."""

import sys
import os
import json
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# Добавить корень репозитория в путь, чтобы работали импорты без установки пакета
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from game.save import save_game, load_save, has_save, delete_save


def _mock_state(stats=None, year=2028, decisions_count=8, win_year=2040):
    """Вспомогательная функция — создать mock-объект GameState."""
    state = MagicMock()
    state.stats = stats or {
        "energy": 60,
        "economy": 50,
        "environment": 40,
        "happiness": 70,
    }
    state.year = year
    state.decisions_count = decisions_count
    state.win_year = win_year
    return state


class TestSave(unittest.TestCase):
    """Тесты функций сохранения и загрузки."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.save_path = os.path.join(self.tmpdir, "save.json")
        self.patcher = patch("game.save._save_path", return_value=self.save_path)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        if os.path.exists(self.save_path):
            os.remove(self.save_path)
        os.rmdir(self.tmpdir)

    # Тесты has_save
    def test_has_save_false_when_no_file(self):
        self.assertFalse(has_save())

    def test_has_save_true_after_save(self):
        save_game(_mock_state())
        self.assertTrue(has_save())

    # Тесты save_game / load_save
    def test_save_creates_file(self):
        save_game(_mock_state())
        self.assertTrue(os.path.isfile(self.save_path))

    def test_load_returns_none_when_no_file(self):
        self.assertIsNone(load_save())

    def test_load_returns_correct_year(self):
        save_game(_mock_state(year=2031))
        data = load_save()
        self.assertIsNotNone(data)
        self.assertEqual(data["year"], 2031)

    def test_load_returns_correct_decisions_count(self):
        save_game(_mock_state(decisions_count=12))
        data = load_save()
        self.assertEqual(data["decisions_count"], 12)

    def test_load_returns_correct_win_year(self):
        save_game(_mock_state(win_year=2030))
        data = load_save()
        self.assertEqual(data["win_year"], 2030)

    def test_load_returns_correct_stats(self):
        stats = {"energy": 65, "economy": 55, "environment": 45, "happiness": 75}
        save_game(_mock_state(stats=stats))
        data = load_save()
        self.assertEqual(data["stats"]["energy"], 65)
        self.assertEqual(data["stats"]["economy"], 55)
        self.assertEqual(data["stats"]["environment"], 45)
        self.assertEqual(data["stats"]["happiness"], 75)

    def test_save_overwrites_previous(self):
        save_game(_mock_state(year=2026))
        save_game(_mock_state(year=2032))
        data = load_save()
        self.assertEqual(data["year"], 2032)

    # Тесты delete_save
    def test_delete_removes_file(self):
        save_game(_mock_state())
        self.assertTrue(has_save())
        delete_save()
        self.assertFalse(has_save())

    def test_delete_on_missing_file_does_not_raise(self):
        # Должно завершиться без исключений, если файла нет
        try:
            delete_save()
        except Exception as exc:
            self.fail(f"delete_save() raised an exception: {exc}")

    # Тесты повреждённого файла
    def test_load_returns_none_on_corrupt_json(self):
        with open(self.save_path, "w") as f:
            f.write("not valid json {{{")
        self.assertIsNone(load_save())

    def test_load_returns_none_on_empty_file(self):
        with open(self.save_path, "w") as f:
            f.write("")
        self.assertIsNone(load_save())


if __name__ == "__main__":
    unittest.main()
