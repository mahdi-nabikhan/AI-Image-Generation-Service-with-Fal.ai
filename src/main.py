from fastapi import FastAPI

from generations.routers import router as generation_router


app = FastAPI(
    title="AI Image Generation Service",
    description="Image generation service using Fal.ai",
    version="1.0.0",
)

app.include_router(generation_router)