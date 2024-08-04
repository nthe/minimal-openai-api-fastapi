import asyncio

from .models import chat as models
from . import utils


async def echo_message_handler(request: models.CreateChatCompletionRequest):
    await asyncio.sleep(0)
    return models.CreateChatCompletionResponse(
        id="chat-completion-1",
        choices=[
            models.CreateChatCompletionChoiceResponse(
                message=models.ChatCompletionResponseMessage(
                    content=f"Got your message! - {request.messages[0].content}",
                    tool_calls=[],
                ),
                index=0,
            )
        ],
        created=utils.get_time(),
        model=request.model,
        system_fingerprint="",
        usage=models.CompletionUsage(
            prompt_tokens=0,
            completion_tokens=0,
            total_tokens=0,
        ),
    )


async def echo_stream_handler(request: models.CreateChatCompletionRequest):
    chunks = f"Got your message! - {request.messages[0].content}".split()
    for i, chunk in enumerate(chunks):
        await asyncio.sleep(0)
        finish_reason = None if i < len(chunks) - 1 else "stop"
        yield models.CreateChatCompletionStreamResponse(
            id="chat-completion-1",
            choices=[
                models.CreateChatCompletionStreamChoiceResponse(
                    delta=models.ChatCompletionStreamResponseDelta(
                        content=f"{chunk} ",
                        tool_calls=[],
                    ),
                    index=i,
                    finish_reason=finish_reason,
                )
            ],
            created=utils.get_time(),
            model=request.model,
            system_fingerprint="",
            usage=models.CompletionUsage(
                prompt_tokens=0,
                completion_tokens=0,
                total_tokens=0,
            ),
        )
