from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from anilist_bot.presentation.telegram.messages import HELP_MESSAGE


def build_help_router() -> Router:
    router = Router(name="help")

    @router.message(Command("help"))
    async def help_command(message: Message) -> None:
        await message.answer(HELP_MESSAGE)

    return router
