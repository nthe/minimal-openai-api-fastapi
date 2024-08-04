import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .stubs import echo_message_handler, echo_stream_handler
from .stores import InMemoryStore
from .models.models import Model
from . import utils


logger = logging.getLogger("uvicorn")

yprint = lambda text: logger.info(f"\033[93m{text}\033[0m")


@asynccontextmanager
async def bootstrap(app: FastAPI):
    yprint("[OpenAI Compatible API]")

    yprint("Setting up message and stream request handlers.")
    yprint(" (Note that these should be overridden with custom implementations.)")
    app.state.message_request_handler = echo_message_handler
    app.state.stream_request_handler = echo_stream_handler

    # load store state from disk?
    yprint("Setting up in-memory store.")
    app.state.store = InMemoryStore()

    # check models?
    yprint("Setting up models.")
    app.state.models = [
        Model(
            id=id,
            created=utils.get_time(),
        )
        for id in [
            "gpt-3",
            "gpt-4",
            "gpt-5",
        ]
    ]

    yield

    # store state to disk?
    yprint("State cleanup completed.")
