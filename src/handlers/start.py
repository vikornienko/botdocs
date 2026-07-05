"""Handler for /start command."""

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Send a welcome message when the command /start is issued."""
    await message.answer("Привет! Я doc-бот. Напиши /help, чтобы узнать, что я умею.")
