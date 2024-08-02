from __future__ import annotations

import abc
from dataclasses import dataclass, field


@dataclass
class StoreFileRequest:
    """Dataclass for storing a file and its content."""

    name: str
    content: bytes
    created_at: int
    metadata: dict = field(default_factory=dict)


@dataclass
class StoreFileResponse:
    """Dataclass for storing a file and its content."""

    id: str
    name: str
    content: bytes
    created_at: int
    metadata: dict = field(default_factory=dict)

    @classmethod
    def from_request(cls, file: StoreFileRequest, id: str) -> StoreFileResponse:
        return cls(
            id=id,
            name=file.name,
            content=file.content,
            created_at=file.created_at,
            metadata=file.metadata,
        )


class BaseStore(abc.ABC):
    """Abstract base class for store implementations."""

    @abc.abstractmethod
    async def add(self, file: StoreFileRequest) -> StoreFileResponse:
        """Store a file and its content in store."""

    @abc.abstractmethod
    async def get(self, file_id: str) -> StoreFileResponse | None:
        """Retrieve a file and its content from store."""

    @abc.abstractmethod
    async def get_all(self) -> list[StoreFileResponse]:
        """Retrieve all files and their content from store."""

    @abc.abstractmethod
    async def delete(self, file_id: str) -> bool:
        """Delete a file and its content from store."""

    @abc.abstractmethod
    async def exists(self, file_id: str) -> bool:
        """Check if a file exists in store."""
