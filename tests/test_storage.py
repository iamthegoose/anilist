import asyncio

from anilist_bot.domain.media import MediaEntry
from anilist_bot.infrastructure.storage.json_storage import JsonMediaRepository


def test_storage_keeps_entries_scoped_by_user_and_media_type(tmp_path):
    storage = JsonMediaRepository(tmp_path / "media.json")

    asyncio.run(
        storage.add(
            MediaEntry(
                user_id=1,
                title="Frieren",
                media_type="anime",
                image="fallback",
                image_kind="fallback_url",
            )
        )
    )
    asyncio.run(
        storage.add(
            MediaEntry(
                user_id=1,
                title="Inception",
                media_type="movie",
                image="photo-file-id",
                image_kind="telegram_file_id",
            )
        )
    )

    entries = asyncio.run(storage.list_by_user(1, "movie"))

    assert len(entries) == 1
    assert entries[0].title == "Inception"
    assert entries[0].media_type == "movie"


def test_storage_persists_user_profile(tmp_path):
    storage = JsonMediaRepository(tmp_path / "media.json")

    profile = asyncio.run(storage.get_profile(42))
    profile.language = "en"
    profile.pending_media_type = "movie"
    asyncio.run(storage.save_profile(profile))

    loaded = asyncio.run(storage.get_profile(42))

    assert loaded.language == "en"
    assert loaded.pending_media_type == "movie"
