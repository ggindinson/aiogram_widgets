from abc import ABC, abstractmethod
from math import ceil
from typing import Any, Dict, List

from aiogram import Dispatcher, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram_widgets.types.types import Additional_buttons_type


class BasePaginator(ABC):
    def __init__(
        self,
        data: List[Any],
        per_page: int,
        pagination_key: str,
        router: Dispatcher | Router,
        additional_buttons: Additional_buttons_type | None = None,
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
    def _register_handler(self):
        """Register a handler for managing pagination"""
        ...

    @property
    def _current_data_chunk(self) -> List[Any]:
        start_index = (self.current_page_index - 1) * self.per_page
        end_index = start_index + self.per_page
        current_data_chunk = self.data[start_index:end_index]

        return current_data_chunk

    def _format_button(
        self, button: InlineKeyboardButton | Dict[str, Any]
    ) -> InlineKeyboardButton:
        """Register a handler for managing pagination"""
        return (
            button
            if isinstance(button, InlineKeyboardButton)
            else InlineKeyboardButton(**button)
        )

    def _build_pagination_buttons(self, builder: InlineKeyboardBuilder):
        if self.paginator_exists:
            pagination_buttons: List[InlineKeyboardButton] = []
            if self.current_page_index > self.first_page_index:
                pagination_buttons.append(
                    InlineKeyboardButton(
                        text="⏪",
                        callback_data=f"{self.pagination_key}|{self.first_page_index}",
                    ),
                )
                pagination_buttons.append(
                    InlineKeyboardButton(
                        text="⬅️",
                        callback_data=f"{self.pagination_key}|{self.current_page_index - 1}",
                    ),
                )

            pagination_buttons.append(
                InlineKeyboardButton(
                    text=str(self.current_page_index),
                    callback_data="pass",
                )
            )
            if self.current_page_index < self.last_page_index:
                pagination_buttons.append(
                    InlineKeyboardButton(
                        text="➡️",
                        callback_data=f"{self.pagination_key}|{self.current_page_index + 1}",
                    ),
                )
                pagination_buttons.append(
                    InlineKeyboardButton(
                        text="⏩",
                        callback_data=f"{self.pagination_key}|{self.last_page_index}",
                    ),
                )
            builder.row(*pagination_buttons)
        if self.additional_buttons:
            for button_row in self.additional_buttons:
                builder.row(*[self._format_button(button) for button in button_row])

    @property
    def _last_page_index(self) -> int:
        return ceil(len(self.data) / self.per_page)
