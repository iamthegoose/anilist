import re

from anilist_bot.domain.media import (
    EditAction,
    Language,
    MediaEntry,
    MediaType,
    UserProfile,
    WatchStatus,
)
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
NOTE_PATTERN = re.compile(r"\s@(.+)$")


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
        title, status, tags, note = parse_media_text(text)
        entry = MediaEntry(
            user_id=user_id,
            title=title,
            media_type=profile.pending_media_type,
            status=status,
            tags=tags,
            note=note,
            image=self._fallback_image_url,
            image_kind="fallback_url",
        )
        await self._repository.add(entry)
        await self._remember_last_entry(profile, entry.id)
        return entry

    async def add_photo_entry(self, user_id: int, caption: str, photo_file_id: str) -> MediaEntry:
        profile = await self._repository.get_profile(user_id)
        title, status, tags, note = parse_media_text(caption)
        entry = MediaEntry(
            user_id=user_id,
            title=title,
            media_type=profile.pending_media_type,
            status=status,
            tags=tags,
            note=note,
            image=photo_file_id,
            image_kind="telegram_file_id",
        )
        await self._repository.add(entry)
        await self._remember_last_entry(profile, entry.id)
        return entry

    async def list_entries(self, user_id: int, media_type: MediaType | None = None) -> list[MediaEntry]:
        return await self._repository.list_by_user(user_id, media_type)

    async def get_last_entry(self, user_id: int) -> MediaEntry | None:
        profile = await self._repository.get_profile(user_id)
        if profile.last_entry_id is None:
            return None
        return await self._repository.get_by_id(user_id, profile.last_entry_id)

    async def start_edit_last_entry(
        self,
        user_id: int,
        action: EditAction,
    ) -> tuple[UserProfile, MediaEntry | None]:
        profile = await self._repository.get_profile(user_id)
        entry = await self.get_last_entry(user_id)
        if entry is None:
            return profile, None

        profile.pending_edit_entry_id = entry.id
        profile.pending_edit_action = action
        await self._repository.save_profile(profile)
        return profile, entry

    async def apply_pending_edit(self, user_id: int, value: str) -> tuple[UserProfile, MediaEntry | None]:
        profile = await self._repository.get_profile(user_id)
        if profile.pending_edit_entry_id is None or profile.pending_edit_action is None:
            return profile, None

        entry = await self._repository.get_by_id(user_id, profile.pending_edit_entry_id)
        if entry is None:
            await self._clear_pending_edit(profile)
            return profile, None

        if profile.pending_edit_action == "title":
            entry.title = value.strip() or entry.title
        elif profile.pending_edit_action == "note":
            entry.note = value.strip() or None
        elif profile.pending_edit_action == "tags":
            entry.tags = parse_tags(value)

        await self._repository.update(entry)
        profile.last_entry_id = entry.id
        await self._clear_pending_edit(profile)
        return profile, entry

    async def set_last_entry_status(
        self,
        user_id: int,
        status: WatchStatus,
    ) -> tuple[UserProfile, MediaEntry | None]:
        profile = await self._repository.get_profile(user_id)
        entry = await self.get_last_entry(user_id)
        if entry is None:
            return profile, None

        entry.status = status
        await self._repository.update(entry)
        await self._clear_pending_edit(profile)
        return profile, entry

    async def clear_last_entry_note(self, user_id: int) -> tuple[UserProfile, MediaEntry | None]:
        profile = await self._repository.get_profile(user_id)
        entry = await self.get_last_entry(user_id)
        if entry is None:
            return profile, None

        entry.note = None
        await self._repository.update(entry)
        await self._clear_pending_edit(profile)
        return profile, entry

    async def cancel_pending_edit(self, user_id: int) -> UserProfile:
        profile = await self._repository.get_profile(user_id)
        await self._clear_pending_edit(profile)
        return profile

    async def _remember_last_entry(self, profile: UserProfile, entry_id: str) -> None:
        profile.last_entry_id = entry_id
        profile.pending_edit_entry_id = None
        profile.pending_edit_action = None
        await self._repository.save_profile(profile)

    async def _clear_pending_edit(self, profile: UserProfile) -> None:
        profile.pending_edit_entry_id = None
        profile.pending_edit_action = None
        await self._repository.save_profile(profile)


def parse_media_text(text: str) -> tuple[str, WatchStatus, list[str], str | None]:
    note_match = NOTE_PATTERN.search(text)
    note = note_match.group(1).strip() if note_match else None
    text_without_note = NOTE_PATTERN.sub("", text).strip()
    tags = [match.group(1).lower() for match in TAG_PATTERN.finditer(text_without_note)]
    status = next((STATUS_ALIASES[tag] for tag in tags if tag in STATUS_ALIASES), "watched")
    meaningful_tags = [tag for tag in tags if tag not in STATUS_ALIASES]
    title = TAG_PATTERN.sub("", text_without_note).strip()
    return title or text_without_note or text.strip(), status, meaningful_tags, note


def parse_tags(text: str) -> list[str]:
    hashtag_tags = [match.group(1).lower() for match in TAG_PATTERN.finditer(text)]
    if hashtag_tags:
        return [tag for tag in hashtag_tags if tag not in STATUS_ALIASES]
    return [tag.strip().lower() for tag in text.split(",") if tag.strip()]
