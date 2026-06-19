from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


ImageKind = Literal["telegram_file_id", "fallback_url"]


class AnimeEntry(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    user_id: int
    title: str
    image: str
    image_kind: ImageKind
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
