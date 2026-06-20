from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from anilist_bot.application.media_library_service import MediaLibraryService
from anilist_bot.presentation.telegram.i18n import text
from anilist_bot.presentation.telegram.keyboards import main_menu


def build_help_router(media_library: MediaLibraryService) -> Router:
    router = Router(name="help")

    @router.message(Command("help"))
    async def help_command(message: Message) -> None:
        profile = await media_library.get_profile(message.from_user.id)
        await message.answer(text(profile.language, "help"), reply_markup=main_menu(profile.language))

    return router
