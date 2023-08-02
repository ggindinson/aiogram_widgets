from typing import Annotated, List

from aiogram import Dispatcher, F, Router
from aiogram.filters.state import StateFilter
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pydantic import Field, validate_arguments

from aiogram_widgets.pagination._base import BasePaginator
from aiogram_widgets.types import (
    Additional_buttons_type,
    Button_type,
    Pagination_key,
    Per_page_type,
    Per_row_type,
)


class KeyboardPaginator(BasePaginator):
    """Allows to create a new markup with keyboard pagination"""

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def __init__(
        self,
        data: Annotated[List[Button_type], Field(min_length=1)],
        router: Dispatcher | Router,
        additional_buttons: Additional_buttons_type | None = None,
        pagination_key: Pagination_key = "keyboard_paginated",
        per_row: Per_row_type = 2,
        per_page: Per_page_type = 10,
    ):
        """
        :param data - buttons data. (`required`)
        >>> data = [
            {
                "text": "Button name",
                "callback_data": "callback_data",
            },
            InlineKeyboardButton(text="Button name 2", callback_data="callback_data_2"),
            {
                "text": "Button name 999",
                "callback_data": "callback_data_999",
            },
        ]

        :param router: pagination automatization. (`required`)
        :param additional_buttons: provide additional buttons, that will be inserted after pagination panel. `(default=None)`
        :param pagination_key: callback data, which will be attached to the callback of each pagination button `(default="text_paginated")`
        :param per_row: amount of items per row `(default=2)`
        :param per_page: amount of items per page `(default=10)`
        """
        self.per_row = per_row
        super().__init__(data, per_page, pagination_key, router, additional_buttons)

    def _build(self):
        self.builder = InlineKeyboardBuilder()

        for button in self._current_data_chunk:
            button = self._format_button(button)
            self.builder.add(button)

        self.builder.adjust(self.per_row)

        self._build_pagination_buttons(self.builder)

    def _register_handler(self):
        """"""

        async def __callback_handler(call: CallbackQuery):
            self.current_page_index = int(call.data.split("|")[-1])
            self._build()

            await call.message.edit_reply_markup(reply_markup=self.as_markup())

        self.router.callback_query.register(
            __callback_handler,
            F.data.startswith(self.pagination_key),
            StateFilter("*"),
        )

    def _format_button(self, button: Button_type) -> InlineKeyboardButton:
        return (
            InlineKeyboardButton(**button)
            if not isinstance(button, InlineKeyboardButton)
            else button
        )
