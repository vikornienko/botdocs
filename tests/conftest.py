from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from aiogram import Bot, Dispatcher
from aiogram.client.session.base import BaseSession
import pytest

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from aiogram.methods import TelegramMethod

TEST_BOT_TOKEN = "123456789:" + ("A" * 35)


class DummySession(BaseSession):
    """Session that records calls without making HTTP requests."""

    def __init__(self) -> None:
        super().__init__()
        self.calls: list[TelegramMethod[Any]] = []

    async def close(self) -> None:
        return None

    async def make_request(
        self,
        bot: Bot,
        method: TelegramMethod[Any],
        timeout: int | None = None,  # noqa: ASYNC109
    ) -> Any:
        self.calls.append(method)
        return None

    async def stream_content(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        timeout: int = 30,  # noqa: ASYNC109
        chunk_size: int = 65536,
        raise_for_status: bool = True,
    ) -> AsyncGenerator[bytes]:
        if False:  # pragma: no cover
            yield b""
        return


@dataclass(frozen=True, slots=True)
class TgIds:
    chat_id: int = 1001
    user_id: int = 2002


@pytest.fixture
def tg_ids() -> TgIds:
    return TgIds()


@pytest.fixture
def dummy_session() -> DummySession:
    return DummySession()


@pytest.fixture
async def bot(dummy_session: DummySession) -> AsyncGenerator[Bot]:
    b = Bot(token=TEST_BOT_TOKEN, session=dummy_session)
    try:
        yield b
    finally:
        await b.session.close()


@pytest.fixture
def test_dispatcher() -> Dispatcher:
    import bot as bot_module  # noqa: PLC0415

    router = bot_module.router
    router._parent_router = None

    dp = Dispatcher()
    dp.include_router(router)
    return dp


def _raw_message_update(
    *,
    update_id: int,
    chat_id: int,
    user_id: int,
    text: str,
    is_command: bool,
) -> dict[str, Any]:
    message: dict[str, Any] = {
        "message_id": 10 + update_id,
        "date": 1_700_000_000,
        "chat": {"id": chat_id, "type": "private"},
        "from": {"id": user_id, "is_bot": False, "first_name": "Test"},
        "text": text,
    }
    if is_command:
        message["entities"] = [
            {"type": "bot_command", "offset": 0, "length": len(text)}
        ]

    return {"update_id": update_id, "message": message}


@pytest.fixture
def raw_update_start(tg_ids: TgIds) -> dict[str, Any]:
    return _raw_message_update(
        update_id=1,
        chat_id=tg_ids.chat_id,
        user_id=tg_ids.user_id,
        text="/start",
        is_command=True,
    )


@pytest.fixture
def raw_update_plain_text(tg_ids: TgIds) -> dict[str, Any]:
    return _raw_message_update(
        update_id=2,
        chat_id=tg_ids.chat_id,
        user_id=tg_ids.user_id,
        text="hello",
        is_command=False,
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    for item in items:
        p = Path(str(item.fspath))
        if "tests" in p.parts and "unit" in p.parts:
            item.add_marker(pytest.mark.unit)
        if "tests" in p.parts and "integration" in p.parts:
            item.add_marker(pytest.mark.integration)
