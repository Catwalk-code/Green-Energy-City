"""Модуль интернационализации для Green Energy City.

Поддерживает два языка:
  'ru' — русский (по умолчанию)
  'en' — английский
"""

# Текущий активный язык игры (глобальная переменная модуля)
# По умолчанию — русский язык
_lang = 'ru'


def get_lang():
    """Вернуть код текущего языка ('en' или 'ru')."""
    return _lang


def set_lang(lang):
    """Установить активный язык игры.

    Args:
        lang: Код языка — 'en' (английский) или 'ru' (русский).
              Любое другое значение игнорируется.
    """
    global _lang
    if lang in ('en', 'ru'):
        _lang = lang


def t(key):
    """Вернуть переведённую строку по ключу для текущего языка.

    Если ключ не найден — возвращает сам ключ (помогает при отладке).
    """
    return _STRINGS.get(_lang, _STRINGS['en']).get(key, key)



# Словарь всех переводимых строк интерфейса
# Ключи одинаковы для обоих языков; значения — переведённые строки.

_STRINGS = {

    #  Английский язык 
    'en': {
        # Кнопка переключения языка (показывает ДРУГОЙ язык)
        'lang_toggle': 'RU',

        #  Главное меню 
        'play': 'PLAY',
        # Подзаголовок без указания года — год показывают кнопки сложности
        'menu_subtitle': (
            "Guide your city to a green future.\n"
            "Swipe cards left or right to make decisions."
        ),
        'stats_legend': 'Energy   Economy   Environment   Happiness',

        #  Выбор сложности 
        'difficulty_label':  'Difficulty:',
        'difficulty_easy':   'Easy\n(2030)',
        'difficulty_medium': 'Medium\n(2035)',
        'difficulty_hard':   'Hard\n(2040)',

        #  Статусные полосы на игровом экране 
        'stat_energy':      'Energy',
        'stat_economy':     'Economy',
        'stat_environment': 'Environ.',
        'stat_happiness':   'Happiness',

        #  Подсказка свайпа на карточке (без стрелок — они теперь картинки) 
        'swipe_hint': 'swipe to decide',

        #  Экран конца игры 
        # Заголовки без эмодзи — вместо них показываются картинки win.png/lose.png
        'win_title':      'Victory!',
        'lose_title':     'Game Over',
        'year_reached':   'Year reached: {}',
        'decisions_made': 'Decisions made: {}',
        'play_again':     'PLAY AGAIN',
        'main_menu':      'MAIN MENU',

        #  Причина победы (плейсхолдер {year} будет заменён) 
        'win_reason': (
            "You guided the city to a green future!\n"
            "The year {year} has arrived — mission accomplished."
        ),

        #  Причины поражения (название_стат_уровень) 
        'loss_energy_low':       "Power cuts became permanent.\nThe city went dark forever.",
        'loss_energy_high':      "The power grid collapsed completely from overload.",
        'loss_economy_low':      "The city went bankrupt.\nAll public services collapsed.",
        'loss_economy_high':     "Prices rose so fast that citizens lost all their savings.",
        'loss_environment_low':  "Pollution made the city completely uninhabitable.",
        'loss_environment_high': "Nature reclaimed the city and expelled its residents.",
        'loss_happiness_low':    "Citizens revolted and abandoned the city en masse.",
        'loss_happiness_high':   "People became too comfortable — work and progress stopped.",

        #  Popup подтверждения выхода (кнопка ☰ / системная кнопка "Назад") 
        'back_popup_title': 'Exit to Menu?',
        'back_popup_body':  'Save your progress and return to the main menu?',
        'continue_game':    'Continue Playing',
        'save_and_exit':    'Save & Exit',

        #  Popup загрузки сохранения при запуске ─
        'save_found_title': 'Save Found',
        'save_found_body':  'A saved game was found.\nContinue where you left off?',
        'new_game':         'New Game',
        'continue_save':    'Continue',
    },

    #  Русский язык 
    'ru': {
        # Кнопка переключения языка (показывает ДРУГОЙ язык)
        'lang_toggle': 'EN',

        #  Главное меню 
        'play': 'ИГРАТЬ',
        # Подзаголовок без указания года — год показывают кнопки сложности
        'menu_subtitle': (
            "Приведите город к зелёному будущему.\n"
            "Смахивайте карточки влево или вправо, чтобы принимать решения."
        ),
        'stats_legend': 'Энергия   Экономика   Природа   Счастье',

        #  Выбор сложности ─
        'difficulty_label':  'Сложность:',
        'difficulty_easy':   'Лёгкий\n(2030)',
        'difficulty_medium': 'Средний\n(2035)',
        'difficulty_hard':   'Сложный\n(2040)',

        #  Статусные полосы на игровом экране 
        'stat_energy':      'Энергия',
        'stat_economy':     'Экономика',
        'stat_environment': 'Природа',
        'stat_happiness':   'Счастье',

        #  Подсказка свайпа на карточке (без стрелок — они теперь картинки) 
        'swipe_hint': 'смахни для выбора',

        #  Экран конца игры 
        # Заголовки без эмодзи — вместо них показываются картинки win.png/lose.png
        'win_title':      'Победа!',
        'lose_title':     'Игра окончена',
        'year_reached':   'Достигнутый год: {}',
        'decisions_made': 'Принято решений: {}',
        'play_again':     'ИГРАТЬ СНОВА',
        'main_menu':      'ГЛАВНОЕ МЕНЮ',

        #  Причина победы (плейсхолдер {year} будет заменён) 
        'win_reason': (
            "Вы привели город к зелёному будущему!\n"
            "Наступил {year} год — миссия выполнена."
        ),

        #  Причины поражения 
        'loss_energy_low':       "Отключения света стали постоянными.\nГород погрузился во тьму навсегда.",
        'loss_energy_high':      "Сеть не выдержала нагрузки и полностью вышла из строя.",
        'loss_economy_low':      "Город остался без денег.\nВсе городские службы прекратили работу.",
        'loss_economy_high':     "Цены выросли так быстро, что жители потеряли все сбережения.",
        'loss_environment_low':  "Загрязнение сделало город полностью непригодным для жизни.",
        'loss_environment_high': "Природа захватила город и вытеснила его жителей.",
        'loss_happiness_low':    "Жители устроили бунт и массово покинули город.",
        'loss_happiness_high':   "Люди стали слишком довольны — работа и прогресс остановились.",

        #  Popup подтверждения выхода (кнопка ☰ / системная кнопка "Назад") 
        'back_popup_title': 'Выйти в меню?',
        'back_popup_body':  'Сохранить прогресс и вернуться в главное меню?',
        'continue_game':    'Продолжить игру',
        'save_and_exit':    'Сохранить и выйти',

        #  Popup загрузки сохранения при запуске 
        'save_found_title': 'Найдено сохранение',
        'save_found_body':  'Найдено сохранение игры.\nПродолжить с того места?',
        'new_game':         'Новая игра',
        'continue_save':    'Продолжить',
    },
}
