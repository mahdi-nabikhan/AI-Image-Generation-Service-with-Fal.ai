from enum import Enum
from pydantic import BaseModel, Field
from typing import Any


class GenerationStatus(str, Enum):
    IN_QUEUE = "IN_QUEUE"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class GenerationRequest(BaseModel):
    """
    Request schema for submitting an image generation job.

    Attributes:
        user_id: ID of the user requesting image generation.
        prompt: Text prompt used to generate the image.
        aspect_ratio: Desired aspect ratio of the generated image.
    """

    user_id: int = Field(..., gt=0)
    prompt: str = Field(..., min_length=1)
    aspect_ratio: str = Field(default="1:1")


class GenerationResponse(BaseModel):
    """
    Response schema returned after successfully submitting a generation job.

    Attributes:
        request_id: Request identifier returned by Fal.ai.
        status: Current status of the generation job.
        cost: Fixed amount charged for the generation.
    """

    request_id: str
    status: GenerationStatus
    cost: float
    




class GenerationCallback(BaseModel):
    """
    Payload received from Fal.ai after an image generation job completes.

    Attributes:
        request_id: Unique identifier of the generation request assigned by Fal.ai.
        status: Final generation status, such as SUCCESS or FAILED.
        payload: Optional result payload returned by Fal.ai.
    """
    request_id: str
    status: str
    payload: dict[str, Any] | None = None