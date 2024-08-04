from .base import BaseStore, StoreFileRequest, StoreFileResponse
from ..utils import get_hash


class InMemoryStore(BaseStore):
    """In-memory store implementation."""

    def __init__(self) -> None:
        self._index: dict[str, StoreFileResponse] = {}

    async def add(self, file: StoreFileRequest) -> StoreFileResponse:
        file_id: str = f"file-{get_hash()}"
        record = StoreFileResponse.from_request(file, file_id)
        self._index[file_id] = record
        return record

    async def get(self, file_id: str) -> StoreFileResponse | None:
        return self._index.get(file_id, None)

    async def get_all(self) -> list[StoreFileResponse]:
        return list(self._index.values())

    async def delete(self, file_id: str) -> bool:
        return self._index.pop(file_id, None) is not None

    async def exists(self, file_id: str) -> bool:
        return file_id in self._index
