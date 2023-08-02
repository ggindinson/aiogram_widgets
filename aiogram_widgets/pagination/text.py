from typing import Annotated, List

from aiogram import Dispatcher, F, Router
from aiogram.filters.state import StateFilter
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pydantic import Field, PositiveInt, validate_arguments

from aiogram_widgets.pagination._base import BasePaginator
from aiogram_widgets.types import Additional_buttons_type, Pagination_key


class TextPaginator(BasePaginator):
    """Allows to create a new markup with text pagination"""

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def __init__(
        self,
        data: Annotated[List[str], Field(min_length=1)],
        router: Dispatcher | Router,
        data_joiner: str = "\n",
        additional_buttons: Additional_buttons_type | None = None,
        pagination_key: Pagination_key = "text_paginated",
        per_page: PositiveInt = 10,
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
        :param data_joiner: string, which will `join` current text chunk to one text `(default=new string)`
        :param additional_buttons: provide additional buttons, that will be inserted after pagination panel. `(default=None)`
        :param pagination_key: callback data, which will be attached to the callback of each pagination button `(default="text_paginated")`
        :param per_page: amount of items per page `(default=10)`
        """
        super().__init__(data, per_page, pagination_key, router, additional_buttons)
        self.data_joiner = data_joiner

    def _build(self):
        self.builder = InlineKeyboardBuilder()
        self._build_pagination_buttons(self.builder)

    def _register_handler(self):
        """"""

        async def __callback_handler(call: CallbackQuery):
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

        self.router.callback_query.register(
            __callback_handler,
            F.data.startswith(self.pagination_key),
            StateFilter("*"),
        )

    @property
    def current_message_data(self) -> tuple[str, InlineKeyboardMarkup]:
        return self._format_data_chunk(), self.as_markup()

    def _format_data_chunk(self) -> str:
        return self.data_joiner.join(self._current_data_chunk)
