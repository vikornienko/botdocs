"""Integration tests for /start handler."""

from aiogram import Dispatcher
from aiogram_test_framework import TestClient as Client
import pytest

from handlers.start import router as start_router

pytestmark = pytest.mark.integration


def setup_dispatcher(bot, dispatcher: Dispatcher) -> None:
    """Configure dispatcher with handlers."""
    dispatcher.include_router(start_router)


async def test_start_command() -> None:
    """/start command sends welcome message."""
    client = await Client.create(
        bot_token="123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh",
        bot_id=123456789,
        bot_username="test_bot",
        bot_first_name="Test Bot",
        setup_dispatcher_func=setup_dispatcher,
    )
    try:
        user = client.create_user()
        await user.send_command("start")
        assert user.has_received_message_containing("Привет")
    finally:
        await client.close()
