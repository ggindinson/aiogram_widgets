

## aiogram_widgets


Create most popular widgets for aiogram 3x in a few code lines 

## 🔗 Links

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/) 
[![Github](https://img.shields.io/github/stars/ggindinson?label=GitHub%20Repo&style=social)](https://github.com/ggindinson/aiogram_widgets)
[![PyPI - Package](https://img.shields.io/pypi/v/aiogram_widgets)](https://pypi.org/project/aiogram-widgets/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/aiogram_widgets)](https://pypistats.org/packages/aiogram-widgets)

# Features

- Fully customizable widgets 
- Stateless
- Automatic handling
- Supports aiogram ^3.0.0b1


# Roadmap

- Checkboxes and multiselect

- Calendar

- Aiogram 2x support


# Changelog

`Version 1.2.0:`
- Custom pagination keyboard support
- Aiogram 3.0.0b8 support
- README with more examples
- Live bot example with source code
- Better types naming


## Installation

Pip:

```bash
pip install aiogram_widgets
```

Poetry:

```bash
poetry add aiogram_widgets
```


# ![](https://raw.githubusercontent.com/ggindinson/aiogram_widgets/main/demo.gif) 🤖 [Bot example](https://t.me/aiogram_widgets_demo_bot) | [Bot source code](https://github.com/ggindinson/aiogram_widgets/blob/main/example.py) ⚙️





# Usage/Examples



## Simple keyboard pagination

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
        pagination_key="test_kb_paginator",
        per_page=20,
        per_row=2
    )


    await message.answer(text="Keyboard pagination", reply_markup=paginator.as_markup())

```
## Keyboard pagination with additional buttons (Same with text pagination)
```python
from aiogram_widgets.pagination import KeyboardPaginator

@router.message(F.text == "/kb_additional_buttons")
async def kb_additional_buttons(message: Message):
    buttons = [
        InlineKeyboardButton(text=f"Button {i}", callback_data=f"button_{i}")
        for i in range(1, 1001)
    ]
    additional_buttons = [
        [
            InlineKeyboardButton(text="Go back 🔙", callback_data="go_back"),
        ]
    ]
    
    paginator = KeyboardPaginator(
        data=buttons,
        pagination_key="test_kb_paginator",
        additional_buttons=additional_buttons,    
        per_page=20, 
        per_row=2
    )

    await message.answer(
        text="Keyboard pagination with additional buttons",
        reply_markup=paginator.as_markup(),
    )

```
## Keyboard pagination with custom pagination buttons (Same with text pagination)
``` python
@router.message(F.text == "/kb_custom_pagination")
async def kb_custom_pagination(message: Message):
    text_data = [f"I am string number {i}" for i in range(1, 1001)]
    pagination_buttons = [
        None, "<-", "->", None
    ]

    paginator = TextPaginator(
        data=text_data,
        pagination_key="test_text_paginator",
        pagination_buttons=pagination_buttons,
    )

    current_text_chunk, reply_markup = paginator.current_message_data

    await message.answer(
        text=current_text_chunk,
        reply_markup=reply_markup,
    )

```

## Simple text pagination
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
        pagination_key="test_text_paginator",
    )

    current_text_chunk, reply_markup = paginator.current_message_data

    await message.answer(
        text=current_text_chunk,
        reply_markup=reply_markup,
    )

```


## Text pagination with custom join

```python
@router.message(F.text == "/text_join")
async def text_custom_join(message: Message):
    text_data = [f"I am string number {i}" for i in range(1, 1001)]

    paginator = TextPaginator(
        data=text_data,
        pagination_key="test_text_paginator",
        data_joiner="\n\n",
    )
    current_text_chunk, reply_markup = paginator.current_message_data

    await message.answer(
        text=current_text_chunk,
        reply_markup=reply_markup,
    )

```

# Feedback

I would be very pleased for a star ⭐️
