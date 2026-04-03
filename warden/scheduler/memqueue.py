"""Async queue with memory to filter for duplicate put calls"""

from asyncio import Queue
from copy import deepcopy

from warden.lib.qpu_client import QPUJobInfo


class MemQueue(Queue[QPUJobInfo]):
    def __init__(self, *args, **kwargs):
        self.memmm: QPUJobInfo | None = None
        super().__init__(*args, **kwargs)

    async def put(self, item: QPUJobInfo):
        if item != self.memmm:
            self.memmm = deepcopy(item)
            return await super().put(item)
