from typing import (
    AsyncGenerator,
    Awaitable,
    Callable,
    TypeAlias,
)

from .models import chat as models


MessageRequestHandler: TypeAlias = Callable[
    [models.CreateChatCompletionRequest],
    Awaitable[models.CreateChatCompletionResponse],
]

StreamRequestHandler: TypeAlias = Callable[
    [models.CreateChatCompletionRequest],
    AsyncGenerator[models.CreateChatCompletionStreamResponse, None],
]
