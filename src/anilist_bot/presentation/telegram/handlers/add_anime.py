from aiogram import F, Router
from aiogram.types import Message

from anilist_bot.application.anime_list_service import AnimeListService
from anilist_bot.presentation.telegram.messages import (
    MISSING_PHOTO_CAPTION_MESSAGE,
    added_message,
)


def build_add_anime_router(anime_lists: AnimeListService) -> Router:
    router = Router(name="add_anime")

    @router.message(F.photo)
    async def add_with_photo(message: Message) -> None:
        title = (message.caption or "").strip()
        if not title:
            await message.answer(MISSING_PHOTO_CAPTION_MESSAGE)
            return

        photo = message.photo[-1]
        entry = await anime_lists.add_photo_entry(
            user_id=message.from_user.id,
            title=title,
            photo_file_id=photo.file_id,
        )
        await message.answer(added_message(entry))

    @router.message(F.text)
    async def add_from_text(message: Message) -> None:
        title = message.text.strip()
        if title.startswith("/"):
            return

        entry = await anime_lists.add_text_entry(user_id=message.from_user.id, title=title)
        await message.answer(added_message(entry))

    return router
