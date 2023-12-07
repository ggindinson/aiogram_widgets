from enum import IntEnum, StrEnum


class InlineKeyboardLimitsEnum(IntEnum):
    MAX_ROW_LENGTH = 8
    MAX_PAGE_ELEMENTS = 100


class AdditionalButtonPlacesEnum(StrEnum):
    TOP = "top"
    BOTTOM = "bottom"
