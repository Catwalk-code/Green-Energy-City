"""Утилиты для доступа к ресурсам в Green Energy City."""

from __future__ import annotations

import os
import sys


def resource_path(relative_path: str) -> str:
    """Вернуть абсолютный путь к ресурсу для dev и PyInstaller."""
    base_dir = getattr(sys, "_MEIPASS", None)
    if base_dir:
        return os.path.join(base_dir, relative_path)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    return os.path.join(project_root, relative_path)
