from fastapi import APIRouter


router = APIRouter(
    tags=["Image Generation"],
)


@router.post("/generate/image")
async def generate_image():
    """
    Submit an asynchronous image generation request.
    """
    return {"message": "Image generation endpoint"}