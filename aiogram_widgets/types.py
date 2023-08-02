from typing import Annotated, Any, Dict, List

from aiogram.types import InlineKeyboardButton
from pydantic import Field

from aiogram_widgets.enums import InlineKeyboardLimits

Additional_buttons_type = List[List[InlineKeyboardButton] | List[Dict[str, Any]]]
Per_row_type = Annotated[int, Field(ge=1, le=InlineKeyboardLimits.MAX_ROW_LENGTH)]
Per_page_type = Annotated[int, Field(ge=1, le=InlineKeyboardLimits.MAX_PAGE_ELEMENTS)]
Pagination_key = Annotated[str, Field(min_length=1)]
Button_type = InlineKeyboardButton | Dict[str, Any]
