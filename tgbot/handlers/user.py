import os

from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from create_bot import bot
from tgbot.keyboards.inline import UserInlineKeyboard as inline_kb
from tgbot.misc.states import UserFSM
from tgbot.services.render import data_to_json

router = Router()


async def template_start(user_id: int | str):
    text = "Выберите тип договора"
    kb = inline_kb.templ_type_kb(action="create")
    await bot.send_message(chat_id=user_id, text=text, reply_markup=kb)


@router.message(Command('start'))
async def template_type(message: Message):
    await template_start(user_id=message.from_user.id)


@router.callback_query(F.data == "get_contract")
@router.callback_query(F.data == "home")
async def template_type(callback: CallbackQuery):
    await template_start(user_id=callback.from_user.id)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data.split(":")[0] == "create")
async def create_template(callback: CallbackQuery, state: FSMContext):
    template = callback.data.split(":")[1]
    await state.update_data(template=template)
    text = "👇 Нужно скопировать текст ниже, отредактировать и отправить ответным сообщением"
    await callback.message.answer(text)
    text = [
        "Номер сделки ||",
        "Название ООО ||",
        "Полное ФИО (род.п)||",
        "Краткое ФИО ||",
        "Сайт ||",
        "Конт. лицо ||",
        "Тлф конт. лица ||",
        "Email конт. лица ||",
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
    if template in ["standard", "optima", "premium"]:
        text.append("Регион ||")
    if template == "marketing":
        text.extend(["ОГРН ||", "ОКВЭД ||", "Регион ||"])
    if template == "razovaya":
        text.extend(["Срок работ ||", "Регион ||"])
    if template == "klasterizaciya":
        text.extend(["Срок работ ||", "Цена запроса ||", "Тематики ||"])
        text.append("\n*Тематики указываются через запятую")
    text = '\n'.join(text)
    kb = inline_kb.home_kb()
    await state.set_state(UserFSM.template)
    await callback.message.answer(f"<code>{text}</code>", reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.message(F.text, UserFSM.template)
async def rendering(message: Message, state: FSMContext):
    state_data = await state.get_data()
    template = state_data["template"]
    file_name = data_to_json(template=template, data_str=message.text)
    if not file_name:
        await message.answer("⚠️ Проверьте введённые данные")
        return
    await state.set_state(UserFSM.home)
    file_path = f'{os.getcwd()}/result.docx'
    file = FSInputFile(path=file_path, filename=f"{file_name}.docx")
    kb = inline_kb.home_kb()
    await bot.send_document(chat_id=message.from_user.id, document=file, reply_markup=kb)
    os.remove(file_path)

