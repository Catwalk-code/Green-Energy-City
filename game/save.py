"""Сохранение и загрузка игрового прогресса для Green Energy City."""

import json
import os

# Имя файла сохранения
_SAVE_FILE = "save.json"


def _save_path():
    """Вернуть полный путь к файлу сохранения.

    На Android возвращает путь внутри приватной директории приложения
    (``App.user_data_dir``); на десктопе — путь в текущем каталоге.
    """
    try:
        from kivy.app import App  # type: ignore[import]
        app = App.get_running_app()
        if app is not None:
            return os.path.join(app.user_data_dir, _SAVE_FILE)
    except Exception:
        pass
    return _SAVE_FILE


def has_save():
    """Вернуть ``True``, если файл сохранения существует."""
    return os.path.isfile(_save_path())


def save_game(state):
    """Сохранить текущее состояние игры в файл JSON.

    Args:
        state: Экземпляр :class:`game.state.GameState`.
    """
    data = {
        "stats": dict(state.stats),
        "year": state.year,
        "decisions_count": state.decisions_count,
        "win_year": state.win_year,
    }
    path = _save_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def load_save():
    """Загрузить данные из файла сохранения.

    Returns:
        Словарь с сохранёнными данными или None при ошибке / отсутствии файла.
    """
    path = _save_path()
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def delete_save():
    """Удалить файл сохранения, если он существует."""
    path = _save_path()
    try:
        os.remove(path)
    except OSError:
        pass
