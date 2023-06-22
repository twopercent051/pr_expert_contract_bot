from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram import F, Router
from aiogram.filters.state import StateFilter

from create_bot import bot
from tgbot.filters.admin import AdminFilter
from tgbot.keyboards.inline import InlineKeyboard as inline_kb
from tgbot.misc.states import AdminFSM
from tgbot.models.redis_connector import RedisConnector as rds

router = Router()
router.message.filter(AdminFilter())

