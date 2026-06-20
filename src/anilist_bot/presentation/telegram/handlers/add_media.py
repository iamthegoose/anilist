from aiogram import F, Router
from aiogram.types import Message

from anilist_bot.application.media_library_service import MediaLibraryService
from anilist_bot.presentation.telegram.i18n import added_message, text
from anilist_bot.presentation.telegram.keyboards import ALL_BUTTON_TEXTS, main_menu


def build_add_media_router(media_library: MediaLibraryService) -> Router:
    router = Router(name="add_media")

    @router.message(F.photo)
    async def add_with_photo(message: Message) -> None:
        profile = await media_library.get_profile(message.from_user.id)
        caption = (message.caption or "").strip()
        if not caption:
            await message.answer(
                text(profile.language, "missing_photo_caption"),
                reply_markup=main_menu(profile.language),
            )
            return

        photo = message.photo[-1]
        entry = await media_library.add_photo_entry(
            user_id=message.from_user.id,
            caption=caption,
            photo_file_id=photo.file_id,
        )
        await message.answer(
            added_message(profile.language, entry),
            reply_markup=main_menu(profile.language),
        )

    @router.message(F.text)
    async def add_from_text(message: Message) -> None:
        title = message.text.strip()
        if title.startswith("/") or title in ALL_BUTTON_TEXTS:
            return

        profile = await media_library.get_profile(message.from_user.id)
        entry = await media_library.add_text_entry(user_id=message.from_user.id, text=title)
        await message.answer(
            added_message(profile.language, entry),
            reply_markup=main_menu(profile.language),
        )

    return router
