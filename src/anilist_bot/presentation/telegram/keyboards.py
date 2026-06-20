from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from anilist_bot.domain.media import Language


BUTTONS: dict[Language, dict[str, str]] = {
    "uk": {
        "add_anime": "➕ Аніме",
        "add_movie": "➕ Фільм",
        "anime_list": "📚 Аніме",
        "movie_list": "🎬 Фільми",
        "language": "🌍 Мова",
        "stats": "📊 Статистика",
        "help": "❔ Допомога",
        "ukrainian": "🇺🇦 Українська",
        "english": "🇬🇧 English",
    },
    "en": {
        "add_anime": "➕ Anime",
        "add_movie": "➕ Movie",
        "anime_list": "📚 Anime",
        "movie_list": "🎬 Movies",
        "language": "🌍 Language",
        "stats": "📊 Stats",
        "help": "❔ Help",
        "ukrainian": "🇺🇦 Українська",
        "english": "🇬🇧 English",
    },
}


ALL_BUTTON_TEXTS = {value for buttons in BUTTONS.values() for value in buttons.values()}


def main_menu(language: Language) -> ReplyKeyboardMarkup:
    buttons = BUTTONS[language]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=buttons["add_anime"]), KeyboardButton(text=buttons["add_movie"])],
            [KeyboardButton(text=buttons["anime_list"]), KeyboardButton(text=buttons["movie_list"])],
            [KeyboardButton(text=buttons["language"]), KeyboardButton(text=buttons["stats"])],
            [KeyboardButton(text=buttons["help"])],
        ],
        resize_keyboard=True,
        input_field_placeholder=_placeholder(language),
    )


def language_menu(language: Language) -> ReplyKeyboardMarkup:
    buttons = BUTTONS[language]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=buttons["ukrainian"])],
            [KeyboardButton(text=buttons["english"])],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def _placeholder(language: Language) -> str:
    if language == "uk":
        return "Назва, фото або дія з меню"
    return "Title, photo, or menu action"
