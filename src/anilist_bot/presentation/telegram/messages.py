from html import escape

from anilist_bot.domain.anime import AnimeEntry


START_MESSAGE = (
    "🌸 Привіт! Я твій anime watchlist бот.\n\n"
    "Надішли назву аніме текстом, і я додам її у список.\n"
    "Або скинь постер/скрін з назвою в caption — так запис буде з картинкою."
)

HELP_MESSAGE = (
    "✨ Що я вмію:\n\n"
    "📝 Текстове повідомлення — додати аніме без фото\n"
    "🖼 Фото з caption — додати аніме з картинкою\n"
    "📚 /list — показати твій список\n"
    "❔ /help — підказка по командах"
)

EMPTY_LIST_MESSAGE = (
    "📭 Список поки порожній.\n\n"
    "Надішли назву першого аніме, яке вже подивився."
)
MISSING_PHOTO_CAPTION_MESSAGE = (
    "🖼 Фото отримав, але не бачу назви.\n\n"
    "Додай назву аніме в caption до фото, і я збережу запис."
)


def added_message(entry: AnimeEntry) -> str:
    return f"✅ Додав у список:\n<b>{escape(entry.title)}</b>"


def anime_list_message(entries: list[AnimeEntry]) -> str:
    lines = [f"{index}. 🎬 {escape(entry.title)}" for index, entry in enumerate(entries, start=1)]
    return "📚 Твої переглянуті аніме:\n\n" + "\n".join(lines)
