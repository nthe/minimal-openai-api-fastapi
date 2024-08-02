import asyncio
from typing import AsyncGenerator, AsyncIterable

from fastapi import APIRouter, HTTPException, Request
from starlette.responses import StreamingResponse

from ..models.chat import (
    CreateChatCompletionRequest,
    CreateChatCompletionStreamResponse,
)
from ..types import MessageRequestHandler, StreamRequestHandler


router = APIRouter(
    prefix="/chat/completions",
    tags=["chat completions"],
)


async def as_sse_generator(
    coro: AsyncGenerator[CreateChatCompletionStreamResponse, None]
) -> AsyncIterable[str]:
    async for chunk in coro:
        yield f"data: {chunk.model_dump_json()}\n\n"
        await asyncio.sleep(0)
    yield "data: [DONE]\n\n"


@router.post("/")
async def chat_completions(
    req: Request,
    body: CreateChatCompletionRequest,
):  # -> models.CreateChatCompletionResponse | StreamingResponse:

    if not body.messages:
        raise HTTPException(
            status_code=400,
            detail="No messages provided",
        )

    state = req.app.state

    if not body.stream:
        message_handler: MessageRequestHandler = state.message_request_handler
        return await message_handler(body)

    streaming_handler: StreamRequestHandler = state.stream_request_handler
    return StreamingResponse(
        as_sse_generator(streaming_handler(body)),
        media_type="application/x-ndjson",
    )
