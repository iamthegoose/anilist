import asyncio

from anilist_bot.domain.anime import AnimeEntry
from anilist_bot.infrastructure.storage.json_storage import JsonAnimeRepository


def test_storage_keeps_entries_scoped_by_user(tmp_path):
    storage = JsonAnimeRepository(tmp_path / "anime.json")

    asyncio.run(
        storage.add(
            AnimeEntry(
                user_id=1,
                title="Frieren",
                image="fallback",
                image_kind="fallback_url",
            )
        )
    )
    asyncio.run(
        storage.add(
            AnimeEntry(
                user_id=2,
                title="Cowboy Bebop",
                image="photo-file-id",
                image_kind="telegram_file_id",
            )
        )
    )

    entries = asyncio.run(storage.list_by_user(1))

    assert len(entries) == 1
    assert entries[0].title == "Frieren"
    assert entries[0].image_kind == "fallback_url"
