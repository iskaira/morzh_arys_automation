import sys
import threading
from concurrent.futures import ProcessPoolExecutor

from PyQt5 import QtWidgets
import aiogram.utils
import aiogram.utils.markdown as md
from aiogram import Bot, executor, Dispatcher, types
import aiogram.types
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

API_TOKEN = '1805835451:AAEHb_HLk9FkHiiVdMqgrfAeVLo-9LZefCE'
CHAT_ID = 295091909
# For example use simple Bot, Bot should be a subclass of Bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

class ChatWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.text_edit = QtWidgets.QTextEdit(self)
        self.text_edit.setReadOnly(True)

        self.line_edit = QtWidgets.QTextEdit(self)

        send_button = QtWidgets.QPushButton('Send', self)
        send_button.clicked.connect(self.send_message)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.line_edit)
        layout.addWidget(send_button)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def send_message(self):
        message = self.line_edit.toPlainText()
        print('a')
        _thread = threading.Thread(target=asyncio.run, args=(self.send_message_async(message),))
        _thread.start()
        # loop.run_until_complete()
        # self.send_message_async(message))
        # asyncio.run_coroutine_threadsafe(, loop=loop)
        print('b')

    async def send_message_async(self, message):
        print('asda')
        await bot.send_message(chat_id=CHAT_ID, text=message)
        self.text_edit.append(message)
        self.line_edit.clear()


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


# async def start_bot_polling(bot, loop):
#     await
#     await bot.wait_closed()

def run_qt():
    print('here')
    app = QtWidgets.QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    # loop = asyncio.new_event_loop()
    print('here2')
    app.exec()
    # loop.run_forever()
    # sys.exit(app.exec_())


# async def main():

    # loop = asyncio.new_event_loop()
    # executor2 = ProcessPoolExecutor(2)
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # await executor.start_polling(dispatcher=dp, loop=loop)
    # await asyncio.gather(run_qt, executor.start_polling(dp, loop=loop))


async def on_startup(x):
    pass
    # asyncio.create_task(run_qt())


if __name__ == '__main__':
    t = threading.Thread(target=run_qt)
    t.start()
    executor.start_polling(dispatcher=dp)




