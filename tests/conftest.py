"""Shared test fixtures."""

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import pytest


@pytest.fixture
def bot() -> Bot:
    """Create a Bot instance with a test token."""
    return Bot(
        token="123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh",
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


@pytest.fixture
def dp() -> Dispatcher:
    """Create a Dispatcher instance."""
    return Dispatcher()
