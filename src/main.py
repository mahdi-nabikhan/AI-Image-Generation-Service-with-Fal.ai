from fastapi import FastAPI

from generations.routers import router as generation_router
from user.routers import router as user_router
from core.database import Base, engine
from generations.models import GenerationJobModel
from user.models import UserModel
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Image Generation Service",
    description="Image generation service using Fal.ai",
    version="1.0.0",
)

app.include_router(generation_router)
app.include_router(user_router)