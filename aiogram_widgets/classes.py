from typing import List
from aiogram.types import InlineKeyboardButton

from aiogram_widgets.enums import AdditionalButtonPlacesEnum


class AdditionalButtonsRow:
    buttons: List[InlineKeyboardButton]
    buttons_place: AdditionalButtonPlacesEnum = AdditionalButtonPlacesEnum.TOP
