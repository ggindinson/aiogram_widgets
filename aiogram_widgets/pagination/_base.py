from abc import ABC, abstractmethod
from math import ceil
from typing import Any, Dict, List

import aiogram
from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

if aiogram.__version__ >= "3.0.0b8":
    from pydantic.v1 import validate_arguments
else:
    from pydantic import validate_arguments

from aiogram_widgets.types import AdditionalButtonsType, PaginationButtonsType


class BasePaginator(ABC):
    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def __init__(
        self,
        data: List[Any],
        per_page: int,
        router: Router,
        pagination_key: str,
        pagination_buttons: PaginationButtonsType = ["⏪", "⬅️", "➡️", "⏩"],
        additional_buttons: AdditionalButtonsType | None = None,
    ):
        """Base paginator class, which implements basic methods"""
        self.data = data
        self.builder = InlineKeyboardBuilder()
        self.pagination_key = pagination_key
        self.router = router
        self.additional_buttons = additional_buttons

        self.per_page = per_page
        self.first_page_index = 1
        self.current_page_index = self.first_page_index
        self.last_page_index = self._last_page_index
        self.pagination_buttons = pagination_buttons

        self.paginator_exists: bool = self.last_page_index - self.first_page_index > 0
        self._build()
        if self.paginator_exists:
            self._register_handler()

    def as_builder(self) -> InlineKeyboardBuilder:
        return self.builder

    def as_markup(self) -> InlineKeyboardMarkup:
        return self.builder.as_markup()

    @abstractmethod
    def _build(self):
        """Build a keyboard using InlineKeyboardBuilder"""
        ...

    @abstractmethod
    async def _callback_handler(self, call: CallbackQuery):
        """Handler for pagination updates"""
        ...

    def _register_handler(self):
        """"""

        self.router.callback_query.register(
            self._callback_handler,
            F.data.startswith(self.pagination_key),
            StateFilter("*"),
        )

    def _build_pagination_buttons(self, builder: InlineKeyboardBuilder):
        if self.paginator_exists:
            pagination_buttons: List[InlineKeyboardButton] = []
            if self.current_page_index > self.first_page_index:
                self._add_pagination_button_if_exists(
                    button_index=0,
                    callback_data=f"{self.pagination_key}|{self.first_page_index}",
                    pagination_buttons=pagination_buttons,
                )
                self._add_pagination_button_if_exists(
                    button_index=1,
                    callback_data=f"{self.pagination_key}|{self.current_page_index - 1}",
                    pagination_buttons=pagination_buttons,
                )
            pagination_buttons.append(
                InlineKeyboardButton(
                    text=f"{self.current_page_index}/{self.last_page_index}",
                    callback_data="pass",
                )
            )
            if self.current_page_index < self.last_page_index:
                self._add_pagination_button_if_exists(
                    button_index=2,
                    callback_data=f"{self.pagination_key}|{self.current_page_index + 1}",
                    pagination_buttons=pagination_buttons,
                )
                self._add_pagination_button_if_exists(
                    button_index=3,
                    callback_data=f"{self.pagination_key}|{self.last_page_index}",
                    pagination_buttons=pagination_buttons,
                )
            builder.row(*pagination_buttons)
        if self.additional_buttons:
            for button_row in self.additional_buttons:
                builder.row(*[self._format_button(button) for button in button_row])

    def _format_button(
        self, button: InlineKeyboardButton | Dict[str, Any]
    ) -> InlineKeyboardButton:
        """Format button to InlineKeyboardButton"""
        if isinstance(button, InlineKeyboardButton):
            return button
        return InlineKeyboardButton(**button)

    def _add_pagination_button_if_exists(
        self,
        button_index: int,
        callback_data: str,
        pagination_buttons: List[InlineKeyboardButton],
    ):
        button_text = self.pagination_buttons[button_index]
        if button_text is not None:
            pagination_buttons.append(
                InlineKeyboardButton(text=button_text, callback_data=callback_data)
            )

    @property
    def _current_data_chunk(self) -> List[Any]:
        start_index = (self.current_page_index - 1) * self.per_page
        end_index = start_index + self.per_page
        current_data_chunk = self.data[start_index:end_index]

        return current_data_chunk

    @property
    def _last_page_index(self) -> int:
        return ceil(len(self.data) / self.per_page)
