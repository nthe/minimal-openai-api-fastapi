from fastapi import APIRouter, HTTPException, Request

from ..models.models import ListModelsResponse, Model, DeleteModelResponse


router = APIRouter(
    prefix="/models",
    tags=["models"],
)


@router.get("/")
async def list_models(req: Request) -> ListModelsResponse:
    return ListModelsResponse(data=req.app.state.models)


@router.get("/{model_id}")
async def get_model(req: Request, model_id: str) -> Model:
    models = req.app.state.models
    if model := next(
        (m for m in models if m.id_ == model_id),
        None,
    ):
        return model
    raise HTTPException(
        status_code=404,
        detail="Model not found",
    )


@router.delete("/{model_id}")
async def delete_model(req: Request, model_id: str) -> DeleteModelResponse:
    models = req.app.state.models
    if model := next(
        (m for m in models if m.id_ == model_id),
        None,
    ):
        models.remove(model)
        return DeleteModelResponse(id=model_id, deleted=True)
    raise HTTPException(
        status_code=404,
        detail="Model not found",
    )
