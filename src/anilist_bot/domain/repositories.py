from typing import Protocol

from anilist_bot.domain.media import MediaEntry, MediaType, UserProfile


class MediaRepository(Protocol):
    async def add(self, entry: MediaEntry) -> None:
        ...

    async def list_by_user(self, user_id: int, media_type: MediaType | None = None) -> list[MediaEntry]:
        ...

    async def get_profile(self, user_id: int) -> UserProfile:
        ...

    async def save_profile(self, profile: UserProfile) -> None:
        ...
