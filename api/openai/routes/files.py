from typing import Literal

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile

from ..models.files import DeleteFileResponse, ListFilesResponse, OpenAIFile
from ..stores import BaseStore, StoreFileRequest, StoreFileResponse
from .. import utils


router = APIRouter(
    prefix="/files",
    tags=["files"],
)


def store_response_to_openai_model(file: StoreFileResponse) -> OpenAIFile:
    return OpenAIFile(
        id=file.id,
        filename=file.name,
        bytes=len(file.content),
        created_at=file.created_at,
        purpose=file.metadata.get("purpose", "assistants"),
    )


@router.post("/")
async def upload_file(
    req: Request,
    purpose: Literal["assistants", "batch", "fine-tune", "vision"] = Form(),
    file: UploadFile = File(...),
) -> OpenAIFile:
    store: BaseStore = req.app.state.store

    name = file.filename or "n/a"
    content = await file.read()
    created_at = utils.get_time()

    metadata = dict(await req.form())
    metadata.pop("file", None)

    stored_file: StoreFileResponse = await store.add(
        StoreFileRequest(
            name=name,
            content=content,
            created_at=created_at,
            metadata={
                **metadata,
                "purpose": purpose,
            },
        )
    )

    return store_response_to_openai_model(stored_file)


@router.get("/")
async def list_files(req: Request) -> ListFilesResponse:
    store: BaseStore = req.app.state.store
    files: list[StoreFileResponse] = await store.get_all()
    return ListFilesResponse(
        data=list(map(store_response_to_openai_model, files)),
    )


@router.get("/{file_id}")
async def get_file(req: Request, file_id: str) -> OpenAIFile:
    store: BaseStore = req.app.state.store
    if file := await store.get(file_id):
        return store_response_to_openai_model(file)
    raise HTTPException(
        status_code=404,
        detail="File not found",
    )


@router.delete("/{file_id}")
async def delete_file(req: Request, file_id: str) -> DeleteFileResponse:
    store: BaseStore = req.app.state.store
    if success := await store.delete(file_id):
        return DeleteFileResponse(id=file_id, deleted=success)
    raise HTTPException(
        status_code=404,
        detail="File not found",
    )


@router.get("/{file_id}/content")
async def get_file_content(req: Request, file_id: str) -> bytes:
    store: BaseStore = req.app.state.store
    if file := await store.get(file_id):
        return file.content
    raise HTTPException(
        status_code=404,
        detail="File not found",
    )
