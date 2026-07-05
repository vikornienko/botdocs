"""Tests for bot creation and basic setup."""

from aiogram import Bot, Dispatcher
import pytest

from handlers.start import router as start_router

pytestmark = pytest.mark.unit

TEST_TOKEN = "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh"


def test_bot_creation(bot: Bot) -> None:
    """Bot instance is created with the test token."""
    assert bot.token == TEST_TOKEN


def test_dispatcher_creation(dp: Dispatcher) -> None:
    """Dispatcher instance is created."""
    assert isinstance(dp, Dispatcher)


def test_start_router_included(dp: Dispatcher) -> None:
    """Start router can be included in dispatcher."""
    dp.include_router(start_router)
    assert start_router in dp.sub_routers
