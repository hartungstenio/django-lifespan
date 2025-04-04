import asyncio
from collections import ChainMap
from collections.abc import MutableMapping, Sequence
from contextlib import AsyncExitStack
from typing import Any, NoReturn

from asgiref.typing import (
    LifespanScope,
    LifespanShutdownCompleteEvent,
    LifespanShutdownEvent,
    LifespanShutdownFailedEvent,
    LifespanStartupCompleteEvent,
    LifespanStartupEvent,
    LifespanStartupFailedEvent,
)
from channels.consumer import AsyncConsumer, StopConsumer
from django.utils.module_loading import autodiscover_modules

from .registry import LifespanFactory, _state_registry


class LifespanConsumer(AsyncConsumer):  # type: ignore[misc]
    async def _state(
        self, names: tuple[str, ...], factory: LifespanFactory
    ) -> MutableMapping[str, Any]:
        values = await self._exit_stack.enter_async_context(factory())
        if not isinstance(values, Sequence):
            values = (values,)

        return dict(zip(names, values, strict=True))

    async def lifespan_startup(self, message: LifespanStartupEvent) -> None:
        self._exit_stack = AsyncExitStack()
        try:
            autodiscover_modules("lifespan")

            if _state_registry:
                scope: LifespanScope = self.scope
                if "state" not in scope:
                    raise RuntimeError("Server does not support lifespan state.")

                lifespan_tasks: list[asyncio.Task[MutableMapping[str, Any]]] = [
                    asyncio.create_task(self._state(names, factory))
                    for names, factory in _state_registry.items()
                ]
                states: list[MutableMapping[str, Any]] = await asyncio.gather(
                    *lifespan_tasks
                )
                scope["state"].update(ChainMap(*states))

        except Exception as exc:
            await self.send(
                LifespanStartupFailedEvent(
                    type="lifespan.startup.failed",
                    message=str(exc),
                )
            )
        else:
            await self.send(
                LifespanStartupCompleteEvent(type="lifespan.startup.complete")
            )

    async def lifespan_shutdown(self, message: LifespanShutdownEvent) -> NoReturn:
        try:
            if hasattr(self, "_exit_stack"):
                await self._exit_stack.aclose()
        except Exception as exc:
            await self.send(
                LifespanShutdownFailedEvent(
                    type="lifespan.shutdown.failed",
                    message=str(exc),
                )
            )
        else:
            await self.send(
                LifespanShutdownCompleteEvent(type="lifespan.shutdown.complete")
            )
        raise StopConsumer
