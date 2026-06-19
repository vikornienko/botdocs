"""Telegram bot entry point and configuration.

This module initializes the aiogram Bot and Dispatcher,
registers routers, and starts the long-polling process.
It serves as the main entry point for running the application.
"""

import asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message
from decouple import config

# Initializes router and dispatcher
router = Router()

dp = Dispatcher()
dp.include_router(router)


# Command handler
@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    """Handles the `/start` command.

    This handler is triggered when a user initiates a conversation
    with the bot or restarts it using the `/start` command.
    It sends a basic greeting message back to the user.

    Args:
        message (Message): The incoming Telegram message object
            containing user data and command text.
    """
    await message.answer("Hello! I'm a bot created with aiogram.")


# Run the bot
async def main() -> None:
    """Initializes and starts the Telegram bot.

    Retrieves the bot token from the environment variables using
    `python-decouple`, creates an aiogram Bot instance, and starts
    the Dispatcher's long-polling process to listen for incoming updates.
    """
    bot = Bot(token=config("BOT_TOKEN"))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
