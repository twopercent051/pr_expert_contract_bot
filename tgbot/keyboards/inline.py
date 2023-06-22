from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class InlineKeyboard:

    @classmethod
    def templ_type_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text="Аудит", callback_data="template:audit")],
            [InlineKeyboardButton(text="Оптима", callback_data="template:optima")],
            [InlineKeyboardButton(text="Премиум", callback_data="template:premium")],
            [InlineKeyboardButton(text="Стандарт", callback_data="template:standard")],
            [InlineKeyboardButton(text="Ведение рекламы", callback_data="template:marketing")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def partner_type_kb(cls):
        keyboard = [
            [
                InlineKeyboardButton(text="ООО", callback_data="partner:ooo"),
                InlineKeyboardButton(text="ИП", callback_data="partner:ip"),
                InlineKeyboardButton(text="ФЛ", callback_data="partner:fl"),
            ],
            [InlineKeyboardButton(text="🏡 Домой", callback_data="home")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def home_kb(cls):
        keyboard = [[InlineKeyboardButton(text="🏡 Домой", callback_data="home")]]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
