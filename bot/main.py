import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode, setup_dialogs


from options import BOT_TOKEN
from database import db_manager
from states import MainDialog
from windows import main_dialog


async def set_commands(bot: Bot):
    commands = [BotCommand(command="/start", description="Запустить бота")]
    await bot.set_my_commands(commands)

# Обработчик для команды /start
async def cmd_start(message: types.Message, dialog_manager: DialogManager):
    chat_id = message.chat.id
    for i in range(10):
        try:
            await message.bot.delete_message(chat_id, message.message_id - i)
        except Exception:
            continue

    await dialog_manager.start(MainDialog.start, mode=StartMode.RESET_STACK)


async def main():
    print("Bot is starting...")
    db_manager.init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    setup_dialogs(dp)
    dp.include_router(main_dialog)

    # Регистрация команд
    dp.message.register(cmd_start, Command(commands="start"))

    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())