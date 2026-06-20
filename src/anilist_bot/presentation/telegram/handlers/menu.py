from aiogram import Router
from aiogram.types import Message

from anilist_bot.application.media_library_service import MediaLibraryService
from anilist_bot.presentation.telegram.i18n import stats_message, text
from anilist_bot.presentation.telegram.keyboards import BUTTONS, language_menu, main_menu


def build_menu_router(media_library: MediaLibraryService) -> Router:
    router = Router(name="menu")

    @router.message(lambda message: message.text in _button_values("add_anime"))
    async def set_anime_mode(message: Message) -> None:
        profile = await media_library.set_pending_media_type(message.from_user.id, "anime")
        await message.answer(text(profile.language, "anime_mode"), reply_markup=main_menu(profile.language))

    @router.message(lambda message: message.text in _button_values("add_movie"))
    async def set_movie_mode(message: Message) -> None:
        profile = await media_library.set_pending_media_type(message.from_user.id, "movie")
        await message.answer(text(profile.language, "movie_mode"), reply_markup=main_menu(profile.language))

    @router.message(lambda message: message.text in _button_values("language"))
    async def show_language_menu(message: Message) -> None:
        profile = await media_library.get_profile(message.from_user.id)
        await message.answer(
            text(profile.language, "language_menu"),
            reply_markup=language_menu(profile.language),
        )

    @router.message(lambda message: message.text in _button_values("stats"))
    async def show_stats(message: Message) -> None:
        profile = await media_library.get_profile(message.from_user.id)
        entries = await media_library.list_entries(message.from_user.id)
        if not entries:
            await message.answer(text(profile.language, "stats_empty"), reply_markup=main_menu(profile.language))
            return

        await message.answer(stats_message(profile.language, entries), reply_markup=main_menu(profile.language))

    @router.message(lambda message: message.text in _button_values("help"))
    async def show_help(message: Message) -> None:
        profile = await media_library.get_profile(message.from_user.id)
        await message.answer(text(profile.language, "help"), reply_markup=main_menu(profile.language))

    @router.message(lambda message: message.text in _button_values("ukrainian"))
    async def set_ukrainian(message: Message) -> None:
        profile = await media_library.set_language(message.from_user.id, "uk")
        await message.answer(text(profile.language, "language_updated"), reply_markup=main_menu(profile.language))

    @router.message(lambda message: message.text in _button_values("english"))
    async def set_english(message: Message) -> None:
        profile = await media_library.set_language(message.from_user.id, "en")
        await message.answer(text(profile.language, "language_updated"), reply_markup=main_menu(profile.language))

    return router


def _button_values(key: str) -> set[str]:
    return {buttons[key] for buttons in BUTTONS.values()}
