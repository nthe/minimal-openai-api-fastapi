from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ChatCompletionRequestMessage(BaseModel):
    model_config = ConfigDict(extra="allow")

    content: str
    role: Literal[
        "system",
        "user",
        "assistant",
        "tool",
        "function",
    ]


class CreateChatCompletionRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    model: str
    messages: list[ChatCompletionRequestMessage]
    stream: bool | None = True
    user: str | None = None
    temperature: float | None = 1.0
    top_p: float | None = 1.0
    seed: int | None = None


class CompletionUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponseMessage(BaseModel):
    content: str
    tool_calls: list
    role: Literal[
        "system",
        "user",
        "assistant",
        "tool",
    ] = Field(default="assistant")


class CreateChatCompletionChoiceResponse(BaseModel):
    message: ChatCompletionResponseMessage
    # TODO: logprobs model
    logprobs: dict | None = Field(default=None)
    finish_reason: Literal[
        "stop",
        "length",
        "content_filter",
        "tool_calls",
        "function_call",
    ] = Field(default="stop")
    index: int


class CreateChatCompletionResponse(BaseModel):
    id_: str = Field(alias="id")
    choices: list[CreateChatCompletionChoiceResponse]
    created: int
    model: str
    object_: Literal["chat.completion"] = Field(
        default="chat.completion",
        alias="object",
    )
    usage: CompletionUsage


class ChatCompletionStreamResponseDelta(BaseModel):
    content: str
    tool_calls: list
    role: Literal[
        "system",
        "user",
        "assistant",
        "tool",
    ] = Field(default="assistant")


class CreateChatCompletionStreamChoiceResponse(BaseModel):
    delta: ChatCompletionStreamResponseDelta
    # TODO: logprobs model
    logprobs: dict | None = Field(default=None)
    finish_reason: (
        Literal[
            "stop",
            "length",
            "content_filter",
            "tool_calls",
            "function_call",
        ]
        | None
    ) = Field(default="stop")
    index: int


class CreateChatCompletionStreamResponse(BaseModel):
    id_: str = Field(alias="id")
    choices: list[CreateChatCompletionStreamChoiceResponse]
    created: int
    model: str
    object_: Literal["chat.completion.chunk"] = Field(
        default="chat.completion.chunk",
        alias="object",
    )
    usage: CompletionUsage
