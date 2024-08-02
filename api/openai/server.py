from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from .routes.chat import router as chat_router
from .routes.files import router as files_router
from .routes.models import router as models_router
from .state import bootstrap

app = FastAPI(
    title="OpenAI Compatible API",
    version="v1",
    description="The OpenAI compatible API.",
    root_path="/api/v1",
    lifespan=bootstrap,
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(files_router)
app.include_router(models_router)


@app.get("/health")
async def healthCheck():
    return {"message": "success"}


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
