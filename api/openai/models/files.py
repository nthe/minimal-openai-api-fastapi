from typing import Literal

from pydantic import BaseModel, Field


class OpenAIFile(BaseModel):
    object_: Literal["file"] = Field(default="file", alias="object")
    id_: str = Field(alias="id")
    bytes_: int = Field(alias="bytes")
    created_at: int
    filename: str
    purpose: Literal[
        "assistants",
        "assistants_output",
        "batch",
        "batch_output",
        "fine-tune",
        "fine-tune-results",
        "vision",
    ]


class ListFilesResponse(BaseModel):
    object_: Literal["list"] = Field(default="list", alias="object")
    data: list[OpenAIFile]


class DeleteFileResponse(BaseModel):
    object_: Literal["file"] = Field(default="file", alias="object")
    id_: str = Field(alias="id")
    deleted: bool


class CreateFileRequest(BaseModel):
    purpose: Literal[
        "assistants",
        "batch",
        "fine-tune",
        "vision",
    ]
    file: bytes
