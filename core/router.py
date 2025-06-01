import typing as t

from fastapi import APIRouter, Depends, FastAPI, Header
from fastapi.routing import APIRoute

from common.errors import InvalidApiVersionError
from core import cfg
from products.api import product_router


ParentT = t.TypeVar("ParentT", APIRouter, FastAPI)


def remove_trailing_slashes_from_routes(parent: ParentT) -> ParentT:
    "Removes trailing slashes from all routes in the given router"

    for route in parent.routes:
        if isinstance(route, APIRoute):
            route.path = route.path.rstrip("/")

    return parent


async def get_api_version(api_version: str = Header(example=cfg.API_VERSION)):
    """Maybe ignore minors?"""
    if api_version != cfg.API_VERSION:
        raise InvalidApiVersionError()


main_router = APIRouter()
router_with_api_version = APIRouter(dependencies=[Depends(get_api_version)])


router_with_api_version.include_router(product_router)
main_router.include_router(router_with_api_version)

remove_trailing_slashes_from_routes(main_router)