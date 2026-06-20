import asyncio

from anilist_bot.application.media_library_service import MediaLibraryService
from anilist_bot.domain.media import MediaEntry, UserProfile


class InMemoryMediaRepository:
    def __init__(self) -> None:
        self.entries: list[MediaEntry] = []
        self.profiles: dict[int, UserProfile] = {}

    async def add(self, entry: MediaEntry) -> None:
        self.entries.append(entry)

    async def list_by_user(self, user_id: int, media_type=None) -> list[MediaEntry]:
        entries = [entry for entry in self.entries if entry.user_id == user_id]
        if media_type is None:
            return entries
        return [entry for entry in entries if entry.media_type == media_type]

    async def get_profile(self, user_id: int) -> UserProfile:
        return self.profiles.setdefault(user_id, UserProfile(user_id=user_id))

    async def save_profile(self, profile: UserProfile) -> None:
        self.profiles[profile.user_id] = profile


def test_service_adds_text_entry_with_fallback_image_and_tags():
    repository = InMemoryMediaRepository()
    service = MediaLibraryService(repository, fallback_image_url="https://example.com/fallback.png")

    entry = asyncio.run(service.add_text_entry(user_id=7, text="Frieren #watched #fantasy"))

    assert entry.title == "Frieren"
    assert entry.media_type == "anime"
    assert entry.status == "watched"
    assert entry.tags == ["fantasy"]
    assert entry.image == "https://example.com/fallback.png"
    assert entry.image_kind == "fallback_url"
    assert repository.entries == [entry]


def test_service_adds_movie_after_user_selects_movie_mode():
    repository = InMemoryMediaRepository()
    service = MediaLibraryService(repository, fallback_image_url="fallback")

    asyncio.run(service.set_pending_media_type(user_id=7, media_type="movie"))
    entry = asyncio.run(
        service.add_photo_entry(user_id=7, caption="Inception #want #sci-fi", photo_file_id="file-id")
    )

    assert entry.title == "Inception"
    assert entry.media_type == "movie"
    assert entry.status == "planned"
    assert entry.tags == ["sci-fi"]
    assert entry.image == "file-id"
