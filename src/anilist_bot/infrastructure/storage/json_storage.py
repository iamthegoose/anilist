import json
from pathlib import Path
from typing import Any

from anilist_bot.domain.media import MediaEntry, MediaType, UserProfile


class JsonMediaRepository:
    def __init__(self, path: Path) -> None:
        self._path = path

    async def add(self, entry: MediaEntry) -> None:
        state = self._read_state()
        entries = [item for item in state.entries if item.user_id != entry.user_id]
        entries.extend(await self.list_by_user(entry.user_id))
        entries.append(entry)
        state.entries = entries
        self._write_state(state)

    async def list_by_user(
        self,
        user_id: int,
        media_type: MediaType | None = None,
    ) -> list[MediaEntry]:
        entries = [entry for entry in self._read_state().entries if entry.user_id == user_id]
        if media_type is None:
            return entries
        return [entry for entry in entries if entry.media_type == media_type]

    async def get_profile(self, user_id: int) -> UserProfile:
        state = self._read_state()
        profile = state.profiles.get(str(user_id))
        if profile is not None:
            return profile

        profile = UserProfile(user_id=user_id)
        state.profiles[str(user_id)] = profile
        self._write_state(state)
        return profile

    async def save_profile(self, profile: UserProfile) -> None:
        state = self._read_state()
        state.profiles[str(profile.user_id)] = profile
        self._write_state(state)

    def _read_state(self) -> "_StorageState":
        if not self._path.exists():
            return _StorageState()

        with self._path.open("r", encoding="utf-8") as file:
            raw_state = json.load(file)

        return _StorageState.from_raw(raw_state)

    def _write_state(self, state: "_StorageState") -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("w", encoding="utf-8") as file:
            json.dump(state.to_raw(), file, ensure_ascii=False, indent=2)
            file.write("\n")


class _StorageState:
    def __init__(
        self,
        entries: list[MediaEntry] | None = None,
        profiles: dict[str, UserProfile] | None = None,
    ) -> None:
        self.entries = entries or []
        self.profiles = profiles or {}

    @classmethod
    def from_raw(cls, raw_state: Any) -> "_StorageState":
        if isinstance(raw_state, list):
            return cls(entries=[_entry_from_legacy(item) for item in raw_state])

        raw_entries = raw_state.get("entries", [])
        raw_profiles = raw_state.get("profiles", {})
        return cls(
            entries=[MediaEntry.model_validate(item) for item in raw_entries],
            profiles={
                str(user_id): UserProfile.model_validate(profile)
                for user_id, profile in raw_profiles.items()
            },
        )

    def to_raw(self) -> dict[str, Any]:
        return {
            "entries": [entry.model_dump(mode="json") for entry in self.entries],
            "profiles": {
                user_id: profile.model_dump(mode="json")
                for user_id, profile in self.profiles.items()
            },
        }


def _entry_from_legacy(raw_entry: dict[str, Any]) -> MediaEntry:
    return MediaEntry.model_validate(
        {
            **raw_entry,
            "media_type": raw_entry.get("media_type", "anime"),
            "status": raw_entry.get("status", "watched"),
            "tags": raw_entry.get("tags", []),
        }
    )
