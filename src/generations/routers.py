from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from .schemas import (GenerationRequest,GenerationResponse,GenerationCallback,UserGenerationJobResponse)
from core.database import get_db
from .service import (generate_image,process_generation_callback)
from .models import GenerationJobModel


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
    
    




@router.post("/generate/image/callback")
async def generation_callback(
    data: GenerationCallback,
    db: Session = Depends(get_db),
):
    return process_generation_callback(
        db=db,
        request_id=data.request_id,
        generation_status=data.status,
        result_url=(
            data.payload.get("result_url")
            if data.payload
            else None
        ),
    )
    
    
    
    
@router.get("/my-files/{user_id}",response_model=list[UserGenerationJobResponse])
def get_user_generation_files(user_id: int,db: Session = Depends(get_db)):
    """
    Retrieve all generation jobs for a specific user.
    """

    jobs = (
        db.query(GenerationJobModel)
        .filter(GenerationJobModel.user_id == user_id)
        .order_by(GenerationJobModel.id.desc())
        .all()
    )

    return jobs