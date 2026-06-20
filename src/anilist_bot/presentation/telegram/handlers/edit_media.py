from aiogram import F, Router
from aiogram.filters import BaseFilter
from aiogram.types import Message

from anilist_bot.application.media_library_service import MediaLibraryService
from anilist_bot.domain.media import EditAction, WatchStatus
from anilist_bot.presentation.telegram.i18n import (
    edit_menu_message,
    entry_updated_message,
    text,
)
from anilist_bot.presentation.telegram.keyboards import BUTTONS, edit_menu, main_menu


def build_edit_media_router(media_library: MediaLibraryService) -> Router:
    router = Router(name="edit_media")

    @router.message(lambda message: message.text in _button_values("edit_last"))
    async def show_edit_menu(message: Message) -> None:
        profile = await media_library.get_profile(message.from_user.id)
        entry = await media_library.get_last_entry(message.from_user.id)
        if entry is None:
            await message.answer(
                text(profile.language, "edit_menu_empty"),
                reply_markup=main_menu(profile.language),
            )
            return

        await message.answer(edit_menu_message(profile.language, entry), reply_markup=edit_menu(profile.language))

    @router.message(lambda message: message.text in _button_values("back"))
    async def back_to_main_menu(message: Message) -> None:
        profile = await media_library.cancel_pending_edit(message.from_user.id)
        await message.answer(text(profile.language, "edit_cancelled"), reply_markup=main_menu(profile.language))

    @router.message(lambda message: message.text in _status_buttons())
    async def update_status(message: Message) -> None:
        status = _status_by_button(message.text)
        profile, entry = await media_library.set_last_entry_status(message.from_user.id, status)
        if entry is None:
            await message.answer(
                text(profile.language, "edit_menu_empty"),
                reply_markup=main_menu(profile.language),
            )
            return

        await message.answer(
            entry_updated_message(profile.language, entry),
            reply_markup=edit_menu(profile.language),
        )

    @router.message(lambda message: message.text in _button_values("clear_note"))
    async def clear_note(message: Message) -> None:
        profile, entry = await media_library.clear_last_entry_note(message.from_user.id)
        if entry is None:
            await message.answer(
                text(profile.language, "edit_menu_empty"),
                reply_markup=main_menu(profile.language),
            )
            return

        await message.answer(
            entry_updated_message(profile.language, entry),
            reply_markup=edit_menu(profile.language),
        )

    @router.message(lambda message: message.text in _edit_action_buttons())
    async def start_edit_action(message: Message) -> None:
        action = _action_by_button(message.text)
        profile, entry = await media_library.start_edit_last_entry(message.from_user.id, action)
        if entry is None:
            await message.answer(
                text(profile.language, "edit_menu_empty"),
                reply_markup=main_menu(profile.language),
            )
            return

        await message.answer(text(profile.language, f"edit_{action}_prompt"), reply_markup=edit_menu(profile.language))

    @router.message(F.text, PendingEditFilter(media_library))
    async def apply_pending_edit(message: Message) -> None:
        profile, entry = await media_library.apply_pending_edit(message.from_user.id, message.text)
        if entry is None:
            await message.answer(
                text(profile.language, "edit_menu_empty"),
                reply_markup=main_menu(profile.language),
            )
            return

        await message.answer(
            entry_updated_message(profile.language, entry),
            reply_markup=edit_menu(profile.language),
        )

    return router


class PendingEditFilter(BaseFilter):
    def __init__(self, media_library: MediaLibraryService) -> None:
        self._media_library = media_library

    async def __call__(self, message: Message) -> bool:
        profile = await self._media_library.get_profile(message.from_user.id)
        return profile.pending_edit_action is not None


def _button_values(key: str) -> set[str]:
    return {buttons[key] for buttons in BUTTONS.values()}


def _status_buttons() -> set[str]:
    return (
        _button_values("status_planned")
        | _button_values("status_watching")
        | _button_values("status_watched")
        | _button_values("status_dropped")
    )


def _edit_action_buttons() -> set[str]:
    return _button_values("edit_title") | _button_values("edit_note") | _button_values("edit_tags")


def _status_by_button(button: str) -> WatchStatus:
    mapping = {
        **{value: "planned" for value in _button_values("status_planned")},
        **{value: "watching" for value in _button_values("status_watching")},
        **{value: "watched" for value in _button_values("status_watched")},
        **{value: "dropped" for value in _button_values("status_dropped")},
    }
    return mapping[button]


def _action_by_button(button: str) -> EditAction:
    mapping = {
        **{value: "title" for value in _button_values("edit_title")},
        **{value: "note" for value in _button_values("edit_note")},
        **{value: "tags" for value in _button_values("edit_tags")},
    }
    return mapping[button]
