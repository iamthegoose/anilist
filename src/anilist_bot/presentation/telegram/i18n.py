from html import escape

from anilist_bot.domain.media import Language, MediaEntry, MediaType, WatchStatus


MESSAGES: dict[Language, dict[str, str]] = {
    "uk": {
        "start": (
            "🌸 <b>Вітаю у твоїй медіатеці.</b>\n\n"
            "Зберігай аніме й фільми, додавай статуси та теги, а я триматиму все охайно."
        ),
        "help": (
            "✨ <b>Як користуватись</b>\n\n"
            "1. Обери <b>➕ Аніме</b> або <b>➕ Фільм</b> у меню.\n"
            "2. Надішли назву текстом або фото з назвою в caption.\n"
            "3. Додай теги через #, наприклад: <code>#переглянуто #романтика</code>.\n\n"
            "Статуси: <code>#переглянуто</code>, <code>#хочу</code>, "
            "<code>#дивлюсь</code>, <code>#закинуто</code>."
        ),
        "language_menu": "🌍 Обери мову інтерфейсу:",
        "language_updated": "✅ Мову змінено.",
        "anime_mode": (
            "➕ <b>Режим додавання: аніме</b>\n\n"
            "Надішли назву або фото з caption. Теги можна додати через #."
        ),
        "movie_mode": (
            "➕ <b>Режим додавання: фільм</b>\n\n"
            "Надішли назву або фото з caption. Теги можна додати через #."
        ),
        "missing_photo_caption": (
            "🖼 Фото отримав, але не бачу назви.\n\n"
            "Додай назву в caption, наприклад: <code>Perfect Blue #переглянуто #психологія</code>."
        ),
        "empty_anime": "📭 У списку аніме поки порожньо.",
        "empty_movie": "📭 У списку фільмів поки порожньо.",
        "stats_empty": "📊 Поки немає записів для статистики.",
        "unknown": "Я не впізнав дію. Скористайся меню знизу або /help.",
    },
    "en": {
        "start": (
            "🌸 <b>Welcome to your media library.</b>\n\n"
            "Save anime and movies, add statuses and tags, and I will keep everything tidy."
        ),
        "help": (
            "✨ <b>How to use</b>\n\n"
            "1. Choose <b>➕ Anime</b> or <b>➕ Movie</b> from the menu.\n"
            "2. Send a title as text or a photo with the title in caption.\n"
            "3. Add tags with #, for example: <code>#watched #romance</code>.\n\n"
            "Statuses: <code>#watched</code>, <code>#want</code>, "
            "<code>#watching</code>, <code>#dropped</code>."
        ),
        "language_menu": "🌍 Choose interface language:",
        "language_updated": "✅ Language updated.",
        "anime_mode": (
            "➕ <b>Add mode: anime</b>\n\n"
            "Send a title or a photo with caption. Tags can be added with #."
        ),
        "movie_mode": (
            "➕ <b>Add mode: movie</b>\n\n"
            "Send a title or a photo with caption. Tags can be added with #."
        ),
        "missing_photo_caption": (
            "🖼 I got the photo, but there is no title.\n\n"
            "Add the title in caption, for example: <code>Perfect Blue #watched #psychological</code>."
        ),
        "empty_anime": "📭 Your anime list is empty for now.",
        "empty_movie": "📭 Your movie list is empty for now.",
        "stats_empty": "📊 No entries yet for stats.",
        "unknown": "I did not recognize that action. Use the bottom menu or /help.",
    },
}

MEDIA_LABELS: dict[Language, dict[MediaType, str]] = {
    "uk": {"anime": "аніме", "movie": "фільм"},
    "en": {"anime": "anime", "movie": "movie"},
}

STATUS_LABELS: dict[Language, dict[WatchStatus, str]] = {
    "uk": {
        "planned": "хочу подивитись",
        "watching": "дивлюсь",
        "watched": "переглянуто",
        "dropped": "закинуто",
    },
    "en": {
        "planned": "want to watch",
        "watching": "watching",
        "watched": "watched",
        "dropped": "dropped",
    },
}


def text(language: Language, key: str) -> str:
    return MESSAGES[language][key]


def added_message(language: Language, entry: MediaEntry) -> str:
    media = MEDIA_LABELS[language][entry.media_type]
    status = STATUS_LABELS[language][entry.status]
    tags = _tags_line(language, entry.tags)
    if language == "uk":
        return (
            f"✅ Додав {media}:\n"
            f"<b>{escape(entry.title)}</b>\n"
            f"🏷 Статус: <b>{status}</b>"
            f"{tags}"
        )

    return (
        f"✅ Added {media}:\n"
        f"<b>{escape(entry.title)}</b>\n"
        f"🏷 Status: <b>{status}</b>"
        f"{tags}"
    )


def media_list_message(language: Language, media_type: MediaType, entries: list[MediaEntry]) -> str:
    title = "📚 Твоє аніме:" if language == "uk" and media_type == "anime" else None
    if title is None:
        title = "🎬 Твої фільми:" if language == "uk" else None
    if title is None:
        title = "📚 Your anime:" if media_type == "anime" else "🎬 Your movies:"

    lines = [
        (
            f"{index}. <b>{escape(entry.title)}</b>\n"
            f"   {STATUS_LABELS[language][entry.status]}{_inline_tags(entry.tags)}"
        )
        for index, entry in enumerate(entries, start=1)
    ]
    return title + "\n\n" + "\n".join(lines)


def stats_message(language: Language, entries: list[MediaEntry]) -> str:
    anime_count = sum(1 for entry in entries if entry.media_type == "anime")
    movie_count = sum(1 for entry in entries if entry.media_type == "movie")
    watched_count = sum(1 for entry in entries if entry.status == "watched")
    planned_count = sum(1 for entry in entries if entry.status == "planned")

    if language == "uk":
        return (
            "📊 <b>Твоя медіатека</b>\n\n"
            f"🌸 Аніме: <b>{anime_count}</b>\n"
            f"🎬 Фільми: <b>{movie_count}</b>\n"
            f"✅ Переглянуто: <b>{watched_count}</b>\n"
            f"🕒 Хочу подивитись: <b>{planned_count}</b>"
        )

    return (
        "📊 <b>Your media library</b>\n\n"
        f"🌸 Anime: <b>{anime_count}</b>\n"
        f"🎬 Movies: <b>{movie_count}</b>\n"
        f"✅ Watched: <b>{watched_count}</b>\n"
        f"🕒 Want to watch: <b>{planned_count}</b>"
    )


def _tags_line(language: Language, tags: list[str]) -> str:
    if not tags:
        return ""
    label = "Теги" if language == "uk" else "Tags"
    return f"\n🏷 {label}: " + ", ".join(f"#{escape(tag)}" for tag in tags)


def _inline_tags(tags: list[str]) -> str:
    if not tags:
        return ""
    return " · " + " ".join(f"#{escape(tag)}" for tag in tags)
