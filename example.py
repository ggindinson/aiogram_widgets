import asyncio
import logging
from typing import Dict, List

from aiogram import Bot, Dispatcher, F, Router
from aiogram.fsm.storage.memory import MemoryStorage as ms
from aiogram.types import (
    BotCommand,
    BotCommandScopeAllPrivateChats,
    InlineKeyboardButton,
    Message,
)

from aiogram_widgets.pagination import KeyboardPaginator, TextPaginator

BOT_TOKEN = "5728066977:AAFBB99HeUgc7B291PPTvkJs5F1NUYLYN1s"
dp = Dispatcher(storage=ms())
bot = Bot(BOT_TOKEN, parse_mode="HTML")
test_router = Router(name="test_router")

commands: Dict[str, str] = {
    "keyboard_pagination": "Simple kb pagination",
    "kb_additional_buttons": "Kb pagination with additional buttons",
    "kb_custom_pagination": "Kb pagination with custom pagination buttons",
    "text_pagination": "Simple text pagination",
    "text_join": "Text pagination with custom join",
}


# Simple keyboard pagination
@test_router.message(F.text == "/keyboard_pagination")
async def keyboard_pagination(message: Message):
    buttons: List[InlineKeyboardButton] = [
        InlineKeyboardButton(text=f"Button {i}", callback_data=f"button_{i}")
        for i in range(1, 1002)
    ]

    paginator = KeyboardPaginator(
        data=buttons,
        router=test_router,
        per_page=7,
        per_row=(1, 2),
    )

    await message.answer(text="Keyboard pagination", reply_markup=paginator.as_markup())


# Keyboard pagination with additional buttons


@test_router.message(F.text == "/kb_additional_buttons")
async def keyboard_pagination_with_additional_buttons(message: Message):
    buttons = [
        InlineKeyboardButton(text=f"Button {i}", callback_data=f"button_{i}")
        for i in range(1, 1001)
    ]
    additional_buttons = [
        [
            InlineKeyboardButton(text="Go back 🔙", callback_data="go_back"),
        ],
    ]

    paginator = KeyboardPaginator(
        data=buttons,
        router=test_router,
        additional_buttons=additional_buttons,
        per_page=20,
        per_row=2,
    )

    await message.answer(
        text="Keyboard pagination with additional buttons",
        reply_markup=paginator.as_markup(),
    )


# Keyboard pagination with custom pagination buttons (Same with text pagination)
@test_router.message(F.text == "/kb_custom_pagination")
async def kb_custom_pagination(message: Message):
    buttons = [
        InlineKeyboardButton(text=f"Button {i}", callback_data=f"button_{i}")
        for i in range(1, 1001)
    ]
    pagination_buttons = [None, "<-", "->", None]

    paginator = KeyboardPaginator(
        data=buttons,
        router=test_router,
        pagination_buttons=pagination_buttons,
    )

    await message.answer(
        text="Keyboard pagination with custom pagination buttons",
        reply_markup=paginator.as_markup(),
    )


# Simple text pagination
from aiogram_widgets.pagination import TextPaginator


@test_router.message(F.text == "/text_pagination")
async def text_pagination(message: Message):
    text_data = [f"I am string number {i}" for i in range(1, 1001)]

    paginator = TextPaginator(
        data=text_data,
        router=test_router,
    )

    current_text_chunk, reply_markup = paginator.current_message_data

    await message.answer(
        text=current_text_chunk,
        reply_markup=reply_markup,
    )


### Text pagination with custom join


@test_router.message(F.text == "/text_join")
async def text_custom_join(message: Message):
    text_data = [f"I am string number {i}" for i in range(1, 1001)]

    paginator = TextPaginator(
        data=text_data,
        router=test_router,
        join_symbol="\n\n",
    )
    current_text_chunk, reply_markup = paginator.current_message_data

    await message.answer(
        text=current_text_chunk,
        reply_markup=reply_markup,
    )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    formatted_commands = [
        BotCommand(command=comm, description=desc) for comm, desc in commands.items()
    ]
    await bot.set_my_commands(
        commands=formatted_commands,
        scope=BotCommandScopeAllPrivateChats(type="all_private_chats"),
    )
    dp.include_router(test_router)
    await dp.start_polling(bot, allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
