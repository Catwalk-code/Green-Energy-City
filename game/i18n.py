"""Модуль интернационализации для Green Energy City.

Поддерживает два языка:
  'en' — английский (по умолчанию)
  'ru' — русский
"""

# Текущий активный язык игры (глобальная переменная модуля)
_lang: str = 'en'


def get_lang() -> str:
    """Вернуть код текущего языка ('en' или 'ru')."""
    return _lang


def set_lang(lang: str) -> None:
    """Установить активный язык игры.

    Args:
        lang: Код языка — 'en' (английский) или 'ru' (русский).
              Любое другое значение игнорируется.
    """
    global _lang
    if lang in ('en', 'ru'):
        _lang = lang


def t(key: str) -> str:
    """Вернуть переведённую строку по ключу для текущего языка.

    Если ключ не найден — возвращает сам ключ (помогает при отладке).
    """
    return _STRINGS.get(_lang, _STRINGS['en']).get(key, key)


# ──────────────────────────────────────────────────────────────────────
# Словарь всех переводимых строк интерфейса
# Ключи одинаковы для обоих языков; значения — переведённые строки.
# ──────────────────────────────────────────────────────────────────────
_STRINGS: dict[str, dict[str, str]] = {

    # ── Английский язык ───────────────────────────────────────────────
    'en': {
        # Кнопка переключения языка (показывает ДРУГОЙ язык)
        'lang_toggle': 'RU',

        # ── Главное меню ──────────────────────────────────────────────
        'play': 'PLAY',
        'menu_subtitle': (
            "Guide your city to a green future by {year}.\n"
            "Swipe cards left or right to make decisions."
        ),
        'stats_legend': '⚡ Energy   💰 Economy   🌿 Environment   😊 Happiness',

        # ── Статусные полосы на игровом экране ────────────────────────
        'stat_energy':      'Energy',
        'stat_economy':     'Economy',
        'stat_environment': 'Environ.',
        'stat_happiness':   'Happiness',

        # ── Подсказка свайпа на карточке ──────────────────────────────
        'swipe_hint': '← swipe to decide →',

        # ── Экран конца игры ──────────────────────────────────────────
        'win_title':      '🎉 Victory!',
        'lose_title':     '💀 Game Over',
        'year_reached':   'Year reached: {}',
        'decisions_made': 'Decisions made: {}',
        'play_again':     'PLAY AGAIN',
        'main_menu':      'MAIN MENU',

        # ── Причина победы (плейсхолдер {year} будет заменён) ─────────
        'win_reason': (
            "You guided the city to a green future!\n"
            "The year {year} has arrived — mission accomplished."
        ),

        # ── Причины поражения (название_стат_уровень) ─────────────────
        'loss_energy_low':       "Power cuts became permanent.\nThe city went dark forever.",
        'loss_energy_high':      "Grid overload caused a catastrophic cascade failure.",
        'loss_economy_low':      "The city went bankrupt.\nAll public services collapsed.",
        'loss_economy_high':     "Hyperinflation wiped out every citizen's savings.",
        'loss_environment_low':  "Pollution made the city completely uninhabitable.",
        'loss_environment_high': "Nature reclaimed the city and expelled its residents.",
        'loss_happiness_low':    "Citizens revolted and abandoned the city en masse.",
        'loss_happiness_high':   "Complacency took hold — productivity ground to a halt.",
    },

    # ── Русский язык ──────────────────────────────────────────────────
    'ru': {
        # Кнопка переключения языка (показывает ДРУГОЙ язык)
        'lang_toggle': 'EN',

        # ── Главное меню ──────────────────────────────────────────────
        'play': 'ИГРАТЬ',
        'menu_subtitle': (
            "Приведите город к зелёному будущему к {year} году.\n"
            "Смахивайте карточки влево или вправо, чтобы принимать решения."
        ),
        'stats_legend': '⚡ Энергия   💰 Экономика   🌿 Природа   😊 Счастье',

        # ── Статусные полосы на игровом экране ────────────────────────
        'stat_energy':      'Энергия',
        'stat_economy':     'Экономика',
        'stat_environment': 'Природа',
        'stat_happiness':   'Счастье',

        # ── Подсказка свайпа на карточке ──────────────────────────────
        'swipe_hint': '← смахни для выбора →',

        # ── Экран конца игры ──────────────────────────────────────────
        'win_title':      '🎉 Победа!',
        'lose_title':     '💀 Игра окончена',
        'year_reached':   'Достигнутый год: {}',
        'decisions_made': 'Принято решений: {}',
        'play_again':     'ИГРАТЬ СНОВА',
        'main_menu':      'ГЛАВНОЕ МЕНЮ',

        # ── Причина победы (плейсхолдер {year} будет заменён) ─────────
        'win_reason': (
            "Вы привели город к зелёному будущему!\n"
            "Наступил {year} год — миссия выполнена."
        ),

        # ── Причины поражения ─────────────────────────────────────────
        'loss_energy_low':       "Отключения электроэнергии стали постоянными.\nГород погрузился во тьму навсегда.",
        'loss_energy_high':      "Перегрузка сети вызвала катастрофический каскадный сбой.",
        'loss_economy_low':      "Город обанкротился.\nВсе государственные службы прекратили работу.",
        'loss_economy_high':     "Гиперинфляция уничтожила сбережения каждого жителя.",
        'loss_environment_low':  "Загрязнение сделало город полностью непригодным для жизни.",
        'loss_environment_high': "Природа отвоевала город и вытеснила его жителей.",
        'loss_happiness_low':    "Жители подняли восстание и массово покинули город.",
        'loss_happiness_high':   "Самодовольство распространилось — производительность упала до нуля.",
    },
}
