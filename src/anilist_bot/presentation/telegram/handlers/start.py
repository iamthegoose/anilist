from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from anilist_bot.presentation.telegram.messages import START_MESSAGE


def build_start_router() -> Router:
    router = Router(name="start")

    @router.message(CommandStart())
    async def start(message: Message) -> None:
        await message.answer(START_MESSAGE)

    return router
