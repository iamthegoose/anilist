from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from anilist_bot.application.media_library_service import MediaLibraryService
from anilist_bot.domain.media import Language, MediaEntry, MediaType
from anilist_bot.presentation.telegram.i18n import media_list_message, text
from anilist_bot.presentation.telegram.keyboards import BUTTONS, main_menu


def build_list_media_router(media_library: MediaLibraryService) -> Router:
    router = Router(name="list_media")

    @router.message(Command("list"))
    async def list_all_entries(message: Message) -> None:
        profile = await media_library.get_profile(message.from_user.id)
        entries = await media_library.list_entries(message.from_user.id)
        if not entries:
            await message.answer(text(profile.language, "stats_empty"), reply_markup=main_menu(profile.language))
            return

        await message.answer(_combined_list(profile.language, entries), reply_markup=main_menu(profile.language))

    @router.message(lambda message: message.text in _button_values("anime_list"))
    async def list_anime(message: Message) -> None:
        await _send_media_list(message, media_library, "anime")

    @router.message(lambda message: message.text in _button_values("movie_list"))
    async def list_movies(message: Message) -> None:
        await _send_media_list(message, media_library, "movie")

    return router


async def _send_media_list(
    message: Message,
    media_library: MediaLibraryService,
    media_type: MediaType,
) -> None:
    profile = await media_library.get_profile(message.from_user.id)
    entries = await media_library.list_entries(message.from_user.id, media_type)
    if not entries:
        await message.answer(
            text(profile.language, f"empty_{media_type}"),
            reply_markup=main_menu(profile.language),
        )
        return

    await message.answer(
        media_list_message(profile.language, media_type, entries),
        reply_markup=main_menu(profile.language),
    )


def _combined_list(language: Language, entries: list[MediaEntry]) -> str:
    sections = []
    anime = [entry for entry in entries if entry.media_type == "anime"]
    movies = [entry for entry in entries if entry.media_type == "movie"]
    if anime:
        sections.append(media_list_message(language, "anime", anime))
    if movies:
        sections.append(media_list_message(language, "movie", movies))
    return "\n\n".join(sections)


def _button_values(key: str) -> set[str]:
    return {buttons[key] for buttons in BUTTONS.values()}
