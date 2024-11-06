from dotenv import load_dotenv
import logging
import sys
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from openai import OpenAI

load_dotenv()
client = OpenAI()

client.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_API_KEY")

model_name = "gpt-4o-mini"

class Reference:
    '''
    A class to store previously response from the openai API
    '''

    def __init__(self) -> None:
        self.response = ""

reference = Reference()
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

def clear_past():
    """A function to clear the previous conversation and context.
    """
    reference.response = ""

@dp.message(CommandStart())
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` or  `/help `command
    """
    await message.reply("Hi\nI am Tele Bot!\Created by Bappy. How can i assist you?")
    
@dp.message(Command("help"))
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` or  `/help `command
    """
    help_command = """
    Hi There, I'm Telegram bot created by Bappy! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)
    
@dp.message()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")
    
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": message.text
            }
        ]
    )
    
    reference.response = response.choices[0].message.content
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)
    
async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    
# CONTINUE AT 6:36