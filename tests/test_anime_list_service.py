import asyncio

from anilist_bot.application.anime_list_service import AnimeListService
from anilist_bot.domain.anime import AnimeEntry


class InMemoryAnimeRepository:
    def __init__(self) -> None:
        self.entries: list[AnimeEntry] = []

    async def add(self, entry: AnimeEntry) -> None:
        self.entries.append(entry)

    async def list_by_user(self, user_id: int) -> list[AnimeEntry]:
        return [entry for entry in self.entries if entry.user_id == user_id]


def test_service_adds_text_entry_with_fallback_image():
    repository = InMemoryAnimeRepository()
    service = AnimeListService(repository, fallback_image_url="https://example.com/fallback.png")

    entry = asyncio.run(service.add_text_entry(user_id=7, title="Frieren"))

    assert entry.title == "Frieren"
    assert entry.image == "https://example.com/fallback.png"
    assert entry.image_kind == "fallback_url"
    assert repository.entries == [entry]


def test_service_adds_photo_entry_with_telegram_file_id():
    repository = InMemoryAnimeRepository()
    service = AnimeListService(repository, fallback_image_url="fallback")

    entry = asyncio.run(
        service.add_photo_entry(user_id=7, title="Cowboy Bebop", photo_file_id="telegram-file-id")
    )

    assert entry.title == "Cowboy Bebop"
    assert entry.image == "telegram-file-id"
    assert entry.image_kind == "telegram_file_id"
