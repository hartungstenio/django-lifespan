from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from typing import Any, TypeAlias

LifespanFactory: TypeAlias = Callable[[], AbstractAsyncContextManager[Any]]
_state_registry: dict[tuple[str, ...], LifespanFactory] = {}


def register_state(*state: str) -> Callable[[LifespanFactory], LifespanFactory]:
    def wrapper(factory: LifespanFactory) -> LifespanFactory:
        _state_registry[state] = factory
        return factory

    return wrapper
