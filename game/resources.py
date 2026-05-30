"""Утилиты для доступа к ресурсам в Green Energy City."""

from __future__ import annotations

import os
import sys


def resource_path(relative_path: str) -> str:
    """Вернуть абсолютный путь к ресурсу для dev и PyInstaller."""
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, relative_path)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    return os.path.join(project_root, relative_path)
