
## aiogram_widgets


Create most popular widgets for aiogram 3 in few code lines 

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/) 
![PyPI](https://img.shields.io/pypi/v/aiogram_widgets)
![PyPI - Downloads](https://img.shields.io/pypi/dm/aiogram_widgets)

## Installation

Pip:

```bash
pip install aiogram_widgets
```

Poetry:

```bash
poetry add aiogram_widgets
```
## Examples

### Simple keyboard pagination

```python
from aiogram_widgets.pagination import KeyboardPaginator

@router.message(F.text == "/keyboard_pagination")
async def keyboard_pagination(message: Message):
    buttons = [
        InlineKeyboardButton(text=f"Button {i}", callback_data=f"button_{i}")
        for i in range(1, 1001)
    ]
    paginator = KeyboardPaginator(
        data=buttons,
        router=router,  
        pagination_key="test_kb_paginator",
        per_page=20,
        row_witdh=2
    )


    await message.answer(text="Keyboard pagination", reply_markup=paginator.as_markup())

```
### Keyboard pagination with additional buttons
```python
from aiogram_widgets.pagination import KeyboardPaginator

@router.message(F.text == "/keyboard_pagination_with_additional_buttons")
async def keyboard_pagination_with_additional_buttons(message: Message):
    buttons = [
        InlineKeyboardButton(text=f"Button {i}", callback_data=f"button_{i}")
        for i in range(1, 1001)
    ]
    additional_buttons = [
        InlineKeyboardButton(text="Go back 🔙", callback_data="go_back")
    ]
    
    paginator = KeyboardPaginator(
        data=buttons,
        router=router,
        pagination_key="test_kb_paginator",
        additional_buttons=additional_buttons,    
        per_page=20, 
        row_witdh=2
    )

    await message.answer(
        text="Keyboard pagination with additional buttons",
        reply_markup=paginator.as_markup(),
    )

```
### Simple text pagination
```python
from aiogram_widgets.pagination import TextPaginator


@router.message(F.text == "/text_pagination")
async def text_pagination(message: Message):
    text_data = [
        f"I am string number {i}"
        for i in range(1, 1001)
    ]
    
    paginator = TextPaginator(
        data=text_data,
        router=router,
        pagination_key="test_text_paginator",
    )

    current_text_chunk, reply_markup = paginator.current_message_data

    await message.answer(
        text=current_text_chunk,
        reply_markup=reply_markup,
    )

```

### Text pagination with additional buttons 
``` python
@router.message(F.text == "/text_pagination_with_additional_buttons")
async def text_pagination_with_additional_buttons(message: Message):
    text_data = [f"I am string number {i}" for i in range(1, 1001)]
    additional_buttons = [
        InlineKeyboardButton(text="Go back 🔙", callback_data="go_back")
    ]

    paginator = TextPaginator(
        data=text_data,
        router=router,
        pagination_key="test_text_paginator",
        additional_buttons=additional_buttons,
    )

    current_text_chunk, reply_markup = paginator.current_message_data

    await message.answer(
        text=current_text_chunk,
        reply_markup=reply_markup,
    )

```

### Text pagination with custom join

```python
@router.message(F.text == "/text_pagination_with_custom_join")
async def text_pagination_with_custom_join(message: Message):
    text_data = [f"I am string number {i}" for i in range(1, 1001)]

    paginator = TextPaginator(
        data=text_data,
        router=router,
        pagination_key="test_text_paginator",
        additional_buttons=additional_buttons,
        data_joiner="\n\n",
    )
    current_text_chunk, reply_markup = paginator.current_message_data

    await message.answer(
        text=current_text_chunk,
        reply_markup=reply_markup,
    )

```
## 🔗 Links
[![](https://img.shields.io/github/stars/ggindinson?label=GitHub%20Repo&style=social)](https://github.com/ggindinson/aiogram_widgets)

[![Latest Version](https://pypip.in/version/aiogram_widgets/badge.svg)](https://pypi.python.org/pypi/aiogram_widgets/)

## Feedback

I would be very pleased for a star ⭐️
