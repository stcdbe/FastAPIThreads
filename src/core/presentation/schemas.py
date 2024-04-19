from pydantic import BaseModel, ConfigDict


class AttrsBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Message(BaseModel):
    message: str
