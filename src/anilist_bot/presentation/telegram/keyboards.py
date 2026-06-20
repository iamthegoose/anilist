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
        "edit_last": "✏️ Останній запис",
        "help": "❔ Допомога",
        "edit_title": "✏️ Назва",
        "edit_note": "📝 Примітка",
        "edit_tags": "🏷 Теги",
        "clear_note": "🧹 Очистити примітку",
        "status_planned": "🕒 Хочу",
        "status_watching": "👀 Дивлюсь",
        "status_watched": "✅ Переглянуто",
        "status_dropped": "⏸ Закинуто",
        "back": "⬅️ Назад",
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
        "edit_last": "✏️ Last entry",
        "help": "❔ Help",
        "edit_title": "✏️ Title",
        "edit_note": "📝 Note",
        "edit_tags": "🏷 Tags",
        "clear_note": "🧹 Clear note",
        "status_planned": "🕒 Want",
        "status_watching": "👀 Watching",
        "status_watched": "✅ Watched",
        "status_dropped": "⏸ Dropped",
        "back": "⬅️ Back",
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
            [KeyboardButton(text=buttons["edit_last"])],
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


def edit_menu(language: Language) -> ReplyKeyboardMarkup:
    buttons = BUTTONS[language]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=buttons["status_watched"]), KeyboardButton(text=buttons["status_planned"])],
            [KeyboardButton(text=buttons["status_watching"]), KeyboardButton(text=buttons["status_dropped"])],
            [KeyboardButton(text=buttons["edit_title"]), KeyboardButton(text=buttons["edit_tags"])],
            [KeyboardButton(text=buttons["edit_note"]), KeyboardButton(text=buttons["clear_note"])],
            [KeyboardButton(text=buttons["back"])],
        ],
        resize_keyboard=True,
        input_field_placeholder=_edit_placeholder(language),
    )


def _placeholder(language: Language) -> str:
    if language == "uk":
        return "Назва, фото або дія з меню"
    return "Title, photo, or menu action"


def _edit_placeholder(language: Language) -> str:
    if language == "uk":
        return "Редагування останнього запису"
    return "Edit last entry"
