import datetime as dt
import typing as t
from math import ceil

from pydantic import BaseModel, Field, Json, TypeAdapter, field_validator

from lib.camelize import camelize


def dt_to_iso8601z(d: dt.datetime) -> str:
    """
    Convert datetime to iso 8601 format, adding milliseconds and "Z" suffix
    """
    return f"{d.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z"


class BaseSchema(BaseModel):
    model_config = {
        "json_encoders": {dt.datetime: dt_to_iso8601z},
        "populate_by_name": True,
        "alias_generator": camelize,
    }


M = t.TypeVar("M", bound=BaseSchema)
N = t.TypeVar("N")


class ErrorSchema(BaseSchema):
    """
    Error Schema for API Responses.
    """

    status: str = "ERROR"
    message: t.Union[str, None] = "Error Message"
    data: t.Union[t.Dict[str, t.Any], None] = None


class APIResponseBase(BaseSchema):
    # status: ResponseStatusEnum = ResponseStatusEnum.SUCCESS
    status: t.Literal["SUCCESS", "ERROR"] = "SUCCESS"
    message: t.Union[str, None] = None


class GenericPage(BaseSchema, t.Generic[M]):
    content: t.List[M]
    total_elements: int
    total_pages: int
    page_number: int
    page_size: int
    next_page: t.Union[int, None] = None
    previous_page: t.Union[int, None] = None

    @classmethod
    def build_model(cls, *, data: t.Union[t.List[M], None], total: int, limit: int, skip: int):
        if data is None:
            data = []

        total_pages = ceil(total / limit)
        page_number = int(skip / limit) + 1
        return GenericPage[M](
            content=data,
            total_elements=total,
            total_pages=total_pages or 1,
            page_number=page_number,
            page_size=limit,
            next_page=page_number + 1 if page_number < total_pages else None,
            previous_page=page_number - 1 if page_number > 1 else None,
        )


class APIResponse(APIResponseBase, t.Generic[M]):
    data: M


class APIPageResponse(APIResponseBase, t.Generic[M]):
    data: GenericPage[M]


class FilterRequest(BaseSchema):
    """
    (M should be a BaseSchema)
    A request that contains a filter.
    """

    filter: t.Union[Json, None] = Field(default=None, description="JSON filter")

    @classmethod
    def filter_type(cls) -> type:
        raise NotImplementedError("Subclasses must implement get_filter_type")

    @field_validator("filter")
    @classmethod
    def validate_filter(cls, value: Json):
        if value is None:
            return None
        return TypeAdapter(cls.filter_type()).validate_python(value)


class PaginationParams(BaseSchema):
    """
    A Pydantic model representing the pagination parameters for a request.
    """

    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size