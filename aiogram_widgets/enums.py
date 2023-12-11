import sys

if sys.version_info >= (3, 11):
    from enum import IntEnum

    class InlineKeyboardLimitsEnum(IntEnum):
        MAX_ROW_LENGTH = 8
        MAX_PAGE_ELEMENTS = 100

else:
    from enum import Enum

    class InlineKeyboardLimitsEnum(Enum):
        MAX_ROW_LENGTH = 8
        MAX_PAGE_ELEMENTS = 100
