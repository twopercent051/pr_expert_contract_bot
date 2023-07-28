import os

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram import F, Router
from aiogram.filters.state import StateFilter

from create_bot import bot, config
from tgbot.filters.admin import AdminFilter
from tgbot.keyboards.inline import AdminInlineKeyboard as inline_kb
from tgbot.misc.states import AdminFSM
from tgbot.models.redis_connector import RedisConnector as rds

router = Router()
router.message.filter(AdminFilter())
router.callback_query.filter(AdminFilter())


async def main_menu_render(user_id: int | str, start: bool):
    text = "Вы вошли как администратор" if start else "ГЛАВНОЕ МЕНЮ"
    kb = inline_kb.main_menu_kb()
    await bot.send_message(chat_id=user_id, text=text, reply_markup=kb)


@router.message(Command("start"))
async def main_block(message: Message, state: FSMContext):
    await main_menu_render(user_id=message.from_user.id, start=True)
    await state.set_state(AdminFSM.home)


@router.callback_query(F.data == "home")
async def main_block(callback: CallbackQuery, state: FSMContext):
    await main_menu_render(user_id=callback.from_user.id, start=False)
    await state.set_state(AdminFSM.home)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data == "edit_template")
async def main_block(callback: CallbackQuery):
    text = "Выберите тип договора"
    kb = inline_kb.templ_type_kb(action="edit")
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data.split(":")[0] == "edit")
async def main_block(callback: CallbackQuery, state: FSMContext):
    template = callback.data.split(":")[1]
    text = "Сейчас шаблон такой. Отредактируйте и загрузите в бота новый шаблон"
    kb = inline_kb.home_kb()
    await state.set_state(AdminFSM.template)
    await state.update_data(template=template)
    file = FSInputFile(path=f'{os.getcwd()}/templates/{template}_ooo.docx', filename=f"{template}_ooo.docx")
    await callback.message.answer_document(document=file, caption=text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.message(F.document, AdminFSM.template)
async def main_block(message: Message, state: FSMContext):
    state_data = await state.get_data()
    template = state_data["template"]
    file_name = f"{os.getcwd()}/templates/{template}_ooo.docx"
    await bot.download(file=message.document, destination=file_name)
    text = "Данные обновлены"
    kb = inline_kb.home_kb()
    await message.answer(text, reply_markup=kb)