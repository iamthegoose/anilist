from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from anilist_bot.application.anime_list_service import AnimeListService
from anilist_bot.presentation.telegram.messages import EMPTY_LIST_MESSAGE, anime_list_message


def build_list_anime_router(anime_lists: AnimeListService) -> Router:
    router = Router(name="list_anime")

    @router.message(Command("list"))
    async def list_entries(message: Message) -> None:
        entries = await anime_lists.list_entries(message.from_user.id)
        if not entries:
            await message.answer(EMPTY_LIST_MESSAGE)
            return

        await message.answer(anime_list_message(entries))

    return router
