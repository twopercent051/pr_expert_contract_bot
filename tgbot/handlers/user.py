import os

from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from create_bot import bot
from tgbot.keyboards.inline import InlineKeyboard as inline_kb
from tgbot.misc.states import UserFSM
from tgbot.services.render import data_to_json

router = Router()


@router.message(Command('start'))
async def template_type(message: Message):
    text = "Привет, колбаса. Выбери-ка тип договора"
    kb = inline_kb.templ_type_kb()
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data == "home")
async def template_type(callback: CallbackQuery):
    text = "Привет, колбаса. Выбери-ка тип договора"
    kb = inline_kb.templ_type_kb()
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


# @router.callback_query(F.data.split(":")[0] == "template")
# async def partner_type(callback: CallbackQuery, state: FSMContext):
#     template = callback.data.split(":")[1]
#     await state.update_data(template=template)
#     text = "А теперь тип контрагента, bitte"
#     kb = inline_kb.partner_type_kb()
#     await callback.message.answer(text, reply_markup=kb)
#     await bot.answer_callback_query(callback.id)


@router.callback_query(F.data.split(":")[0] == "template")
async def create_template(callback: CallbackQuery, state: FSMContext):
    template = callback.data.split(":")[1]
    await state.update_data(template=template)
    text = "Нужно скопировать текст ниже и отредактировать. Ненужные значения можно просто пропустить"
    await callback.message.answer(text)
    text = [
        "Номер сделки ||",
        "Название ООО ||",
        "Полное ФИО (род.п)||",
        "Краткое ФИО ||",
        "Сайт ||",
        "Решала ||",
        "Тлф решалы ||",
        "Email решалы ||",
        "Сумма сделки ||",
        "Юр. адрес ||",
        "Почтовый адрес ||",
        "ИНН ||",
        "КПП ||",
        "Р. счёт ||",
        "Банк ||",
        "Кор. счёт ||",
        "БИК ||",
    ]
    kb = inline_kb.home_kb()
    text = '\n'.join(text)
    await state.set_state(UserFSM.template)
    await callback.message.answer(f"<code>{text}</code>", reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.message(F.text, UserFSM.template)
async def rendering(message: Message, state: FSMContext):
    state_data = await state.get_data()
    template = state_data["template"]
    # partner = state_data["partner"]
    data_to_json(template=template, data_str=message.text)
    file = FSInputFile(path=f'{os.getcwd()}/result.docx', filename="result.docx")
    kb = inline_kb.home_kb()
    await bot.send_document(chat_id=message.from_user.id, document=file, reply_markup=kb)
