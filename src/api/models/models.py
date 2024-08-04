from typing import Literal

from pydantic import BaseModel, Field


class Model(BaseModel):
    object_: Literal["model"] = Field(default="model", alias="object")
    owned_by: str = Field(default="evil-corp")
    id_: str = Field(alias="id")
    created: int


class ListModelsResponse(BaseModel):
    object_: Literal["list"] = Field(default="list", alias="object")
    data: list[Model]


class DeleteModelResponse(BaseModel):
    object_: Literal["model"] = Field(default="model", alias="object")
    id_: str = Field(alias="id")
    deleted: bool
