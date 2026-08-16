import fal_client
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.config import setting
from generations.models import GenerationJobModel
from user.models import UserModel


GENERATION_COST = 50
FAL_MODEL = "fal-ai/nano-banana"


async def generate_image(
    db: Session,
    user_id: int,
    prompt: str,
    aspect_ratio: str,
) -> dict:
    """
    Submit an asynchronous image generation request to Fal.ai.

    The user's AI balance is checked and the generation cost is deducted
    before submitting the request. A GenerationJob is created with an
    IN_QUEUE status after Fal.ai accepts the request.
    """


    user = db.scalar(
        select(UserModel).where(UserModel.id == user_id)
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )


    if user.balance_ai < GENERATION_COST:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient AI balance.",
        )


    user.balance_ai -= GENERATION_COST
    db.commit()

    try:
        
        handle = await fal_client.submit_async(
            FAL_MODEL,
            arguments={
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
            },
            webhook_url=setting.WEBHOOK_URL,
        )

        request_id = handle.request_id

    
        generation_job = GenerationJobModel(
            request_id=request_id,
            user_id=user_id,
            prompt=prompt,
            status="IN_QUEUE",
            cost=GENERATION_COST,
            is_refunded=False,
            result_url=None,
        )

        db.add(generation_job)
        db.commit()

        return {
            "request_id": request_id,
            "status": "IN_QUEUE",
            "cost": GENERATION_COST,
        }

    except Exception as exc:
   
        user.balance_ai += GENERATION_COST
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to submit image generation request.",
        ) from exc