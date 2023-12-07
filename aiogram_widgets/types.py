from typing import Annotated, Any, Dict, List, Optional, Tuple, TypeAlias

import aiogram
from aiogram.types import InlineKeyboardButton

from aiogram_widgets.enums import InlineKeyboardLimitsEnum

if aiogram.__version__ >= "3.0.0b8":
    from pydantic.v1 import Field
else:
    from pydantic import Field


AdditionalButtonsType: TypeAlias = List[
    List[InlineKeyboardButton] | List[Dict[str, Any]]
]
PerRowType: TypeAlias = Annotated[
    int, Field(ge=1, le=InlineKeyboardLimitsEnum.MAX_ROW_LENGTH)
]
PerPageIntType: TypeAlias = Annotated[
    int, Field(ge=1, le=InlineKeyboardLimitsEnum.MAX_PAGE_ELEMENTS)
]
PerPageIntTupleType: TypeAlias = Annotated[
    Tuple[int, int], Field(min_items=1, max_items=2)
]
PaginationKeyType: TypeAlias = Annotated[str, Field(min_length=1)]
ButtonType: TypeAlias = InlineKeyboardButton | Dict[str, Any]
PaginationButtonsType: TypeAlias = Annotated[
    List[Optional[Annotated[str, Field(min_length=1)]]], Field(min_items=4, max_items=4)
]
