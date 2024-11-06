import logging
import sys
import asyncio

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from os import getenv

load_dotenv()
TELEGRAM_API_KEY = getenv('TELEGRAM_API_KEY')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_API_KEY)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` or  `/help `command
    """
    await message.reply("Hi\nI am Echo Bot!\nPowered by Bappy.")

@dp.message()
async def echo(message: Message) -> None:
    """
    This will retrun echo
    """
    await message.answer(message.text)

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TELEGRAM_API_KEY, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())