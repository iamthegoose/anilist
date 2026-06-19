from typing import Protocol

from anilist_bot.domain.anime import AnimeEntry


class AnimeRepository(Protocol):
    async def add(self, entry: AnimeEntry) -> None:
        ...

    async def list_by_user(self, user_id: int) -> list[AnimeEntry]:
        ...
