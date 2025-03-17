from typing import NoReturn

from asgiref.typing import (
    LifespanShutdownCompleteEvent,
    LifespanShutdownEvent,
    LifespanShutdownFailedEvent,
    LifespanStartupCompleteEvent,
    LifespanStartupEvent,
    LifespanStartupFailedEvent,
)
from channels.consumer import AsyncConsumer, StopConsumer


class LifespanConsumer(AsyncConsumer):  # type: ignore[misc]
    async def lifespan_startup(self, message: LifespanStartupEvent) -> None:
        try:
            pass
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
            pass
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
