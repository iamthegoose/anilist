from anilist_bot.domain.anime import AnimeEntry
from anilist_bot.presentation.telegram.messages import added_message, anime_list_message


def test_added_message_formats_title_for_html_parse_mode():
    entry = AnimeEntry(
        user_id=1,
        title="Frieren <Beyond Journey's End>",
        image="fallback",
        image_kind="fallback_url",
    )

    assert (
        added_message(entry)
        == "✅ Додав у список:\n<b>Frieren &lt;Beyond Journey&#x27;s End&gt;</b>"
    )


def test_anime_list_message_is_user_friendly():
    entries = [
        AnimeEntry(user_id=1, title="Frieren", image="fallback", image_kind="fallback_url"),
        AnimeEntry(user_id=1, title="Cowboy Bebop", image="fallback", image_kind="fallback_url"),
    ]

    assert anime_list_message(entries) == (
        "📚 Твої переглянуті аніме:\n\n"
        "1. 🎬 Frieren\n"
        "2. 🎬 Cowboy Bebop"
    )
