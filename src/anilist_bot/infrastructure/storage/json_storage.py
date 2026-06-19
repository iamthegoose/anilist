import json
from pathlib import Path

from anilist_bot.domain.anime import AnimeEntry


class JsonAnimeRepository:
    def __init__(self, path: Path) -> None:
        self._path = path

    async def add(self, entry: AnimeEntry) -> None:
        entries = await self.list_by_user(entry.user_id)
        entries.append(entry)
        await self._write_all(entries, user_id=entry.user_id)

    async def list_by_user(self, user_id: int) -> list[AnimeEntry]:
        return [entry for entry in self._read_all() if entry.user_id == user_id]

    def _read_all(self) -> list[AnimeEntry]:
        if not self._path.exists():
            return []

        with self._path.open("r", encoding="utf-8") as file:
            raw_entries = json.load(file)

        return [AnimeEntry.model_validate(item) for item in raw_entries]

    async def _write_all(self, user_entries: list[AnimeEntry], user_id: int) -> None:
        all_entries = [entry for entry in self._read_all() if entry.user_id != user_id]
        all_entries.extend(user_entries)

        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("w", encoding="utf-8") as file:
            json.dump(
                [entry.model_dump(mode="json") for entry in all_entries],
                file,
                ensure_ascii=False,
                indent=2,
            )
            file.write("\n")
