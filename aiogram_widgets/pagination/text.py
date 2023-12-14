from typing import Annotated, List

import aiogram
from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

if aiogram.__version__ >= "3.0.0b8":
    from pydantic.v1 import Field
else:
    from pydantic import Field

from aiogram_widgets.pagination._base import BasePaginator
from aiogram_widgets.types import (
    AdditionalButtonsType,
    PaginationButtonsType,
    PerPageIntType,
)


class TextPaginator(BasePaginator):
    """Allows to create a new markup with text pagination"""

    def __init__(
        self,
        data: Annotated[List[str], Field(min_items=1)],
        router: Router,
        join_symbol: str = "\n",
        additional_buttons: AdditionalButtonsType = list(),
        pagination_buttons: PaginationButtonsType = ["⏪", "⬅️", "➡️", "⏩"],
        per_page: PerPageIntType = 10,
    ):
        """
        :param data: list of text chunks (`required`)
        >>> data = [
            [
                        "Text number 1",
                        "Text number 2",
                        "Text number 3",
                        ...,
                        "Text number 999",
            ],
        ]

        :param router: pagination automatization. (`required`)
        :param join_symbol: string, which will `join` current text chunk to one text `(default=new string)`
        :param additional_buttons: provide additional buttons, that will be inserted after pagination panel. `(default=None)`
        :param pagination_key: custom callback data, which will be attached to the callback of each pagination button
        :param pagination_buttons: list of `four` buttons, where each is a string or None (if you don't want to add this button) `(default=["⏪", "⬅️", "➡️", "⏩"])`
        :param per_page: amount of items per page `(default=10)`
        """
        super().__init__(
            data=data,
            router=router,
            additional_buttons=additional_buttons,
            pagination_buttons=pagination_buttons,
            per_page=per_page,
        )
        self.join_symbol = join_symbol

    def _build(self):
        self.builder = InlineKeyboardBuilder()
        self._build_pagination_buttons(self.builder)

    async def _callback_handler(self, call: CallbackQuery):
        self.current_page_index = int(call.data.split("|")[-1])
        self._build()

        text, reply_markup = (
            self._format_data_chunk(),
            self.as_markup(),
        )
        if call.message.caption:
            await call.message.edit_caption(
                caption=text,
                reply_markup=reply_markup,
                disable_web_page_preview=True,
            )
        else:
            await call.message.edit_text(
                text=text, reply_markup=reply_markup, disable_web_page_preview=True
            )

    @property
    def current_message_data(self) -> tuple[str, InlineKeyboardMarkup]:
        return self._format_data_chunk(), self.as_markup()

    def _format_data_chunk(self) -> str:
        return self.join_symbol.join(self._current_data_chunk)
