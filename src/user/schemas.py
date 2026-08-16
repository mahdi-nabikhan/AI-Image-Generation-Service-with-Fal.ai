from pydantic import BaseModel, ConfigDict



class UserCreateRequest(BaseModel):
    balance_ai: float



class UserCreateResponse(BaseModel):
    id: int
    balance_ai: float

    model_config = ConfigDict(from_attributes=True)