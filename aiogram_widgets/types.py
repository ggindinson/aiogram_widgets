from typing import Annotated, Any, Dict, List, Optional, TypeAlias

import aiogram
from aiogram.types import InlineKeyboardButton

if aiogram.__version__ >= "3.0.0b8":
    from pydantic.v1 import Field
else:
    from pydantic import Field

from aiogram_widgets.enums import InlineKeyboardLimits

AdditionalButtonsType: TypeAlias = List[
    List[InlineKeyboardButton] | List[Dict[str, Any]]
]
PerRowType: TypeAlias = Annotated[
    int, Field(ge=1, le=InlineKeyboardLimits.MAX_ROW_LENGTH)
]
PerPageType: TypeAlias = Annotated[
    int, Field(ge=1, le=InlineKeyboardLimits.MAX_PAGE_ELEMENTS)
]
PaginationKeyType: TypeAlias = Annotated[str, Field(min_length=1)]
ButtonType: TypeAlias = InlineKeyboardButton | Dict[str, Any]
PaginationButtonsType: TypeAlias = Annotated[
    List[Optional[Annotated[str, Field(min_length=1)]]], Field(min_items=4, max_items=4)
]
