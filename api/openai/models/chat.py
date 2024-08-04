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


class AssistantsApiResponseFormat(BaseModel):
    type: Literal["text", "json_object"] = "text"


class ChatCompletionStreamOptions(BaseModel):
    include_usage: bool | None = None


class FunctionObject(BaseModel):
    description: str | None = None
    name: str
    parameters: dict | None = None


class ChatCompletionTool(BaseModel):
    type: Literal["function"] = "function"
    function: FunctionObject


class ChatCompletionNamedToolChoice(BaseModel):
    name: str


class ChatCompletionToolChoiceOption(BaseModel):
    type: Literal["function"] = "function"
    function: ChatCompletionNamedToolChoice


class CreateChatCompletionRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    model: str
    messages: list[ChatCompletionRequestMessage]

    stream: bool | None = True
    user: str | None = None
    service_tier: Literal["auto", "default"] | None = None

    frequency_penalty: float | None = 0.0
    presence_penalty: float | None = 0.0

    logit_bias: dict[str, float] | None = None
    logprobs: bool | None = False
    top_logprobs: int | None = 0

    n: int | None = 1
    max_tokens: int | None = None

    response_format: AssistantsApiResponseFormat | None = None
    stream_options: ChatCompletionStreamOptions | None = None

    temperature: float | None = 1.0
    top_p: float | None = 1.0
    seed: int | None = None
    stop: str | list[str] | None = None

    tools: list[ChatCompletionTool] | None = None
    tool_choice: str | ChatCompletionToolChoiceOption | None = None
    parallel_tool_calls: bool | None = True


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
    service_tier: Literal["scale", "default"] | None = None
    system_fingerprint: str
    object_: Literal["chat.completion.chunk"] = Field(
        default="chat.completion.chunk",
        alias="object",
    )
    usage: CompletionUsage
