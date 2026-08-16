from pydantic import BaseModel, ConfigDict


class UserCreateResponse(BaseModel):
    id: int
    balance_ai: float

    model_config = ConfigDict(from_attributes=True)