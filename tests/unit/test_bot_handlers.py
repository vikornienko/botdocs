from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest


@pytest.mark.asyncio
async def test_command_start_handler_answers() -> None:
    import bot as bot_module  # noqa: PLC0415

    message = SimpleNamespace(answer=AsyncMock())

    await bot_module.command_start_handler(message)  # type: ignore[arg-type]

    message.answer.assert_awaited_once_with("Hello! I'm a bot created with aiogram.")


@pytest.mark.asyncio
async def test_main_creates_bot_and_starts_polling(mocker: pytest.MockFixture) -> None:
    import bot as bot_module  # noqa: PLC0415

    mocker.patch.object(bot_module, "config", return_value="123456789:" + ("A" * 35))

    bot_instance = object()
    bot_ctor = mocker.patch.object(
        bot_module, "Bot", autospec=True, return_value=bot_instance
    )

    start_polling_mock = AsyncMock()
    mocker.patch.object(bot_module.dp, "start_polling", start_polling_mock)

    await bot_module.main()

    bot_ctor.assert_called_once()
    assert bot_ctor.call_args.kwargs["token"].startswith("123456789:")

    start_polling_mock.assert_awaited_once_with(bot_instance)
