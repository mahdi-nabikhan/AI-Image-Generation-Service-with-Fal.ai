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
        db.rollback()

        user.balance_ai += GENERATION_COST
        db.commit()
        raise HTTPException(
         status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to submit image generation request.",
        ) from exc
        



def process_generation_callback(db: Session,request_id: str,generation_status: str,result_url: str | None = None,) -> dict:
    """
    Process a Fal.ai generation callback and update the corresponding job.
    The callback is idempotent: if the generation job has already been
    processed, no further changes are made. Successful generations store
    the generated image URL, while failed generations refund the user
    exactly once using the is_refunded flag.

    Args:
        db: Active SQLAlchemy database session.
        request_id: Fal.ai request identifier used to locate the generation job.
        generation_status: Final generation status (SUCCESS or FAILED).
        result_url: URL of the generated image when the generation succeeds.

    Returns:
        A dictionary containing a processing message and the final job status.

    Raises:
        HTTPException: If the generation job or user does not exist, or if
            an unsupported generation status is received.
    """

    generation_job = db.scalar(
    select(GenerationJobModel)
    .where(
        GenerationJobModel.request_id == request_id)
    .with_for_update())

    if generation_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Generation job not found.",
        )

    if generation_job.status != "IN_QUEUE":
        return {
            "message": "Generation job has already been processed.",
            "status": generation_job.status,
        }

    user = db.scalar(
        select(UserModel).where(
            UserModel.id == generation_job.user_id
        )
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    if generation_status == "SUCCESS":

        generation_job.status = "SUCCESS"
        generation_job.result_url = result_url

    elif generation_status == "FAILED":

        generation_job.status = "FAILED"

        if not generation_job.is_refunded:
            user.balance_ai += generation_job.cost
            generation_job.is_refunded = True

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid generation status.",
        )

    db.commit()

    return {
        "message": "Generation callback processed successfully.",
        "status": generation_job.status,
    }