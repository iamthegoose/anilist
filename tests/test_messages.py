from anilist_bot.domain.media import MediaEntry
from anilist_bot.presentation.telegram.i18n import added_message, media_list_message


def test_added_message_formats_and_escapes_title_for_html_parse_mode():
    entry = MediaEntry(
        user_id=1,
        title="Frieren <Beyond Journey's End>",
        media_type="anime",
        status="watched",
        tags=["fantasy"],
        image="fallback",
        image_kind="fallback_url",
    )

    assert added_message("uk", entry) == (
        "✅ Додав аніме:\n"
        "<b>Frieren &lt;Beyond Journey&#x27;s End&gt;</b>\n"
        "🏷 Статус: <b>переглянуто</b>\n"
        "🏷 Теги: #fantasy"
    )


def test_media_list_message_is_user_friendly():
    entries = [
        MediaEntry(
            user_id=1,
            title="Frieren",
            media_type="anime",
            image="fallback",
            image_kind="fallback_url",
        ),
        MediaEntry(
            user_id=1,
            title="Cowboy Bebop",
            media_type="anime",
            image="fallback",
            image_kind="fallback_url",
        ),
    ]

    assert media_list_message("en", "anime", entries) == (
        "📚 Your anime:\n\n"
        "1. <b>Frieren</b>\n"
        "   watched\n"
        "2. <b>Cowboy Bebop</b>\n"
        "   watched"
    )
