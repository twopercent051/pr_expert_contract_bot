from aiogram.fsm.state import State, StatesGroup


class AdminFSM(StatesGroup):
    home = State()


class UserFSM(StatesGroup):
    home = State()
    template = State()
