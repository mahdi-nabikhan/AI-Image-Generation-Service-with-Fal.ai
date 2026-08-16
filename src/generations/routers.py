from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from .schemas import (GenerationRequest,GenerationResponse)
from core.database import get_db
from .service import (generate_image)


router = APIRouter(
    tags=["Image Generation"],
)


@router.post(
    "/generate/image",
    response_model=GenerationResponse,
)
async def generate_image_endpoint(
    data: GenerationRequest,
    db: Session = Depends(get_db),
):
    return await generate_image(
        db=db,
        user_id=data.user_id,
        prompt=data.prompt,
        aspect_ratio=data.aspect_ratio,
    )