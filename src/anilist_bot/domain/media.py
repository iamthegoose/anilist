from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


ImageKind = Literal["telegram_file_id", "fallback_url"]
Language = Literal["uk", "en"]
MediaType = Literal["anime", "movie"]
WatchStatus = Literal["planned", "watching", "watched", "dropped"]
EditAction = Literal["title", "note", "tags"]


class MediaEntry(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    user_id: int
    title: str
    media_type: MediaType
    status: WatchStatus = "watched"
    tags: list[str] = Field(default_factory=list)
    note: str | None = None
    image: str
    image_kind: ImageKind
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserProfile(BaseModel):
    user_id: int
    language: Language = "uk"
    pending_media_type: MediaType = "anime"
    last_entry_id: str | None = None
    pending_edit_entry_id: str | None = None
    pending_edit_action: EditAction | None = None
