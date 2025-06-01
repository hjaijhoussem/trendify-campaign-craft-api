import typing as t
from functools import wraps

from databases.backends.common.records import Record
from pydantic import BaseModel as PydanticBaseModel
from pydantic import TypeAdapter
from sqlalchemy import Column, DateTime, func, text
from sqlalchemy.dialects.postgresql import UUID

PgUUID = UUID(as_uuid=False)


def uuid_pk():
    """
    Generate random UUID primary key column
    """
    return Column(
        "id",
        PgUUID,
        index=True,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        nullable=False,
        unique=True,
    )


def created_at(index=False):
    """
    Generate created_at column (optionally indexed) with current time as default
    """
    return Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=index,
    )


def updated_at(index=False):
    """
    Generate updated_at column (optionally indexed) with None as default
    """
    return Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        index=index,
    )


T = t.TypeVar("T")


def map_to(obj: t.Any, to_type: t.Type[T]) -> T:
    """
    Convert object to a pydantic BaseModel class.

    :param obj: object to convert
    :param to_type: destination pydantic type
    :return: converted object
    """
    if obj is None:
        return None
    if isinstance(obj, Record):
        obj = dict(obj)
    if isinstance(obj, PydanticBaseModel):  # Convert from one Pydantic model to another
        obj = obj.model_dump()
    if isinstance(obj, list):
        return [
            TypeAdapter(to_type).validate_python(
                item.model_dump()
                if isinstance(item, PydanticBaseModel)
                else dict(item)
                if isinstance(item, Record)
                else item
            )
            for item in obj
        ]
    return TypeAdapter(to_type).validate_python(obj) if obj else obj


def map_result(function: t.Callable) -> t.Callable:
    """Map result returned by wrapped function to the
    declared return type, which must extend BaseSchema class."""

    @wraps(function)
    async def wrapper(*args, **kwargs):
        return_type = t.get_type_hints(wrapper).get("return")
        result = await function(*args, **kwargs)
        if isinstance(result, Record):
            if result is None:
                return None
            result = dict(result)
        return TypeAdapter(return_type).validate_python(result) if return_type and result else result

    return wrapper