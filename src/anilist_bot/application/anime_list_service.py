from anilist_bot.domain.anime import AnimeEntry
from anilist_bot.domain.repositories import AnimeRepository


class AnimeListService:
    def __init__(self, repository: AnimeRepository, fallback_image_url: str) -> None:
        self._repository = repository
        self._fallback_image_url = fallback_image_url

    async def add_text_entry(self, user_id: int, title: str) -> AnimeEntry:
        entry = AnimeEntry(
            user_id=user_id,
            title=title,
            image=self._fallback_image_url,
            image_kind="fallback_url",
        )
        await self._repository.add(entry)
        return entry

    async def add_photo_entry(self, user_id: int, title: str, photo_file_id: str) -> AnimeEntry:
        entry = AnimeEntry(
            user_id=user_id,
            title=title,
            image=photo_file_id,
            image_kind="telegram_file_id",
        )
        await self._repository.add(entry)
        return entry

    async def list_entries(self, user_id: int) -> list[AnimeEntry]:
        return await self._repository.list_by_user(user_id)
