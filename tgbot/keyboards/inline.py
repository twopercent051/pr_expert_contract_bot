from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class InlineKeyboard:

    @classmethod
    def home_kb(cls):
        keyboard = [[InlineKeyboardButton(text="🏡 Домой", callback_data="home")]]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def templ_type_kb(cls, action: str):
        keyboard = [
            [InlineKeyboardButton(text="Аудит", callback_data=f"{action}:audit")],
            [InlineKeyboardButton(text="Оптима", callback_data=f"{action}:optima")],
            [InlineKeyboardButton(text="Премиум", callback_data=f"{action}:premium")],
            [InlineKeyboardButton(text="Стандарт", callback_data=f"{action}:standard")],
            [InlineKeyboardButton(text="Ведение рекламы", callback_data=f"{action}:marketing")],
            [InlineKeyboardButton(text="Разовая", callback_data=f"{action}:razovaya")],
            [InlineKeyboardButton(text="Кластеризация", callback_data=f"{action}:klasterizaciya")],
        ]
        if action == "edit":
            keyboard.append([InlineKeyboardButton(text="🏡 Домой", callback_data="home")])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)


class AdminInlineKeyboard(InlineKeyboard):

    @classmethod
    def main_menu_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text="🛠 Редактировать шаблон", callback_data="edit_template")],
            [InlineKeyboardButton(text="📝 Новый договор", callback_data="get_contract")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)


class UserInlineKeyboard(InlineKeyboard):

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


