import re

from anilist_bot.domain.media import Language, MediaEntry, MediaType, UserProfile, WatchStatus
from anilist_bot.domain.repositories import MediaRepository

STATUS_ALIASES: dict[str, WatchStatus] = {
    "watched": "watched",
    "переглянуто": "watched",
    "done": "watched",
    "planned": "planned",
    "plan": "planned",
    "want": "planned",
    "хочу": "planned",
    "планую": "planned",
    "watching": "watching",
    "дивлюсь": "watching",
    "dropped": "dropped",
    "drop": "dropped",
    "закинуто": "dropped",
}

TAG_PATTERN = re.compile(r"(?<!\w)#([\wа-яА-ЯіїєґІЇЄҐ-]+)")


class MediaLibraryService:
    def __init__(self, repository: MediaRepository, fallback_image_url: str) -> None:
        self._repository = repository
        self._fallback_image_url = fallback_image_url

    async def get_profile(self, user_id: int) -> UserProfile:
        return await self._repository.get_profile(user_id)

    async def set_language(self, user_id: int, language: Language) -> UserProfile:
        profile = await self._repository.get_profile(user_id)
        profile.language = language
        await self._repository.save_profile(profile)
        return profile

    async def set_pending_media_type(self, user_id: int, media_type: MediaType) -> UserProfile:
        profile = await self._repository.get_profile(user_id)
        profile.pending_media_type = media_type
        await self._repository.save_profile(profile)
        return profile

    async def add_text_entry(self, user_id: int, text: str) -> MediaEntry:
        profile = await self._repository.get_profile(user_id)
        title, status, tags = parse_media_text(text)
        entry = MediaEntry(
            user_id=user_id,
            title=title,
            media_type=profile.pending_media_type,
            status=status,
            tags=tags,
            image=self._fallback_image_url,
            image_kind="fallback_url",
        )
        await self._repository.add(entry)
        return entry

    async def add_photo_entry(self, user_id: int, caption: str, photo_file_id: str) -> MediaEntry:
        profile = await self._repository.get_profile(user_id)
        title, status, tags = parse_media_text(caption)
        entry = MediaEntry(
            user_id=user_id,
            title=title,
            media_type=profile.pending_media_type,
            status=status,
            tags=tags,
            image=photo_file_id,
            image_kind="telegram_file_id",
        )
        await self._repository.add(entry)
        return entry

    async def list_entries(self, user_id: int, media_type: MediaType | None = None) -> list[MediaEntry]:
        return await self._repository.list_by_user(user_id, media_type)


def parse_media_text(text: str) -> tuple[str, WatchStatus, list[str]]:
    tags = [match.group(1).lower() for match in TAG_PATTERN.finditer(text)]
    status = next((STATUS_ALIASES[tag] for tag in tags if tag in STATUS_ALIASES), "watched")
    meaningful_tags = [tag for tag in tags if tag not in STATUS_ALIASES]
    title = TAG_PATTERN.sub("", text).strip()
    return title or text.strip(), status, meaningful_tags
