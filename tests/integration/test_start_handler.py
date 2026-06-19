from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.methods.send_message import SendMessage
import pytest

if TYPE_CHECKING:
    from tests.conftest import DummySession


@pytest.mark.asyncio
async def test_start_command_through_dispatcher_sends_message(
    bot,
    dummy_session: DummySession,
    test_dispatcher,
    raw_update_start: dict,
    tg_ids,
) -> None:
    await test_dispatcher.feed_raw_update(bot, raw_update_start)

    assert len(dummy_session.calls) == 1
    method = dummy_session.calls[0]

    assert isinstance(method, SendMessage)
    assert method.chat_id == tg_ids.chat_id
    assert method.text == "Hello! I'm a bot created with aiogram."


@pytest.mark.asyncio
async def test_non_command_text_is_ignored(
    bot,
    dummy_session: DummySession,
    test_dispatcher,
    raw_update_plain_text: dict,
) -> None:
    await test_dispatcher.feed_raw_update(bot, raw_update_plain_text)

    assert dummy_session.calls == []
