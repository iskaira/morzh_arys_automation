from aiogram.dispatcher.filters.state import State, StatesGroup

LIST_DIRECTORY = "LIST_DIRECTORY"
IN_DIRECTORY = "IN_DIRECTORY"
START = "START"

class MainMenu(StatesGroup):
    START = State()


class AdminPC(StatesGroup):
    LIST_DIRECTORY = State(LIST_DIRECTORY)
    IN_DIRECTORY = State(IN_DIRECTORY)
