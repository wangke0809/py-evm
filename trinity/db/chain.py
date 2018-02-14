import asyncio
import functools

from multiprocessing.managers import (
    BaseProxy,
)


def async_method(method_name):
    async def method(self, *args, **kwargs):
        loop = asyncio.get_event_loop()

        return await loop.run_in_executor(
            None,
            functools.partial(self._callmethod, kwds=kwargs),
            method_name,
            args,
        )
    return method


def sync_method(method_name):
    def method(self, *args, **kwargs):
        return self._callmethod(method_name, args, kwargs)
    return method


class ChainDBProxy(BaseProxy):
    coro_get_block_header_by_hash = async_method('get_block_header_by_hash')
    coro_get_canonical_head = async_method('get_canonical_head')
    coro_header_exists = async_method('header_exists')
    coro_lookup_block_hash = async_method('lookup_block_hash')
    coro_persist_header_to_db = async_method('persist_header_to_db')

    get_block_header_by_hash = sync_method('get_block_header_by_hash')
    get_canonical_head = sync_method('get_canonical_head')
    get_score = sync_method('get_score')
    header_exists = sync_method('header_exists')
    lookup_block_hash = sync_method('lookup_block_hash')
