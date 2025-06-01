import typing as t

from injector import Injector

T = t.TypeVar("T")


injector = Injector()


def on(dependency_class: t.Type[T]) -> t.Callable[[], T]:
    """Bridge between FastAPI injection and 'injector' DI framework."""
    return lambda: injector.get(dependency_class)


async def configure():
    pass